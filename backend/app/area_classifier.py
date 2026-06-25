"""Rule-based legal-area classifier.

Searching the full ~7k-article corpus for every query is what causes
irrelevant matches: a question phrased casually shares stray words with
unrelated articles scattered across thousands of candidates. Pre-filtering
to the 1-2 most likely legal areas shrinks the candidate pool by ~10x
before semantic/BM25 ranking even runs, which is the single biggest lever
available without a real LLM doing the reasoning.
"""

import re
from collections import Counter

# Stems, not full words — substring-matched against the normalized query,
# so one entry covers every conjugation/inflection ("despid" matches
# despido, despiden, despida, despidieron, despidió...).
AREA_KEYWORDS: dict[str, list[str]] = {
    "laboral": [
        "trabaj", "patron", "patrón", "despid", "desped",
        "liquidaci", "salari", "sueldo", "imss", "aguinaldo", "vacacion",
        "indemniz", "renunci", "jornada", "sindicat", "antigü", "antigu",
        "finiquit", "incapacidad laboral", "horas extra", "infonavit",
    ],
    "civil": [
        "contrat", "arrendamiento", "renta", "inquilin", "propietari",
        "herenci", "testamento", "sucesi", "deuda", "préstamo", "prestamo",
        "compraventa", "propiedad", "vecin", "condomini", "hipoteca",
        "fianza", "daños y perjuicios",
    ],
    "penal": [
        "delit", "denunci", "robo", "robaron", "asalto", "violaci",
        "abuso", "estupro", "violenci", "amenaza", "fraude", "homicidi",
        "lesion", "secuestr", "ministerio publico", "ministerio público",
        "detenci", "arrest", "carcel", "cárcel", "prision", "prisión",
        "menor de edad", "embaraz", "niñ", "niño", "delincuent",
    ],
    "familiar": [
        "divorci", "pension aliment", "pensión aliment", "aliment",
        "custodia", "patria potestad", "paternidad", "reconocimiento de hijo",
        "adopci", "matrimoni", "concubinat", "violencia familiar",
        "violencia domestica", "violencia doméstica", "guarda y custodia",
    ],
    "mercantil": [
        "empresa", "sociedad", "negocio", "socio", "accionista", "comerciante",
        "factura", "pagare", "pagaré", "quiebra", "concurso mercantil",
        "razon social", "razón social", "marca registrada", "franquicia",
    ],
    "fiscal": [
        "impuesto", "declaraci", "rfc", "factura fiscal", "iva",
        "isr", "multa fiscal", "contribuyente",
    ],
    "constitucional": [
        "constituci", "amparo", "garantias", "garantías",
        "detencion arbitraria", "detención arbitraria", "orden judicial",
    ],
    "derechos_humanos": [
        "datos personales", "privacidad", "discriminaci", "proteccion de datos",
        "protección de datos",
    ],
}

_NORMALIZE_PATTERN = re.compile(r"[^a-záéíóúñü\s]")


def _normalize(text: str) -> str:
    return _NORMALIZE_PATTERN.sub(" ", text.lower())


def classify_areas(query: str, max_areas: int = 2) -> list[str]:
    """Returns up to `max_areas` legal areas ranked by keyword hits.
    Empty list means no area matched confidently — caller should fall back
    to searching the full corpus rather than returning nothing."""
    normalized = _normalize(query)
    hits = Counter()

    for area, keywords in AREA_KEYWORDS.items():
        for kw in keywords:
            if kw in normalized:
                hits[area] += 1

    if not hits:
        return []

    ranked = [area for area, _ in hits.most_common(max_areas)]

    # Family law (alimony, paternity, custody) and commercial law both live
    # inside the same federal codes as "civil" in this corpus (Código Civil
    # Federal / Código de Comercio aren't split by sub-topic) — searching
    # "familiar" or "mercantil" alone misses them entirely.
    if "familiar" in ranked and "civil" not in ranked:
        ranked.append("civil")
    if "mercantil" in ranked and "civil" not in ranked:
        ranked.append("civil")

    return ranked
