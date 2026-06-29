"""Detects which Mexican state a user is referring to from free text.

Used to scope retrieval to the right state's penal/civil code instead of
defaulting to federal-only law — most real disputes in Mexico are governed
by state law, not federal law. Returns the canonical state name used as
`jurisdiction` in app/ingest.py, so detection output can be passed straight
into LegalRetriever.retrieve(state=...).
"""

import re
import unicodedata

# Canonical name -> aliases/abbreviations users actually type, covering all
# 32 federal entities (see app/ingest.py SOURCES for the matching corpus).
# Aliases are written without accents — _normalize() strips accents from
# both sides before comparing, so "México"/"mexico" are equivalent.
STATE_ALIASES: dict[str, list[str]] = {
    "Aguascalientes": ["aguascalientes"],
    "Baja California": ["baja california", "tijuana", "mexicali", "ensenada"],
    "Baja California Sur": ["baja california sur", "la paz bcs", "los cabos"],
    "Campeche": ["campeche"],
    "Chiapas": ["chiapas", "tuxtla gutierrez", "tapachula"],
    "Chihuahua": ["chihuahua", "ciudad juarez", "cd juarez"],
    "Coahuila": ["coahuila", "saltillo", "torreon"],
    "Colima": ["colima", "manzanillo"],
    "Ciudad de México": [
        "ciudad de mexico", "cdmx", "distrito federal", "df", "mexico df",
        "mexico city",
    ],
    "Durango": ["durango"],
    "Estado de México": [
        "estado de mexico", "edomex", "edo. de mexico", "edo de mexico",
        "ecatepec", "naucalpan", "toluca",
    ],
    "Guanajuato": ["guanajuato", "leon guanajuato", "irapuato"],
    "Guerrero": ["guerrero", "acapulco", "chilpancingo"],
    "Hidalgo": ["hidalgo", "pachuca"],
    "Jalisco": ["jalisco", "guadalajara", "zapopan", "tlaquepaque"],
    "Michoacán": ["michoacan", "morelia", "uruapan"],
    "Morelos": ["morelos", "cuernavaca"],
    "Nayarit": ["nayarit", "tepic"],
    "Nuevo León": [
        "nuevo leon", "monterrey", "san pedro garza garcia", "guadalupe nl",
    ],
    "Oaxaca": ["oaxaca"],
    "Puebla": ["puebla"],
    "Querétaro": ["queretaro"],
    "Quintana Roo": ["quintana roo", "cancun", "playa del carmen", "chetumal"],
    "San Luis Potosí": ["san luis potosi", "slp"],
    "Sinaloa": ["sinaloa", "culiacan", "mazatlan"],
    "Sonora": ["sonora", "hermosillo", "nogales"],
    "Tabasco": ["tabasco", "villahermosa"],
    "Tamaulipas": ["tamaulipas", "tampico", "reynosa", "nuevo laredo"],
    "Tlaxcala": ["tlaxcala"],
    "Veracruz": ["veracruz", "xalapa", "coatzacoalcos"],
    "Yucatán": ["yucatan", "merida"],
    "Zacatecas": ["zacatecas"],
}

_STRIP_PATTERN = re.compile(r"[^a-z0-9\s]")


def _normalize(text: str) -> str:
    # Strip accents first (México -> Mexico) before discarding remaining
    # punctuation, so accented and unaccented input both match the same
    # unaccented aliases. Word-boundary checks below assume tokens are
    # separated by whitespace only.
    decomposed = unicodedata.normalize("NFKD", text.lower())
    without_accents = "".join(c for c in decomposed if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", _STRIP_PATTERN.sub(" ", without_accents)).strip()


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
