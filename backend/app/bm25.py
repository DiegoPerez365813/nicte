"""Minimal BM25 keyword index — no extra heavy dependency (no sklearn/rank_bm25).

Pure semantic search over thousands of real legal articles is noisy: a
small multilingual embedding model often ranks an unrelated article above
the one that actually uses the right legal terms (e.g. "estupro",
"pensión alimenticia"). BM25 catches exact/near-exact term matches that
embeddings miss, and gets combined with semantic similarity in rag.py for
a hybrid score — standard practice for legal/keyword-heavy RAG.
"""

import math
import re
from collections import Counter, defaultdict

_TOKEN_PATTERN = re.compile(r"[a-záéíóúñü]+", re.IGNORECASE)

_SPANISH_STOPWORDS = {
    "el", "la", "los", "las", "de", "del", "en", "y", "a", "que", "un", "una",
    "unos", "unas", "por", "para", "con", "sin", "su", "sus", "se", "es", "al",
    "lo", "le", "les", "como", "más", "o", "u", "este", "esta", "estos",
    "estas", "ese", "esa", "esos", "esas", "cuando", "si", "no", "sí", "ya",
    "ser", "será", "serán", "haber", "han", "ha", "fue", "son", "está",
    "están", "cual", "cuales", "entre", "sobre", "desde", "hasta", "pero",
    "también", "artículo", "ley", "código", "fracción", "fracciones",
    # Common conversational verb forms — frequent in casual user questions,
    # rare (and unrelated in meaning) in formal legal text, which would
    # otherwise inflate their IDF and let an incidental match dominate.
    "qué", "quien", "quién", "porque", "porqué", "donde", "dónde", "mi", "tu",
    "yo", "me", "te", "nos", "les", "soy", "eres", "somos", "puedo", "puede",
    "pueden", "puedes", "podemos", "poder", "pude", "pudo", "tengo", "tiene",
    "tienen", "tienes", "tenemos", "tener", "tuvo", "tuve", "hago", "hace",
    "hacen", "haces", "hacer", "hizo", "quiero", "quiere", "quieren",
    "quieres", "querer", "debo", "debe", "deben", "debes", "deber", "voy",
    "va", "van", "vas", "vamos", "ir", "fui", "fueron", "doy", "da", "dan",
    "das", "dar", "dio", "veo", "ve", "ven", "ves", "ver", "vio", "sé",
    "sabe", "saben", "sabes", "saber", "creo", "cree", "creen", "crees",
    "creer", "pasa", "pasan", "pasas", "pasar", "pasó", "paso", "gracias",
    "hola", "ayuda", "ayudame", "ayúdame", "explica", "explicame", "explícame",
}


def tokenize(text: str) -> list[str]:
    return [
        tok for tok in _TOKEN_PATTERN.findall(text.lower())
        if tok not in _SPANISH_STOPWORDS and len(tok) > 2
    ]


class BM25Index:
    def __init__(self, documents: list[str], k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b

        self._doc_tokens: list[Counter] = []
        self._doc_lengths: list[int] = []
        self._inverted_index: dict[str, list[int]] = defaultdict(list)

        for doc_idx, text in enumerate(documents):
            tokens = tokenize(text)
            counts = Counter(tokens)
            self._doc_tokens.append(counts)
            self._doc_lengths.append(len(tokens))
            for term in counts:
                self._inverted_index[term].append(doc_idx)

        self._n_docs = len(documents)
        self._avg_doc_len = (sum(self._doc_lengths) / self._n_docs) if self._n_docs else 0.0

        self._idf: dict[str, float] = {}
        for term, doc_ids in self._inverted_index.items():
            df = len(doc_ids)
            self._idf[term] = math.log(1 + (self._n_docs - df + 0.5) / (df + 0.5))

    def score(self, query: str) -> dict[int, float]:
        """Returns {doc_idx: bm25_score} only for documents sharing at least
        one query term — sparse by construction, cheap even at thousands
        of documents."""
        query_terms = set(tokenize(query))
        scores: dict[int, float] = defaultdict(float)

        for term in query_terms:
            idf = self._idf.get(term)
            if idf is None:
                continue
            for doc_idx in self._inverted_index[term]:
                tf = self._doc_tokens[doc_idx][term]
                doc_len = self._doc_lengths[doc_idx]
                denom = tf + self.k1 * (1 - self.b + self.b * doc_len / max(self._avg_doc_len, 1e-9))
                scores[doc_idx] += idf * (tf * (self.k1 + 1)) / denom

        return scores
