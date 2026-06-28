"""In-memory session state — process-local, not persisted.

Tracks whether a session is mid-triage (waiting on the user's answer to
clarifying questions) and the original message that triggered it, so the
next turn can combine both into one specific query. Swap for Redis before
running more than one backend instance.
"""

_sessions: dict[str, dict] = {}

_DEFAULTS = {"awaiting_clarification": False, "original_message": None, "state": None}


def get_session(session_id: str) -> dict:
    return _sessions.setdefault(session_id, dict(_DEFAULTS))


def start_clarification(session_id: str, original_message: str) -> None:
    session = get_session(session_id)
    session["awaiting_clarification"] = True
    session["original_message"] = original_message


def resolve_clarification(session_id: str) -> str | None:
    """Clears the pending flag and returns the stored original message,
    or None if this session wasn't awaiting clarification. Does not touch
    the remembered state — that persists for the rest of the session."""
    session = _sessions.get(session_id)
    if not session or not session.get("awaiting_clarification"):
        return None
    original = session["original_message"]
    session["awaiting_clarification"] = False
    session["original_message"] = None
    return original


def get_state(session_id: str) -> str | None:
    return get_session(session_id).get("state")


def set_state(session_id: str, state: str) -> None:
    get_session(session_id)["state"] = state
