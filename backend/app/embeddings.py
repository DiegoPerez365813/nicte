"""Voyage AI embeddings client — replaces sentence-transformers.

Uses voyage-law-2 (1024 dims, trained on legal documents).
Free tier: 200M tokens/month.
"""

import os
import time

import numpy as np
import voyageai

_MODEL = "voyage-law-2"
_DIMS = 1024
_BATCH = 128  # Voyage AI max per request

_client: voyageai.Client | None = None


def _get_client() -> voyageai.Client:
    global _client
    if _client is None:
        _client = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])
    return _client


def embed_texts(texts: list[str], show_progress: bool = False) -> np.ndarray:
    """Embed a list of texts, returning a (N, 1024) float32 array."""
    client = _get_client()
    results: list[list[float]] = []
    total = len(texts)
    for start in range(0, total, _BATCH):
        batch = texts[start : start + _BATCH]
        retries = 0
        while True:
            try:
                resp = client.embed(batch, model=_MODEL, input_type="document")
                results.extend(resp.embeddings)
                break
            except Exception as exc:
                msg = str(exc).lower()
                transient = any(k in msg for k in ("rate", "connection", "timeout", "reset", "502", "503", "529"))
                if transient and retries < 6:
                    retries += 1
                    time.sleep(5 * retries)
                else:
                    raise
        if show_progress:
            done = min(start + _BATCH, total)
            print(f"  {done}/{total} ({done/total*100:.1f}%)", end="\r", flush=True)
    if show_progress:
        print()
    arr = np.array(results, dtype=np.float32)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return arr / np.where(norms == 0, 1, norms)


def embed_query(text: str) -> np.ndarray:
    """Embed a single query string, returning a (1024,) float32 array."""
    client = _get_client()
    retries = 0
    while True:
        try:
            resp = client.embed([text], model=_MODEL, input_type="query")
            arr = np.array(resp.embeddings[0], dtype=np.float32)
            norm = np.linalg.norm(arr)
            return arr / norm if norm > 0 else arr
        except Exception as exc:
            msg = str(exc).lower()
            transient = any(k in msg for k in ("rate", "connection", "timeout", "reset", "502", "503", "529"))
            if transient and retries < 6:
                retries += 1
                time.sleep(5 * retries)
            else:
                raise
