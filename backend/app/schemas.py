from typing import Literal, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None


class Citation(BaseModel):
    law_name: str
    article_number: str
    jurisdiction: str
    source_url: str
    relevance_score: float
    kind: Literal["fundamento", "defensa"] = "fundamento"
    plain_summary: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    citations: list[Citation]
    legal_area: str
    safety_flag: Optional[Literal["emergency", "out_of_scope", "low_confidence"]] = None


class GoogleSignInRequest(BaseModel):
    credential: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None
