"""RAG retrieval layer backed by Supabase + pgvector.

Retrieval strategy:
  1. Encode query with sentence-transformers (384-dim, normalized).
  2. Fetch top-200 candidates from Supabase using cosine similarity,
     pre-filtered by jurisdiction (state → federal fallback).
  3. Re-rank candidates with BM25 on their texts (catches exact legal
     terms that embeddings may miss).
  4. Return top-k above min_score threshold.

Cold-start is ~30 s (model load) — no corpus or embedding build needed.
"""

from __future__ import annotations

import math
import re
from collections import defaultdict
from dataclasses import dataclass

import numpy as np

from app.area_classifier import classify_areas
from app.db import get_cursor
from app.embeddings import embed_query

# Constitutional defense articles shown verbatim (looked up by law+article).
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


# ---------------------------------------------------------------------------
# Minimal BM25 used for re-ranking a small candidate set from pgvector
# ---------------------------------------------------------------------------

_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


class _BM25Reranker:
    """BM25 over a small candidate set (not the full corpus)."""

    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75) -> None:
        self._k1 = k1
        self._b = b
        tokenized = [_tokenize(d) for d in docs]
        self._n = len(tokenized)
        avgdl = sum(len(t) for t in tokenized) / max(self._n, 1)
        self._avgdl = avgdl
        self._dl = [len(t) for t in tokenized]
        df: dict[str, int] = defaultdict(int)
        self._tf: list[dict[str, int]] = []
        for tokens in tokenized:
            freq: dict[str, int] = defaultdict(int)
            for tok in tokens:
                freq[tok] += 1
            self._tf.append(dict(freq))
            for tok in set(tokens):
                df[tok] += 1
        self._idf: dict[str, float] = {
            tok: math.log((self._n - cnt + 0.5) / (cnt + 0.5) + 1)
            for tok, cnt in df.items()
        }

    def score(self, query: str) -> np.ndarray:
        query_tokens = _tokenize(query)
        scores = np.zeros(self._n)
        for tok in query_tokens:
            if tok not in self._idf:
                continue
            idf = self._idf[tok]
            for i, (tf, dl) in enumerate(zip(self._tf, self._dl)):
                f = tf.get(tok, 0)
                denom = f + self._k1 * (1 - self._b + self._b * dl / self._avgdl)
                scores[i] += idf * f * (self._k1 + 1) / denom
        return scores


# ---------------------------------------------------------------------------

def _vec_literal(arr: np.ndarray) -> str:
    return "[" + ",".join(f"{x:.6f}" for x in arr.tolist()) + "]"


def _fetch_candidates(
    query_vec: np.ndarray,
    state: str | None,
    areas: list[str],
    limit: int = 200,
) -> list[dict]:
    """Query Supabase for top-`limit` candidates, pre-filtered by jurisdiction."""
    vec = _vec_literal(query_vec)
    area_filter = "AND area = ANY(%s)" if areas else ""
    area_params: list = [areas] if areas else []

    rows: list[dict] = []

    with get_cursor() as cur:
        if state is not None:
            # Try state-specific first
            cur.execute(
                f"""
                SELECT id, law_name, jurisdiction, article_number, text,
                       area, source_url,
                       1 - (embedding <=> %s::vector) AS similarity
                FROM articles
                WHERE jurisdiction = %s {area_filter}
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                [vec, state, *area_params, vec, limit],
            )
            rows = [
                dict(zip(
                    ("id", "law_name", "jurisdiction", "article_number",
                     "text", "area", "source_url", "similarity"),
                    row,
                ))
                for row in cur.fetchall()
            ]

        if not rows or (state is not None and not any(r["similarity"] >= 0.3 for r in rows)):
            # Fall back to federal-only
            cur.execute(
                f"""
                SELECT id, law_name, jurisdiction, article_number, text,
                       area, source_url,
                       1 - (embedding <=> %s::vector) AS similarity
                FROM articles
                WHERE is_federal = true {area_filter}
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                [vec, *area_params, vec, limit],
            )
            rows = [
                dict(zip(
                    ("id", "law_name", "jurisdiction", "article_number",
                     "text", "area", "source_url", "similarity"),
                    row,
                ))
                for row in cur.fetchall()
            ]

    return rows


class LegalRetriever:
    def __init__(self) -> None:
        pass  # no local model — embeddings via OpenAI API

    def get_defense_articles(self) -> list[RetrievedChunk]:
        results = []
        with get_cursor() as cur:
            for entry in DEFENSE_ARTICLES:
                cur.execute(
                    "SELECT id, law_name, jurisdiction, article_number, "
                    "text, area, source_url FROM articles "
                    "WHERE law_name = %s AND article_number = %s LIMIT 1",
                    (entry["law_name"], entry["article_number"]),
                )
                row = cur.fetchone()
                if row is None:
                    continue
                results.append(
                    RetrievedChunk(
                        id=row[0],
                        law_name=row[1],
                        jurisdiction=row[2],
                        article_number=row[3],
                        text=row[4],
                        area=row[5],
                        source_url=row[6],
                        score=1.0,
                        plain_summary=entry["plain_summary"],
                    )
                )
        return results

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        min_score: float = 0.3,
        semantic_weight: float = 0.7,
        state: str | None = None,
    ) -> list[RetrievedChunk]:
        query_vec = embed_query(query)

        areas = classify_areas(query)
        candidates = _fetch_candidates(query_vec, state, areas)

        if not candidates:
            return []

        texts = [c["text"] for c in candidates]
        sem_scores = np.array([c["similarity"] for c in candidates], dtype=float)

        bm25 = _BM25Reranker(texts)
        bm25_raw = bm25.score(query)
        max_bm25 = bm25_raw.max()
        bm25_scores = bm25_raw / max_bm25 if max_bm25 > 0 else bm25_raw

        combined = semantic_weight * sem_scores + (1 - semantic_weight) * bm25_scores

        ranked_idx = np.argsort(combined)[::-1]

        results = []
        for idx in ranked_idx:
            if float(combined[idx]) < min_score:
                break
            if len(results) >= top_k:
                break
            c = candidates[idx]
            results.append(
                RetrievedChunk(
                    id=c["id"],
                    law_name=c["law_name"],
                    jurisdiction=c["jurisdiction"],
                    article_number=c["article_number"],
                    text=c["text"],
                    area=c["area"],
                    source_url=c["source_url"],
                    score=float(combined[idx]),
                )
            )
        return results


_retriever: LegalRetriever | None = None


def get_retriever() -> LegalRetriever:
    global _retriever
    if _retriever is None:
        _retriever = LegalRetriever()
    return _retriever
