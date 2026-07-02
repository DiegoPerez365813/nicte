"""Google Sign-In: server-verified identity + signed session cookie.

Uses the ID-token verification flow (no Client Secret): the frontend's
Google Identity Services button hands us a signed ID token, and we verify
it against Google's public keys before trusting any of its claims. That's
the standard, Google-recommended pattern for "who is this user" — a Client
Secret + authorization-code exchange is only needed to call Google APIs on
the user's behalf later, which Nicté doesn't do.

Sessions are a signed, timed cookie (itsdangerous) carrying just the user's
id — no server-side session table needed, matches the article corpus's
Supabase connection pattern (app/db.py) for the `users` table.
"""

import os
import time
import uuid
from typing import Optional

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.db import get_cursor

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
SESSION_COOKIE_NAME = "nicte_session"
_SESSION_MAX_AGE = 60 * 60 * 24 * 30  # 30 days

_serializer: Optional[URLSafeTimedSerializer] = None
_users_table_ready = False


def _get_serializer() -> URLSafeTimedSerializer:
    global _serializer
    if _serializer is None:
        secret = os.environ["SESSION_SECRET"]
        _serializer = URLSafeTimedSerializer(secret, salt="nicte-session")
    return _serializer


def ensure_users_table() -> None:
    """Creates the users table on first use — same lazy pattern as the
    connection pool in app/db.py, so no manual SQL step is required."""
    global _users_table_ready
    if _users_table_ready:
        return
    with get_cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                google_sub TEXT UNIQUE NOT NULL,
                email TEXT,
                name TEXT,
                picture TEXT,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                last_login_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        )
    _users_table_ready = True


def verify_google_credential(credential: str) -> dict:
    """Verifies a Google ID token's signature, audience and issuer against
    Google's public keys. Raises ValueError on any invalid/forged/expired
    token — callers should turn that into a 401."""
    if not GOOGLE_CLIENT_ID:
        raise ValueError("GOOGLE_CLIENT_ID is not configured")
    try:
        claims = id_token.verify_oauth2_token(
            credential, google_requests.Request(), GOOGLE_CLIENT_ID
        )
    except Exception as exc:
        raise ValueError(f"Invalid Google credential: {exc}") from exc

    if claims.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
        raise ValueError("Invalid token issuer")
    return claims


def upsert_user(google_sub: str, email: str | None, name: str | None, picture: str | None) -> dict:
    ensure_users_table()
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO users (google_sub, email, name, picture)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (google_sub) DO UPDATE
                SET email = EXCLUDED.email,
                    name = EXCLUDED.name,
                    picture = EXCLUDED.picture,
                    last_login_at = now()
            RETURNING id, email, name, picture
            """,
            (google_sub, email, name, picture),
        )
        row = cur.fetchone()
    return {"id": str(row[0]), "email": row[1], "name": row[2], "picture": row[3]}


def get_user_by_id(user_id: str) -> dict | None:
    ensure_users_table()
    with get_cursor() as cur:
        cur.execute(
            "SELECT id, email, name, picture FROM users WHERE id = %s",
            (user_id,),
        )
        row = cur.fetchone()
    if not row:
        return None
    return {"id": str(row[0]), "email": row[1], "name": row[2], "picture": row[3]}


def create_session_token(user_id: str) -> str:
    return _get_serializer().dumps({"uid": user_id})


def read_session_token(token: str) -> str | None:
    """Returns the user id encoded in a session token, or None if the token
    is missing, forged, or older than _SESSION_MAX_AGE."""
    if not token:
        return None
    try:
        data = _get_serializer().loads(token, max_age=_SESSION_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None
    return data.get("uid")
