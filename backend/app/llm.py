"""Pluggable LLM connector.

Defaults to a deterministic mock generator so the whole pipeline (RAG ->
safety -> response) is testable with zero API keys. Set ANTHROPIC_API_KEY
or OPENAI_API_KEY in the environment to use a real provider.
"""

import os

from app.rag import RetrievedChunk

SYSTEM_PROMPT = """Eres Nicté Bot, el asistente legal informativo de la plataforma Nicté.
Respondes sobre cualquier área del sistema jurídico mexicano (laboral, civil,
penal, familiar, mercantil, fiscal, constitucional, derechos humanos, trámites)
en un tono formal pero amigable: cortés, cálido y respetuoso, sin tecnicismos
innecesarios pero sin perder seriedad profesional.

Tu objetivo principal es responder directamente la pregunta del usuario y
ayudarle a resolver su duda o conflicto de forma práctica — no simplemente
recitar artículos. Para cada respuesta:
1. Primero contesta lo que el usuario realmente preguntó (sí/no, qué
   institución, qué proceso aplica), en lenguaje claro.
2. Tradúcelo a pasos concretos: qué trámite hacer, ante qué autoridad o
   institución, y qué documentos o plazos aplican. Nombra la institución o
   vía correcta según el tema: SAT (fiscal), IMSS/INFONAVIT (laboral),
   PROFECO (consumo), CONDUSEF (servicios financieros), Junta de
   Conciliación y Arbitraje o Tribunal Laboral (conflictos laborales),
   Ministerio Público/Fiscalía (penal), DIF (familiar/menores), Registro
   Civil, entre otras según corresponda — aunque el contexto legal recuperado
   no las mencione explícitamente, ya que esto es conocimiento general sobre
   cómo funcionan las instituciones mexicanas.
3. Cita un artículo o ley específica ÚNICAMENTE si aparece tal cual en el
   CONTEXTO LEGAL RECUPERADO que se te proporciona. Nunca escribas "artículo
   N" de una ley que no esté en ese contexto, ni inventes o recuerdes de
   memoria un número de artículo — aunque estés seguro de que existe. Si el
   contexto recuperado no contiene el fundamento exacto para la pregunta,
   dilo brevemente y continúa orientando con lo que sí sabes (instituciones,
   procesos, a quién acudir) sin citar ningún artículo.
4. No fuerces una cita legal cuando la pregunta no la necesita — por ejemplo,
   preguntas sobre "¿existe tal institución?" o "¿a quién acudo?" se
   responden directamente, sin que cada respuesta tenga que anclarse a un
   artículo.
5. Cuando la situación involucre policías, Ministerio Público u otras
   autoridades, explica con claridad qué SÍ pueden hacer y qué NO pueden
   hacer legalmente (por ejemplo: no pueden detenerte sin orden judicial o
   sin que exista flagrancia, no pueden retenerte más de 48 horas — 96 en
   delincuencia organizada — sin presentarte ante un juez, no pueden
   obligarte a declarar ni incomunicarte, tienes derecho a un abogado desde
   el primer momento). Indica también cómo defenderse si la autoridad se
   excede, y cómo denunciar abuso o corrupción: ante la institución estatal
   correspondiente (Fiscalía/Visitaduría/Asuntos Internos del estado,
   Contraloría o Secretaría Anticorrupción estatal, Comisión Estatal de
   Derechos Humanos) cuando conozcas el estado del usuario, y siempre
   mencionando las vías nacionales disponibles: la Comisión Nacional de los
   Derechos Humanos (CNDH), la Plataforma Nacional de Denuncia Ciudadana de
   la Secretaría Anticorrupción y Buen Gobierno, la línea de denuncia
   anónima 089, y la Fiscalía Especializada en Combate a la Corrupción que
   corresponda.

Nunca afirmas ser abogado. Nunca emites juicios morales sobre la situación
del usuario, incluso en temas delicados."""

