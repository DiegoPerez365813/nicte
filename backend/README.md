# Nicté Backend — MVP Slice (Chat + RAG, área laboral)

Proof-of-concept vertical slice: chat endpoint grounded by RAG retrieval over
a sample of the Ley Federal del Trabajo, with the safety layer (emergency
detection, disclaimer injection, citation hallucination guard) wired in.

## Run

```
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Server runs at `http://127.0.0.1:8000`. Health check: `GET /health`.

## Test

```
python test_client.py "¿Qué pasa si me despiden sin previo aviso?"
python test_client.py "¿Cuántos días de vacaciones me corresponden con 2 años de antigüedad?"
python test_client.py "me quiere matar mi pareja"        # triggers emergency safety flag
python test_client.py "cómo hago un pastel de chocolate"  # triggers out-of-scope fallback
```

Or via curl:

```
curl -X POST http://127.0.0.1:8000/v1/chat/message ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"¿Qué pasa si me despiden sin previo aviso?\"}"
```

## What this slice proves

- **RAG grounding**: answers are constrained to retrieved statute chunks
  (in-memory cosine similarity over sentence-transformer embeddings —
  stand-in for pgvector, same retrieval contract).
- **Citation discipline**: `app/safety.py::validate_citations` strips any
  answer that cites an article not present in the retrieved context.
- **Emergency routing**: messages matching risk patterns short-circuit to a
  hotline redirect instead of generating legal content.
- **Disclaimer injection**: deterministic, appended server-side, never left
  to model discretion.

## What's mocked / not production-ready

- `app/llm.py` defaults to a deterministic mock generator (no API key
  needed). Real provider call (Anthropic/OpenAI) is a `NotImplementedError`
  stub — wire it in `generate_answer()` when ready.
- Vector index is in-memory, rebuilt on every server start. Swap for
  `pgvector` + persistent ingestion job before production.
- Only the "laboral" legal area has a corpus (`app/legal_corpus/laboral.py`).
  Other areas return the out-of-scope fallback until their corpora are added.
- No auth, no PostgreSQL persistence, no rate limiting yet — see the product
  engineering plan for the full backend architecture this slice will grow
  into.

## Next steps

1. Add corpora for civil/familiar/penal/mercantil areas.
2. Wire a real LLM provider behind `generate_answer()`.
3. Move retrieval to pgvector-backed PostgreSQL.
4. Add JWT auth + session persistence per the data model design.
5. Build the SwiftUI client against this same `/v1/chat/message` contract.
