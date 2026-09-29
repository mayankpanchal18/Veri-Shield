from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(30), default="submitter", index=True)
    password_hash: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Screening(Base):
    __tablename__ = "screenings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    submitter_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    reviewer_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    filename: Mapped[str] = mapped_column(String(255))
    mime_type: Mapped[str] = mapped_column(String(100))
    document_hash: Mapped[str] = mapped_column(String(64), index=True)
    evidence_path: Mapped[str] = mapped_column(Text)

    document_type: Mapped[str] = mapped_column(String(120), default="Unknown")
    ocr_text: Mapped[str] = mapped_column(Text, default="")
    ocr_fields: Mapped[dict] = mapped_column(JSON, default=dict)
    extracted_fields: Mapped[dict] = mapped_column(JSON, default=dict)
    forensics: Mapped[dict] = mapped_column(JSON, default=dict)
    ai_review: Mapped[dict] = mapped_column(JSON, default=dict)

    deterministic_risk: Mapped[int] = mapped_column(Integer, default=0)
    risk_score: Mapped[int] = mapped_column(Integer, default=0)
    risk_level: Mapped[str] = mapped_column(String(20), default="Low")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

    status: Mapped[str] = mapped_column(String(40), default="PENDING_REVIEW", index=True)
    reviewer_decision: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    reviewer_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)

    submitter = relationship("User", foreign_keys=[submitter_id])
    reviewer = relationship("User", foreign_keys=[reviewer_id])


class VerificationEvent(Base):
    __tablename__ = "verification_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    screening_id: Mapped[int] = mapped_column(ForeignKey("screenings.id", ondelete="CASCADE"), index=True)
    document_hash: Mapped[str] = mapped_column(String(64), index=True)
    action: Mapped[str] = mapped_column(String(60))
    actor_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    previous_event_hash: Mapped[str] = mapped_column(String(64), default="0" * 64)
    event_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    blockchain_tx: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