# Local institutions worth naming when the user's state is known — generic
# legal knowledge, not tied to the retrieved corpus, so safe to surface even
# when validate_citations would reject an unsupported article number.
STATE_INSTITUTIONS: dict[str, dict[str, str]] = {
    "Ciudad de México": {
        "fiscalia": "Fiscalía General de Justicia de la Ciudad de México (FGJ CDMX)",
        "derechos_humanos": "Comisión de Derechos Humanos de la Ciudad de México (CDHCM)",
        "anticorrupcion": "Secretaría de la Contraloría General de la CDMX y Fiscalía Especializada en Combate a la Corrupción de la CDMX",
        "seguridad": "Secretaría de Seguridad Ciudadana de la CDMX (SSC) — Visitaduría/Asuntos Internos para quejas contra policías",
    },
    "Jalisco": {
        "fiscalia": "Fiscalía del Estado de Jalisco",
        "derechos_humanos": "Comisión Estatal de Derechos Humanos Jalisco (CEDHJ)",
        "anticorrupcion": "Secretaría de Transparencia, Integridad y Combate a la Corrupción de Jalisco y Fiscalía Especializada en Combate a la Corrupción de Jalisco",
        "seguridad": "Secretaría de Seguridad Pública de Jalisco — Visitaduría/Asuntos Internos para quejas contra policías",
    },
    "Nuevo León": {
        "fiscalia": "Fiscalía General de Justicia del Estado de Nuevo León",
        "derechos_humanos": "Comisión Estatal de Derechos Humanos de Nuevo León (CEDHNL)",
        "anticorrupcion": "Secretaría de la Contraloría y Transparencia Gubernamental de Nuevo León y Fiscalía Anticorrupción del Estado",
        "seguridad": "Secretaría de Seguridad Pública de Nuevo León — Visitaduría/Asuntos Internos para quejas contra policías",
    },
    "Estado de México": {
        "fiscalia": "Fiscalía General de Justicia del Estado de México",
        "derechos_humanos": "Comisión de Derechos Humanos del Estado de México (CODHEM)",
        "anticorrupcion": "Secretaría de la Contraloría del Estado de México y Fiscalía Especializada en Combate a la Corrupción",
        "seguridad": "Secretaría de Seguridad del Estado de México — Visitaduría/Asuntos Internos para quejas contra policías",
    },
}


def _generic_state_institutions(state: str) -> dict[str, str]:
    """Fallback institution names for states without a curated entry above,
    following the naming convention nearly every Mexican state uses. Close
    enough to point the user in the right direction even if a given state's
    exact official name differs slightly — this is general orientation, not
    a cited legal fact, so it isn't subject to validate_citations."""
    return {
        "fiscalia": f"Fiscalía General de Justicia del Estado de {state}",
        "derechos_humanos": f"Comisión Estatal de Derechos Humanos de {state}",
        "anticorrupcion": (
            f"Secretaría de la Contraloría del Estado de {state} y su Fiscalía "
            f"Especializada en Combate a la Corrupción"
        ),
        "seguridad": (
            f"Secretaría de Seguridad Pública del Estado de {state} — "
            f"Visitaduría/Asuntos Internos para quejas contra policías"
        ),
    }


def _state_institutions_block(state: str | None) -> str:
    if not state:
        return ""
    institutions = STATE_INSTITUTIONS.get(state) or _generic_state_institutions(state)
    lines = [
        "",
        f"INSTITUCIONES DE {state.upper()} QUE PUEDES NOMBRAR SI APLICA AL CASO:",
        f"- Fiscalía: {institutions['fiscalia']}",
        f"- Derechos humanos: {institutions['derechos_humanos']}",
        f"- Anticorrupción: {institutions['anticorrupcion']}",
        f"- Seguridad / quejas contra policías: {institutions['seguridad']}",
        "",
    ]
    return "\n".join(lines)


def _quote(chunk: RetrievedChunk, max_len: int = 280) -> str:
    text = chunk.text[:max_len].rstrip()
    return f'"{text}..."' if len(chunk.text) > max_len else f'"{chunk.text}"'


def _defense_section(defense_chunks: list[RetrievedChunk]) -> list[str]:
    if not defense_chunks:
        return []
    lines = [
        "",
        "Para defenderte, estos son derechos que te protegen sin importar el "
        "delito del que se trate:",
        "",
    ]
    for chunk in defense_chunks:
        lines.append(f"- Artículo {chunk.article_number} constitucional: {chunk.plain_summary}")
    return lines


