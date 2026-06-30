"""One-time script: encode all 97k articles and upsert into Supabase.

Run from the backend/ directory:
    python upload_to_supabase.py

Requires SUPABASE_DB_URL in backend/.env (the postgres:// URL from Supabase
dashboard → Settings → Database → Connection String → URI, using the
"Transaction" pooler or direct connection).

The SQL schema to create first in Supabase SQL editor:

    CREATE EXTENSION IF NOT EXISTS vector;

    CREATE TABLE IF NOT EXISTS articles (
        id          TEXT PRIMARY KEY,
        code        TEXT NOT NULL,
        law_name    TEXT NOT NULL,
        jurisdiction TEXT NOT NULL,
        is_federal  BOOLEAN NOT NULL,
        article_number TEXT NOT NULL,
        text        TEXT NOT NULL,
        area        TEXT NOT NULL,
        source_url  TEXT NOT NULL DEFAULT '',
        embedding   vector(384)
    );

    CREATE INDEX IF NOT EXISTS articles_embedding_idx
        ON articles USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);

    CREATE INDEX IF NOT EXISTS articles_jurisdiction_idx
        ON articles (jurisdiction);

    CREATE INDEX IF NOT EXISTS articles_is_federal_idx
        ON articles (is_federal);
"""

import json
import os
import sys
from pathlib import Path

import numpy as np
import psycopg2
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

_PROCESSED_DIR = Path(__file__).parent / "app" / "data" / "processed"
_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
_BATCH_SIZE = 256
_DB_BATCH = 500


def _load_corpus() -> list[dict]:
    chunks = []
    for json_path in sorted(_PROCESSED_DIR.glob("*.json")):
        try:
            docs = json.loads(json_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        chunks.extend(docs)
    return chunks


def _vec_literal(arr: np.ndarray) -> str:
    return "[" + ",".join(f"{x:.6f}" for x in arr.tolist()) + "]"


def main() -> None:
    db_url = os.environ.get("SUPABASE_DB_URL")
    if not db_url:
        sys.exit("Error: SUPABASE_DB_URL not set in .env")

    print("Loading corpus…")
    corpus = _load_corpus()
    print(f"  {len(corpus)} articles loaded")

    print("Loading sentence-transformer model…")
    model = SentenceTransformer(_MODEL_NAME)

    texts = [doc["text"] for doc in corpus]
    print(f"Encoding {len(texts)} texts in batches of {_BATCH_SIZE}…")
    embeddings = model.encode(
        texts,
        batch_size=_BATCH_SIZE,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    print("Connecting to Supabase…")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    sql = """
        INSERT INTO articles
            (id, code, law_name, jurisdiction, is_federal,
             article_number, text, area, source_url, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s::vector)
        ON CONFLICT (id) DO UPDATE SET
            embedding = EXCLUDED.embedding,
            text      = EXCLUDED.text;
    """

    total = len(corpus)
    uploaded = 0
    for start in range(0, total, _DB_BATCH):
        batch_docs = corpus[start : start + _DB_BATCH]
        batch_embs = embeddings[start : start + _DB_BATCH]
        rows = []
        for doc, emb in zip(batch_docs, batch_embs):
            rows.append((
                doc["id"],
                doc.get("code", ""),
                doc["law_name"],
                doc["jurisdiction"],
                doc["jurisdiction"] == "federal",
                doc["article_number"],
                doc["text"],
                doc["area"],
                doc.get("source_url", ""),
                _vec_literal(emb),
            ))
        cur.executemany(sql, rows)
        conn.commit()
        uploaded += len(rows)
        pct = uploaded / total * 100
        print(f"  {uploaded}/{total} ({pct:.1f}%)", end="\r", flush=True)

    cur.close()
    conn.close()
    print(f"\nDone — {uploaded} articles uploaded.")


if __name__ == "__main__":
    main()
