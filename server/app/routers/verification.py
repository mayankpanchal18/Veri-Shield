from __future__ import annotations

import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Screening, VerificationEvent

router = APIRouter(prefix="/verify", tags=["public-verification"])
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


@router.get("/{document_hash}")
def public_verify(document_hash: str, db: Session = Depends(get_db)):
    if not HEX64.fullmatch(document_hash):
        raise HTTPException(status_code=400, detail="Document hash must be 64 hexadecimal characters")
    item = db.scalar(
        select(Screening).where(Screening.document_hash == document_hash.lower()).order_by(Screening.created_at.desc()).limit(1)
    )
    if not item:
        return {"found": False, "document_hash": document_hash.lower()}

    latest = db.scalar(
        select(VerificationEvent).where(VerificationEvent.screening_id == item.id).order_by(VerificationEvent.id.desc()).limit(1)
    )
    return {
        "found": True,
        "document_hash": item.document_hash,
        "status": item.status,
        "reviewer_decision": item.reviewer_decision,
        "reviewed_at": item.reviewed_at,
        "latest_event_hash": latest.event_hash if latest else None,
        "blockchain_tx": latest.blockchain_tx if latest else None,
        "privacy_note": "No private document contents or extracted identity fields are returned by this public endpoint.",
    }