def _mock_generate(
    message: str,
    context_chunks: list[RetrievedChunk],
    defense_chunks: list[RetrievedChunk] | None = None,
) -> str:
    """Deterministic stand-in for the LLM — grounds strictly on retrieved
    chunks so the demo behaves like a real RAG-constrained answer.

    When the retrieved chunks span more than one legal area (e.g. a single
    situation that has both a penal and a familiar dimension), the answer
    is structured as one section per area instead of only citing the single
    top match — real situations rarely fall under one neat legal box."""
    if not context_chunks:
        return (
            "No encontré una fuente específica en mi base de conocimiento para "
            "responder esto con precisión."
        )

    areas_seen: dict[str, RetrievedChunk] = {}
    for chunk in context_chunks:
        areas_seen.setdefault(chunk.area, chunk)

    if len(areas_seen) == 1:
        top = context_chunks[0]
        lines = [
            "Qué dice la ley:",
            f"Según el Artículo {top.article_number} de la {top.law_name}:",
            _quote(top),
            "",
            "En palabras simples:",
            "Ese es el texto oficial completo; lo importante para ti es que esta "
            "es la norma específica que aplica a tu situación. Los pasos "
            "concretos a seguir (qué trámite hacer, ante quién, en qué plazo) "
            "dependen de los detalles exactos de tu caso, que un abogado puede "
            "revisar contigo.",
        ]
        lines.extend(_defense_section(defense_chunks or []))
        return "\n".join(lines)

    area_labels = {
        "laboral": "Desde el punto de vista laboral",
        "civil": "Desde el punto de vista civil",
        "penal": "Desde el punto de vista penal",
        "familiar": "Desde el punto de vista familiar",
        "mercantil": "Desde el punto de vista mercantil",
        "fiscal": "Desde el punto de vista fiscal",
        "constitucional": "Desde el punto de vista constitucional",
        "derechos_humanos": "En materia de derechos humanos y protección de datos",
    }

    lines = [
        "Gracias por confiarme tu situación. Es un caso que toca más de un área "
        "del derecho mexicano, así que te lo explico por partes:",
        "",
    ]
    for area, chunk in areas_seen.items():
        label = area_labels.get(area, f"En materia de {area}")
        lines.append(f"{label} (Artículo {chunk.article_number}, {chunk.law_name}):")
        lines.append(_quote(chunk))
        lines.append("")

    lines.append(
        "Dada la seriedad del tema, te recomiendo no solo entender estos "
        "fundamentos, sino acudir a la autoridad competente (Ministerio "
        "Público, DIF, o un abogado certificado) para que tu caso se atienda "
        "de forma personalizada y oportuna."
    )
    lines.extend(_defense_section(defense_chunks or []))
    return "\n".join(lines)


_ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

_DEFENSE_INSTRUCTIONS = (
    "\n\nDERECHOS DE DEFENSA APLICABLES (menciónalos si el caso toca materia "
    "penal):\n{defense_block}"
)


def _anthropic_generate(
    message: str,
    context_chunks: list[RetrievedChunk],
    defense_chunks: list[RetrievedChunk] | None = None,
    state: str | None = None,
    history: list[dict] | None = None,
) -> str:
    import anthropic

    if not context_chunks:
        return (
            "No encontré una fuente específica en mi base de conocimiento para "
            "responder esto con precisión."
        )

    context_block = "\n\n".join(
        f"[{c.law_name}, Artículo {c.article_number}] {c.text}" for c in context_chunks
    )
    user_prompt = (
        f"CONTEXTO LEGAL RECUPERADO (úsalo como única fuente de verdad; cita "
        f"solo los artículos que aparecen aquí, nunca inventes uno):\n"
        f"{context_block}\n\n"
    )
    if defense_chunks:
        defense_block = "\n".join(
            f"- Artículo {c.article_number} constitucional: {c.plain_summary}"
            for c in defense_chunks
        )
        user_prompt += _DEFENSE_INSTRUCTIONS.format(defense_block=defense_block) + "\n\n"
    user_prompt += _state_institutions_block(state)
    user_prompt += f"PREGUNTA DEL USUARIO:\n{message}"

    messages = list(history or []) + [{"role": "user", "content": user_prompt}]

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=_ANTHROPIC_MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    return "".join(block.text for block in response.content if block.type == "text")


def generate_answer(
    message: str,
    context_chunks: list[RetrievedChunk],
    defense_chunks: list[RetrievedChunk] | None = None,
    state: str | None = None,
    history: list[dict] | None = None,
) -> str:
    if os.getenv("ANTHROPIC_API_KEY"):
        return _anthropic_generate(message, context_chunks, defense_chunks, state, history)
    return _mock_generate(message, context_chunks, defense_chunks)
