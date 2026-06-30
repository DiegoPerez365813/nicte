"""Supabase / PostgreSQL connection pool (psycopg2).

Expects the env var SUPABASE_DB_URL with a full postgres:// connection string,
e.g. the "Transaction" pooler URL from Supabase dashboard → Settings → Database.

The pool is created once at module import and reused across requests.
"""

import os
from contextlib import contextmanager
from typing import Generator

import psycopg2
import psycopg2.pool
from dotenv import load_dotenv

load_dotenv()

_DB_URL = os.environ["SUPABASE_DB_URL"]

_pool = psycopg2.pool.ThreadedConnectionPool(minconn=1, maxconn=10, dsn=_DB_URL)


@contextmanager
def get_cursor() -> Generator[psycopg2.extensions.cursor, None, None]:
    conn = _pool.getconn()
    try:
        with conn.cursor() as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)
