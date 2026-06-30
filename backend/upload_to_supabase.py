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
        embedding   vector(1024)
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
import re
import sys
from pathlib import Path

import numpy as np
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Add app/ to path so we can import embeddings module
sys.path.insert(0, str(Path(__file__).parent))
from app.embeddings import embed_texts  # noqa: E402

_PROCESSED_DIR = Path(__file__).parent / "app" / "data" / "processed"
_DB_BATCH = 500

# Parsed manually instead of handed to psycopg2 as a URI — passwords with
# characters like "!" break naive URI parsing unless percent-encoded.
_DSN_RE = re.compile(
    r"^postgresql(?:\+\w+)?://(?P<user>[^:/@]+):(?P<password>.+)@(?P<host>[^:/@]+):(?P<port>\d+)/(?P<dbname>[^?]+)"
)


def _parse_dsn(url: str) -> dict:
    match = _DSN_RE.match(url)
    if not match:
        raise ValueError(
            "SUPABASE_DB_URL must look like postgresql://user:password@host:port/dbname"
        )
    return match.groupdict()


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

    texts = [doc["text"] for doc in corpus]
    cache_path = Path(__file__).parent / "_upload_embeddings_cache.npy"
    if cache_path.exists():
        cached = np.load(cache_path)
        if cached.shape[1] == 1024:
            print(f"Loading cached embeddings from {cache_path.name}…")
            embeddings = cached
        else:
            print("Cache is from old model (384 dims), re-encoding with OpenAI…")
            cache_path.unlink()
            embeddings = None
    else:
        embeddings = None

    if embeddings is None:
        print(f"Encoding {len(texts)} texts via OpenAI API…")
        embeddings = embed_texts(texts, show_progress=True)
        np.save(cache_path, embeddings)

    print("Connecting to Supabase…")
    db_params = _parse_dsn(db_url)
    conn = psycopg2.connect(
        host=db_params["host"],
        port=db_params["port"],
        dbname=db_params["dbname"],
        user=db_params["user"],
        password=db_params["password"],
    )
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
