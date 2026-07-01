import uuid

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from app.area_classifier import classify_areas
from app.clarification import build_clarification_message, needs_clarification
from app.llm import generate_answer
from app.rag import get_retriever
from app.safety import (
    EMERGENCY_RESPONSE,
    OUT_OF_SCOPE_RESPONSE,
    append_disclaimer,
    detect_emergency,
    validate_citations,
)
from app.schemas import ChatRequest, ChatResponse, Citation
from app.municipal_contacts import detect_municipality, municipal_contacts_block
from app.session_store import (
    append_history,
    get_history,
    get_state,
    resolve_clarification,
    set_state,
    start_clarification,
)
from app.state_detector import detect_state

app = FastAPI(title="Nicté API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten before production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def warm_up_retriever() -> None:
    # Build the embedding index once, eagerly, at process start. Without
    # this, the first concurrent requests can each see an uninitialized
    # retriever and race to build it (encoding ~7k articles) at the same
    # time, starving the CPU and timing out every request involved.
    get_retriever()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/v1/chat/message", response_model=ChatResponse)
def chat_message(request: ChatRequest) -> ChatResponse:
    session_id = request.session_id or str(uuid.uuid4())

    if detect_emergency(request.message):
        return ChatResponse(
            session_id=session_id,
            answer=EMERGENCY_RESPONSE,
            citations=[],
            legal_area="emergencia",
            safety_flag="emergency",
        )

    # Detect municipality for hyper-local contact info (contraloría, DIF, etc.)
    mentioned_municipality = detect_municipality(request.message)
    if mentioned_municipality:
        set_state(session_id, mentioned_municipality)  # municipality implies state too via contacts

    # Remember the user's state as soon as it's mentioned, on every message
    # regardless of which branch handles it below — most penal/civil/familiar
    # law in Mexico is state jurisdiction, so this scopes retrieval to the
    # right code instead of guessing from federal law alone. Re-check every
    # message in case the user corrects themselves.
    mentioned_state = detect_state(request.message)
    if mentioned_state:
        set_state(session_id, mentioned_state)
    user_state = get_state(session_id)

    # Two-turn triage: if this session already asked clarifying questions
    # and is waiting on the reply, fold both messages into one specific
    # query instead of treating the reply as a brand-new, even vaguer
    # question. Otherwise, on a session's first message, ask 1-2 follow-ups
    # before retrieving anything — a real consultation starts with
    # questions, not a guess off a one-line message.
    prior_message = resolve_clarification(session_id)
    if prior_message is not None:
        effective_message = f"{prior_message}. {request.message}"
    else:
        likely_areas = classify_areas(request.message)
        area = likely_areas[0] if likely_areas else None
        if area and needs_clarification(area):
            start_clarification(session_id, request.message)
            return ChatResponse(
                session_id=session_id,
                answer=build_clarification_message(area, request.message),
                citations=[],
                legal_area=area,
                safety_flag=None,
            )
        effective_message = request.message

    retriever = get_retriever()
    retrieved = retriever.retrieve(effective_message, state=user_state)

    if not retrieved:
        return ChatResponse(
            session_id=session_id,
            answer=OUT_OF_SCOPE_RESPONSE,
            citations=[],
            legal_area="desconocido",
            safety_flag="low_confidence",
        )

    # Defense/due-process rights apply regardless of which crime is at
    # issue, so they're surfaced any time the question touches penal law —
    # not retrieved by similarity, looked up from a fixed constitutional set.
    defense_chunks = (
        retriever.get_defense_articles()
        if any(c.area == "penal" for c in retrieved)
        else []
    )

    history = get_history(session_id)
    raw_answer = generate_answer(
        effective_message, retrieved, defense_chunks,
        state=user_state, history=history,
        municipality=mentioned_municipality or None,
    )

    # Citation guard: flag unverified citations but keep the full answer —
    # replacing it with a generic "can't confirm" message is worse UX than
    # showing real guidance with a low-confidence banner.
    safety_flag = None if validate_citations(raw_answer, retrieved + defense_chunks) else "low_confidence"

    final_answer = append_disclaimer(raw_answer)

    append_history(session_id, "user", effective_message)
    append_history(session_id, "assistant", final_answer)

    citations = [
        Citation(
            law_name=c.law_name,
            article_number=c.article_number,
            jurisdiction=c.jurisdiction,
            source_url=c.source_url,
            relevance_score=round(c.score, 3),
            kind="fundamento",
        )
        for c in retrieved
    ] + [
        Citation(
            law_name=c.law_name,
            article_number=c.article_number,
            jurisdiction=c.jurisdiction,
            source_url=c.source_url,
            relevance_score=round(c.score, 3),
            kind="defensa",
            plain_summary=c.plain_summary,
        )
        for c in defense_chunks
    ]

    return ChatResponse(
        session_id=session_id,
        answer=final_answer,
        citations=citations,
        legal_area=retrieved[0].area,
        safety_flag=safety_flag,
    )
