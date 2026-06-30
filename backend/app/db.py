"""Supabase / PostgreSQL connection pool (psycopg2).

Expects the env var SUPABASE_DB_URL with a full postgres:// connection string,
e.g. the "Transaction" pooler URL from Supabase dashboard → Settings → Database.

The DSN is parsed manually (not handed to psycopg2 as a URI) because
database passwords routinely contain characters like "!" that are valid
in a password but break naive URI parsing if not percent-encoded.

The pool is created once at module import and reused across requests.
"""

import os
import re
from contextlib import contextmanager
from typing import Generator

import psycopg2
import psycopg2.pool
from dotenv import load_dotenv

load_dotenv()

_DSN_RE = re.compile(
    r"^postgresql(?:\+\w+)?://(?P<user>[^:/@]+):(?P<password>.+)@(?P<host>[^:/@]+):(?P<port>\d+)/(?P<dbname>[^?]+)"
)


def _parse_dsn(url: str) -> dict:
    match = _DSN_RE.match(url)
    if not match:
        raise ValueError(
            "SUPABASE_DB_URL must look like "
            "postgresql://user:password@host:port/dbname"
        )
    return match.groupdict()


_DB_PARAMS = _parse_dsn(os.environ["SUPABASE_DB_URL"])

_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    host=_DB_PARAMS["host"],
    port=_DB_PARAMS["port"],
    dbname=_DB_PARAMS["dbname"],
    user=_DB_PARAMS["user"],
    password=_DB_PARAMS["password"],
)


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
