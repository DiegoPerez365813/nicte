"""Minimal RAG retrieval layer.

For this proof-of-concept slice, the vector index lives in memory
(numpy cosine similarity) instead of pgvector — same retrieval contract,
swappable backend later without touching callers.
"""

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from app.area_classifier import classify_areas
from app.bm25 import BM25Index

_CACHE_DIR = Path(__file__).parent / "data" / "embeddings_cache"

from app.legal_corpus.civil import CIVIL_CORPUS
from app.legal_corpus.familiar import FAMILIAR_CORPUS
from app.legal_corpus.laboral import LABORAL_CORPUS
from app.legal_corpus.penal import PENAL_CORPUS

_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"  # decent ES coverage, small

_PROCESSED_DIR = Path(__file__).parent / "data" / "processed"

HAND_CURATED_CORPORA = [*LABORAL_CORPUS, *CIVIL_CORPUS, *PENAL_CORPUS, *FAMILIAR_CORPUS]


def _load_ingested_corpora() -> list[dict]:
    """Loads every law ingested by app/ingest.py (full official text, auto
    -extracted per article). Falls back to the small hand-curated corpus
    for any law that hasn't been ingested yet, so the API never has zero
    coverage for a given area."""
    if not _PROCESSED_DIR.exists():
        return HAND_CURATED_CORPORA

    chunks: list[dict] = []
    ingested_codes: set[str] = set()
    for json_path in sorted(_PROCESSED_DIR.glob("*.json")):
        try:
            docs = json.loads(json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if docs:
            chunks.extend(docs)
            ingested_codes.add(json_path.stem)

    if not chunks:
        return HAND_CURATED_CORPORA

    # Hand-curated entries stay as a safety net only for laws not yet ingested.
    ingested_law_names = {c["law_name"] for c in chunks}
    for fallback in HAND_CURATED_CORPORA:
        if fallback["law_name"] not in ingested_law_names:
            chunks.append(fallback)

    return chunks


ALL_CORPORA = _load_ingested_corpora()

# Fixed catalog of constitutional defense/due-process rights — these don't
# change per query, so they're looked up directly by article number instead
# of through similarity search (which would be noisy for a "find me my
# rights" intent). Each entry pairs a real ingested article with a
# hand-written plain-language summary, since CPEUM Art. 20 in particular is
# long and dense — quoting it raw isn't "comprensible" on its own.
DEFENSE_ARTICLES: list[dict] = [
    {
        "law_name": "Constitución Política de los Estados Unidos Mexicanos",
        "article_number": "20",
        "plain_summary": (
            "Se presume tu inocencia hasta que se demuestre lo contrario. Tienes "
            "derecho a no declarar contra ti mismo, a que se te informe de qué se "
            "te acusa, a tener un defensor (público o privado) desde el primer "
            "momento, y a que el proceso sea público y con pruebas presentadas "
            "ante un juez."
        ),
    },
    {
        "law_name": "Constitución Política de los Estados Unidos Mexicanos",
        "article_number": "19",
        "plain_summary": (
            "Nadie puede mantenerte detenido más de 72 horas sin que un juez "
            "determine, con base en pruebas, si existen elementos suficientes "
            "para procesarte (auto de vinculación a proceso)."
        ),
    },
    {
        "law_name": "Constitución Política de los Estados Unidos Mexicanos",
        "article_number": "17",
        "plain_summary": (
            "Tienes derecho a que se te administre justicia de forma gratuita, "
            "pronta y completa por tribunales — nadie puede impedirte acceder a "
            "ellos ni cobrarte por ese acceso."
        ),
    },
]


@dataclass
class RetrievedChunk:
    id: str
    law_name: str
    article_number: str
    jurisdiction: str
    source_url: str
    text: str
    area: str
    score: float
    plain_summary: str | None = None


def _corpus_fingerprint(texts: list[str]) -> str:
    digest = hashlib.sha256()
    for text in texts:
        digest.update(text.encode("utf-8"))
        digest.update(b"\x00")
    return digest.hexdigest()


class LegalRetriever:
    def __init__(self) -> None:
        self._model = SentenceTransformer(_MODEL_NAME)
        self._corpus = ALL_CORPORA
        texts = [doc["text"] for doc in self._corpus]
        self._embeddings = self._load_or_build_embeddings(texts)
        self._bm25 = BM25Index(texts)
        self._area_indices: dict[str, np.ndarray] = {}
        for area in {doc["area"] for doc in self._corpus}:
            self._area_indices[area] = np.array(
                [i for i, doc in enumerate(self._corpus) if doc["area"] == area]
            )
        self._by_law_and_article: dict[tuple[str, str], dict] = {
            (doc["law_name"], doc["article_number"]): doc for doc in self._corpus
        }

    def get_defense_articles(self) -> list[RetrievedChunk]:
        """Fixed set of constitutional due-process/defense-rights articles,
        each carrying a hand-written plain-language summary. Looked up by
        article number rather than similarity search."""
        results = []
        for entry in DEFENSE_ARTICLES:
            doc = self._by_law_and_article.get((entry["law_name"], entry["article_number"]))
            if doc is None:
                continue
            results.append(
                RetrievedChunk(
                    id=doc["id"],
                    law_name=doc["law_name"],
                    article_number=doc["article_number"],
                    jurisdiction=doc["jurisdiction"],
                    source_url=doc["source_url"],
                    text=doc["text"],
                    area=doc["area"],
                    score=1.0,
                    plain_summary=entry["plain_summary"],
                )
            )
        return results

    def _load_or_build_embeddings(self, texts: list[str]) -> np.ndarray:
        # Re-embedding ~7k articles takes several minutes on CPU. Cache the
        # result keyed by a hash of the corpus text so dev restarts (and
        # prod redeploys with an unchanged corpus) skip straight to a
        # disk load instead of recomputing every vector from scratch.
        fingerprint = _corpus_fingerprint(texts)
        cache_path = _CACHE_DIR / f"{fingerprint}.npy"

        if cache_path.exists():
            return np.load(cache_path)

        embeddings = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        for stale in _CACHE_DIR.glob("*.npy"):
            stale.unlink(missing_ok=True)
        np.save(cache_path, embeddings)

        return embeddings

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        min_score: float = 0.3,
        semantic_weight: float = 0.7,
    ) -> list[RetrievedChunk]:
        query_vec = self._model.encode([query], normalize_embeddings=True)[0]
        semantic_scores = self._embeddings @ query_vec  # cosine sim (vectors normalized)

        bm25_raw = self._bm25.score(query)
        bm25_scores = np.zeros(len(self._corpus))
        if bm25_raw:
            max_bm25 = max(bm25_raw.values())
            for doc_idx, raw_score in bm25_raw.items():
                bm25_scores[doc_idx] = raw_score / max_bm25  # normalize to [0, 1]

        # Hybrid score: dense embeddings catch paraphrase/concept matches,
        # BM25 catches exact legal terminology embeddings tend to miss
        # ("estupro", "pensión alimenticia") once the corpus has thousands
        # of distractor articles.
        combined_scores = semantic_weight * semantic_scores + (1 - semantic_weight) * bm25_scores

        # Pre-filter to the 1-2 legal areas the query is likely about. This
        # is the main lever against irrelevant matches: searching all ~7k
        # articles lets stray shared words (e.g. "pasa") from completely
        # unrelated areas outrank the genuinely relevant one. If no area
        # matches confidently, fall back to the full corpus.
        likely_areas = classify_areas(query)
        if likely_areas:
            allowed = np.concatenate([self._area_indices[a] for a in likely_areas if a in self._area_indices])
            mask = np.full(len(self._corpus), False)
            mask[allowed] = True
            combined_scores = np.where(mask, combined_scores, -np.inf)

        ranked_idx = np.argsort(combined_scores)[::-1][:top_k]

        results = []
        for idx in ranked_idx:
            score = float(combined_scores[idx])
            if score < min_score:
                continue
            doc = self._corpus[idx]
            results.append(
                RetrievedChunk(
                    id=doc["id"],
                    law_name=doc["law_name"],
                    article_number=doc["article_number"],
                    jurisdiction=doc["jurisdiction"],
                    source_url=doc["source_url"],
                    text=doc["text"],
                    area=doc["area"],
                    score=score,
                )
            )
        return results


_retriever: LegalRetriever | None = None


def get_retriever() -> LegalRetriever:
    global _retriever
    if _retriever is None:
        _retriever = LegalRetriever()
    return _retriever
