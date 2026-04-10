from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ── Auth ──────────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict


# ── Analysis ──────────────────────────────────────────────────────────────────

class RedFlag(BaseModel):
    title: str
    description: str
    severity: str  # high | medium | low


class SimilarCase(BaseModel):
    type: str  # court_settlement | similar_agreement | ignored_clause | helpful_info
    title: str
    description: str
    relevance: str


class AnalysisResult(BaseModel):
    summary: str
    red_flags: List[RedFlag]
    similar_cases: List[SimilarCase]
