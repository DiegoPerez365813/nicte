"""Clarifying-question triage — asks 1-2 follow-up questions before
answering, the way a lawyer would in a first consultation, instead of
generating an answer off a single vague message.

This does NOT make Nicté Bot a lawyer. It's a conversational pattern: a
short triage turn that gathers the missing details (when, what happened,
what's already been done) so the eventual retrieval query is specific
enough to find the right article instead of guessing from a one-line
question."""

CLARIFYING_QUESTIONS: dict[str, list[str]] = {
    "laboral": [
        "¿Cuánto tiempo llevabas trabajando ahí y tenías contrato por escrito?",
        "¿Te dieron alguna razón del despido, o algo por escrito?",
    ],
    "civil": [
        "¿En qué estado de la República ocurrió esto?",
        "¿Existe un contrato firmado para esta situación?",
        "¿Ya intentaste resolverlo directamente con la otra parte?",
    ],
    "penal": [
        "¿En qué estado de la República ocurrió esto?",
        "¿Ya levantaste una denuncia ante el Ministerio Público, o aún no?",
        "¿Hay algún riesgo inmediato para tu seguridad en este momento?",
    ],
    "familiar": [
        "¿En qué estado de la República ocurrió esto?",
        "¿Hay ya algún acuerdo, convenio o resolución judicial previa sobre esto?",
        "¿Los menores involucrados están actualmente a salvo?",
    ],
    "mercantil": [
        "¿La empresa o relación comercial está formalizada (contrato, factura, sociedad registrada)?",
        "¿Qué monto o alcance tiene el asunto?",
    ],
    "fiscal": [
        "¿Ya recibiste alguna notificación oficial del SAT sobre esto?",
        "¿De qué periodo fiscal se trata?",
    ],
}


def needs_clarification(area: str) -> bool:
    return area in CLARIFYING_QUESTIONS


def build_clarification_message(area: str) -> str:
    questions = CLARIFYING_QUESTIONS[area]
    lines = [
        "Antes de darte una orientación más precisa, déjame hacerte un par de "
        "preguntas sobre tu situación:",
        "",
    ]
    lines.extend(f"{i + 1}. {q}" for i, q in enumerate(questions))
    lines.append("")
    lines.append("Cuéntame lo que puedas y con gusto te explico qué dice la ley para tu caso.")
    return "\n".join(lines)
