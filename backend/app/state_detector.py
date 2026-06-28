"""Detects which Mexican state a user is referring to from free text.

Used to scope retrieval to the right state's penal/civil code instead of
defaulting to federal-only law — most real disputes in Mexico are governed
by state law, not federal law. Returns the canonical state name used as
`jurisdiction` in app/ingest.py, so detection output can be passed straight
into LegalRetriever.retrieve(state=...).
"""

import re

# Canonical name -> aliases/abbreviations users actually type. Only states
# with an ingested corpus are listed for now (see app/ingest.py SOURCES);
# add an entry here whenever a new state's codes are ingested.
STATE_ALIASES: dict[str, list[str]] = {
    "Ciudad de México": [
        "ciudad de mexico", "cdmx", "distrito federal", "df", "mexico df",
        "mexico city",
    ],
    "Jalisco": ["jalisco", "guadalajara", "zapopan", "tlaquepaque"],
    "Nuevo León": [
        "nuevo leon", "monterrey", "san pedro garza garcia", "guadalupe nl",
    ],
    "Estado de México": [
        "estado de mexico", "edomex", "edo. de mexico", "edo de mexico",
        "ecatepec", "naucalpan", "toluca",
    ],
}

_NORMALIZE_PATTERN = re.compile(r"[^a-z0-9\s]")


def _normalize(text: str) -> str:
    # Strip all punctuation (not just collapse it to space) so "Jalisco,"
    # or "Jalisco." match the same as a bare "Jalisco" — word-boundary
    # checks below assume tokens are separated by whitespace only.
    return re.sub(r"\s+", " ", _NORMALIZE_PATTERN.sub(" ", text.lower())).strip()


def detect_state(text: str) -> str | None:
    """Returns the first canonical state name whose alias appears in text,
    or None if no known state is mentioned. Checks longer/more specific
    aliases first so "cdmx" doesn't get shadowed by a shorter false match."""
    normalized = _normalize(text)
    for state, aliases in STATE_ALIASES.items():
        for alias in sorted(aliases, key=len, reverse=True):
            if re.search(rf"\b{re.escape(alias.strip())}\b", normalized):
                return state
    return None
