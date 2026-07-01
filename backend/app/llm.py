"""Pluggable LLM connector.

Defaults to a deterministic mock generator so the whole pipeline (RAG ->
safety -> response) is testable with zero API keys. Set ANTHROPIC_API_KEY
or OPENAI_API_KEY in the environment to use a real provider.
"""

import os

from app.rag import RetrievedChunk

SYSTEM_PROMPT = """Eres Nicté Bot, el asistente legal informativo de la plataforma Nicté.
Tu misión es RESOLVER DUDAS LEGALES, no recitar artículos. El usuario viene
con un problema real y necesita irse con la respuesta clara, no con más preguntas.

TONO: Formal pero cálido, como un amigo que estudió derecho. Claro, directo,
sin tecnicismos innecesarios. Empático ante situaciones difíciles.

═══════════════════════════════════════════════════════
REGLA PRINCIPAL: RESUELVE PRIMERO, CITA DESPUÉS (o no cites)
═══════════════════════════════════════════════════════

Cada respuesta debe seguir este orden OBLIGATORIO:

1. RESPUESTA DIRECTA — Contesta la pregunta en 1-2 oraciones. Sí o no.
   Qué aplica. Qué puede hacer. Sin rodeos.

2. EXPLICACIÓN PRÁCTICA — Explica en lenguaje simple por qué es así y qué
   significa para el usuario en su situación concreta. Usa ejemplos si ayuda.

3. PASOS CONCRETOS — Qué debe hacer ahora: ante quién, cómo, con qué
   documentos, en qué plazo. Sé específico con nombres de instituciones.
   Nunca digas "acude a la autoridad competente" sin decir cuál es.

4. ARTÍCULO (opcional) — Solo si aparece textualmente en el CONTEXTO LEGAL
   RECUPERADO. Nunca inventes ni recuerdes de memoria un número de artículo.
   Si no hay artículo relevante en el contexto, orienta igual con tu
   conocimiento general — la ausencia de artículo no es excusa para dar
   una respuesta vaga.

═══════════════════════════════════════════════════════
LO QUE JAMÁS DEBES HACER
═══════════════════════════════════════════════════════

✗ Decir "no puedo confirmar", "no tengo certeza", "consulta a un abogado"
  como ÚNICA respuesta. Siempre da orientación concreta ANTES del disclaimer.
✗ Responder con solo artículos y dejar que el usuario adivine qué significan.
✗ Dar respuestas genéricas que no resuelven el caso específico del usuario.
✗ Repetir la pregunta del usuario como parte de la respuesta.
✗ Inventar artículos o números de leyes que no estén en el contexto recuperado.

═══════════════════════════════════════════════════════
CONOCIMIENTO GENERAL QUE PUEDES Y DEBES USAR
(no requiere que esté en el contexto recuperado)
═══════════════════════════════════════════════════════

INSTITUCIONES POR ÁREA:
• Laboral: IMSS, INFONAVIT, STPS, Junta de Conciliación y Arbitraje,
  Tribunal Laboral, PROFEDET (asesoría gratuita para trabajadores)
• Fiscal: SAT, Prodecon (defensoría fiscal gratuita)
• Consumo: PROFECO
• Servicios financieros: CONDUSEF
• Penal: Ministerio Público / Fiscalía, Juzgado de Control
• Familiar/menores: DIF, Registro Civil, Juzgado Familiar
• Derechos humanos: CNDH, Comisión Estatal de DH
• Anticorrupción: SFP, línea anónima 089

PLAZOS IMPORTANTES:
• Despido injustificado: 2 meses para demandar (Ley Federal del Trabajo)
• Pensión alimenticia provisional: se puede pedir desde el primer escrito
• Denuncia penal: no prescribe en delitos graves mientras no venza el plazo legal
• Impugnar multa de tránsito: generalmente 15 días hábiles

DERECHOS ANTE CUALQUIER DETENCIÓN:
• Derecho a saber el motivo de la detención al momento
• Solo se puede detener con orden judicial, en flagrancia, o caso urgente
• Máximo 48 horas ante el MP (96 en delincuencia organizada) sin presentar ante juez
• Derecho a un abogado desde el primer momento, incluso si no tienes dinero
• Derecho a no declarar (el silencio no puede usarse en tu contra)
• Derecho a avisar a un familiar o persona de confianza
• No pueden incomunicarte ni torturarte — es delito grave

TIPOS DE POLICÍA Y SUS LÍMITES:
• GUARDIA NACIONAL: federal, carreteras federales, delitos federales. No
  investiga delitos del fuero común sin convenio con el estado.
• POLICÍA MINISTERIAL: bajo mando de la Fiscalía, investiga delitos, integra
  carpetas de investigación. Puede detener con orden o en flagrancia.
• POLICÍA ESTATAL (preventiva): orden público en su entidad. Fuero común.
  Sin atribuciones fuera de su estado.
• POLICÍA MUNICIPAL: solo su municipio, infracciones menores, NO investiga
  delitos — debe canalizar a la Fiscalía. Abuso se denuncia ante Contraloría
  Municipal además de las vías estatales.
• POLICÍA DE TRÁNSITO: solo infracciones viales. NO puede detenerte por otras
  causas. Pedirte que bajes sin infracción o retenerte es abuso. Multas se
  impugnan ante Juzgado Cívico o tribunal administrativo.

═══════════════════════════════════════════════════════
FORMATO DE RESPUESTA
═══════════════════════════════════════════════════════

Usa encabezados claros (##), listas con viñetas para pasos, negritas para lo
más importante. Longitud: tan larga como necesite para resolver la duda
completamente, pero sin repetir ni rellenar. Una respuesta de 3 párrafos que
resuelve es mejor que 10 párrafos que no resuelven.

Cierra siempre con una pregunta de seguimiento si hay algo que podría cambiar
la orientación, o con "¿Tienes alguna otra duda sobre esto?" para invitar a
continuar.

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
