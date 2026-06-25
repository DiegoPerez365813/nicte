"""Safety layer: emergency detection, disclaimer injection, citation validation.

This logic is deterministic and server-side by design — it must not depend
on the LLM remembering to behave; see system-prompt design notes in the
product engineering plan.
"""

import re

from app.rag import RetrievedChunk

STANDARD_DISCLAIMER = (
    "\n\nRecuerda que esta información es orientativa. Para tu caso específico, "
    "te recomiendo consultar con un abogado certificado que pueda asesorarte de "
    "forma personalizada. Nicté te ayuda a entender tus derechos — un abogado "
    "te ayuda a ejercerlos."
)

EMERGENCY_PATTERNS = [
    r"\bme\s+quiere[n]?\s+matar\b",
    r"\bviolencia\s+(familiar|dom[eé]stica)\b",
    r"\bme\s+est[aá]\s+golpeando\b",
    r"\bpeligro\s+inmediato\b",
    r"\bsecuestr",
]

EMERGENCY_RESPONSE = (
    "Lo que describes puede ser una emergencia. Nicté no puede intervenir en "
    "situaciones de riesgo inmediato. Por favor contacta de inmediato al 911, "
    "o si se trata de violencia familiar, a la Línea Nacional contra la "
    "Violencia (911 / *088). Si estás a salvo y quieres entender tus derechos "
    "una vez resuelta la emergencia, aquí estaré."
)

OUT_OF_SCOPE_RESPONSE = (
    "Esa pregunta está fuera de mi área — solo puedo orientarte sobre el "
    "sistema jurídico mexicano. Si tienes una duda legal, cuéntame con más "
    "detalle y con gusto te ayudo."
)


def detect_emergency(message: str) -> bool:
    lowered = message.lower()
    return any(re.search(pattern, lowered) for pattern in EMERGENCY_PATTERNS)


_ARTICLE_CITATION_PATTERN = re.compile(
    r"art[íi]culo\s+(\d+(?:-[A-Za-zÑñ]{1,3})?(?:\s+(?:bis|ter|qu[áa]ter|quinquies))?)",
    re.IGNORECASE,
)


def _normalize_article_number(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def validate_citations(answer_text: str, retrieved: list[RetrievedChunk]) -> bool:
    """Returns True if every article number the model claims to cite was
    actually present in the retrieved context. Crude but effective guard
    against hallucinated citations. Article numbers with suffixes (e.g.
    "199 Quáter") are matched in full, not just their leading digits."""
    cited_articles = {
        _normalize_article_number(m) for m in _ARTICLE_CITATION_PATTERN.findall(answer_text)
    }
    retrieved_articles = {_normalize_article_number(chunk.article_number) for chunk in retrieved}
    return cited_articles.issubset(retrieved_articles)


def append_disclaimer(answer_text: str) -> str:
    if STANDARD_DISCLAIMER.strip() not in answer_text:
        return answer_text + STANDARD_DISCLAIMER
    return answer_text
