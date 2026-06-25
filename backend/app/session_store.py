"""In-memory session state — process-local, not persisted.

Tracks whether a session is mid-triage (waiting on the user's answer to
clarifying questions) and the original message that triggered it, so the
next turn can combine both into one specific query. Swap for Redis before
running more than one backend instance.
"""

_sessions: dict[str, dict] = {}


def get_session(session_id: str) -> dict:
    return _sessions.setdefault(session_id, {"awaiting_clarification": False, "original_message": None})


def start_clarification(session_id: str, original_message: str) -> None:
    _sessions[session_id] = {"awaiting_clarification": True, "original_message": original_message}


def resolve_clarification(session_id: str) -> str | None:
    """Clears the pending flag and returns the stored original message,
    or None if this session wasn't awaiting clarification."""
    session = _sessions.get(session_id)
    if not session or not session.get("awaiting_clarification"):
        return None
    original = session["original_message"]
    _sessions[session_id] = {"awaiting_clarification": False, "original_message": None}
    return original
