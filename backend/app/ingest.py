"""Ingestion pipeline: download official Mexican legal PDFs, extract every
article automatically, and write them as structured JSON chunks the RAG
retriever can load.

This replaces hand-curated corpus files (app/legal_corpus/*.py, ~20
paraphrased articles) with the full, official text of each law (thousands
of articles), sourced directly from diputados.gob.mx (DOF-published PDFs).

Run manually (re-run when laws are amended):

    python -m app.ingest

Output: app/data/processed/{code}.json — one file per law, each a list of
chunk dicts with the same shape as app/legal_corpus/*.py entries, so the
retriever can merge both formats transparently.
"""

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import httpx
from pypdf import PdfReader

BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

BOILERPLATE_PATTERNS = [
    r"Cámara de Diputados del H\. Congreso de la Unión",
    r"Secretaría General",
    r"Secretaría de Servicios Parlamentarios",
    r"Última Reforma DOF.*",
    r"^\d{1,4}\s*$",  # bare page numbers
    r"LeyesBiblio",
]


@dataclass
class LawSource:
    code: str
    law_name: str
    area: str
    jurisdiction: str
    url: str


SOURCES: list[LawSource] = [
    LawSource("CPEUM", "Constitución Política de los Estados Unidos Mexicanos", "constitucional", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/CPEUM.pdf"),
    LawSource("LFT", "Ley Federal del Trabajo", "laboral", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf"),
    LawSource("CCF", "Código Civil Federal", "civil", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/CCF.pdf"),
    LawSource("CPF", "Código Penal Federal", "penal", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/CPF.pdf"),
    LawSource("CCO", "Código de Comercio", "mercantil", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/CCom.pdf"),
    LawSource("CFF", "Código Fiscal de la Federación", "fiscal", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/CFF.pdf"),
    LawSource("LGAMVLV", "Ley General de Acceso de las Mujeres a una Vida Libre de Violencia", "familiar", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/LGAMVLV.pdf"),
    LawSource("LFPDPPP", "Ley Federal de Protección de Datos Personales en Posesión de los Particulares",
               "derechos_humanos", "federal",
               "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf"),
]

ARTICLE_PATTERN = re.compile(
    r"Art[íi]culo\s+(\d+(?:\s*(?:Bis|Ter|Qu[aá]ter|Quinquies)\b)?(?:[-–]\w+)?)\s*[.\-–]",
    re.IGNORECASE,
)


def download_pdf(source: LawSource) -> Path:
    raw_path = RAW_DIR / f"{source.code}.pdf"
    if raw_path.exists():
        return raw_path

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with httpx.Client(follow_redirects=True, timeout=60) as client:
        resp = client.get(source.url, headers={"User-Agent": "Mozilla/5.0 (Nicte-Ingest/0.1)"})
        resp.raise_for_status()
        raw_path.write_bytes(resp.content)
    return raw_path


def extract_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages_text = []
    for page in reader.pages:
        text = page.extract_text() or ""
        lines = text.split("\n")
        cleaned_lines = [
            line for line in lines
            if not any(re.search(p, line) for p in BOILERPLATE_PATTERNS)
        ]
        pages_text.append(" ".join(cleaned_lines))
    full_text = " ".join(pages_text)
    return re.sub(r"\s+", " ", full_text).strip()


def split_into_articles(full_text: str, max_chars: int = 1800) -> list[tuple[str, str]]:
    matches = list(ARTICLE_PATTERN.finditer(full_text))
    articles = []
    for i, match in enumerate(matches):
        article_number = match.group(1).strip()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        body = full_text[start:end].strip()
        if len(body) > max_chars:
            body = body[:max_chars].rstrip() + "..."
        if len(body) < 20:  # noise / false-positive match
            continue
        articles.append((article_number, body))
    return articles


def build_chunks(source: LawSource, articles: list[tuple[str, str]]) -> list[dict]:
    today = date.today().isoformat()
    chunks = []
    seen_numbers: set[str] = set()
    for article_number, text in articles:
        dedup_key = f"{article_number}"
        if dedup_key in seen_numbers:
            continue
        seen_numbers.add(dedup_key)
        chunks.append({
            "id": f"{source.code.lower()}-art-{article_number}".replace(" ", "-"),
            "law_name": source.law_name,
            "jurisdiction": source.jurisdiction,
            "article_number": article_number,
            "effective_date": today,
            "source_url": source.url,
            "area": source.area,
            "text": text,
        })
    return chunks


def ingest_source(source: LawSource) -> int:
    pdf_path = download_pdf(source)
    full_text = extract_text(pdf_path)
    articles = split_into_articles(full_text)
    chunks = build_chunks(source, articles)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / f"{source.code}.json"
    out_path.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(chunks)


def main() -> None:
    for source in SOURCES:
        try:
            count = ingest_source(source)
            print(f"[OK] {source.code} ({source.law_name}) -> {count} artículos")
        except Exception as exc:  # noqa: BLE001 — one bad source must not stop the rest
            print(f"[FAIL] {source.code}: {exc}")


if __name__ == "__main__":
    main()
