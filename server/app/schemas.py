from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ReviewDecisionRequest(BaseModel):
    decision: Literal["VALID", "INVALID", "NEEDS_MORE_EVIDENCE"]
    note: str = Field(default="", max_length=2000)


class PublicVerifyRequest(BaseModel):
    document_hash: str = Field(min_length=64, max_length=64)


class GeminiFields(BaseModel):
    full_name: str = ""
    date_of_birth: str = ""
    document_number: str = ""
    issue_date: str = ""
    expiry_date: str = ""
    issuing_authority: str = ""
    issuing_country: str = ""
    address: str = ""
    document_type: str = "Unknown"


class GeminiCheck(BaseModel):
    name: str
    status: Literal["PASS", "WARN", "FAIL", "UNKNOWN"]
    details: str


class GeminiReview(BaseModel):
    fields: GeminiFields
    checks: list[GeminiCheck]
    suspicious_signals: list[str]
    risk_score: int = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    reviewer_summary: str
    recommended_focus: list[str]
    limitations: str
