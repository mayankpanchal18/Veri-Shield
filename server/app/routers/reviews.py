from __future__ import annotations

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import reviewer_only
from ..models import Screening, User
from ..schemas import ReviewDecisionRequest
from ..services.blockchain import anchor_verification
from ..services.ledger import append_event

router = APIRouter(prefix="/reviews", tags=["reviews"])


def _row(item: Screening) -> dict:
    return {
        "id": item.id, "filename": item.filename, "document_hash": item.document_hash,
        "document_type": item.document_type, "risk_score": item.risk_score, "risk_level": item.risk_level,
        "confidence": item.confidence, "status": item.status, "created_at": item.created_at,
        "extracted_fields": item.extracted_fields, "forensics": item.forensics, "ai_review": item.ai_review,
        "ocr_fields": item.ocr_fields,
    }


@router.get("/queue")
def review_queue(db: Session = Depends(get_db), reviewer: User = Depends(reviewer_only)):
    items = db.scalars(
        select(Screening).where(Screening.status == "PENDING_REVIEW").order_by(Screening.risk_score.desc(), Screening.created_at.asc())
    ).all()
    return {"items": [_row(x) for x in items]}


@router.post("/{screening_id}/decision")
def decide(
    screening_id: int,
    payload: ReviewDecisionRequest,
    db: Session = Depends(get_db),
    reviewer: User = Depends(reviewer_only),
):
    item = db.get(Screening, screening_id)
    if not item:
        raise HTTPException(status_code=404, detail="Screening not found")
    if item.status != "PENDING_REVIEW":
        raise HTTPException(status_code=409, detail=f"Screening is already {item.status}")

    status_map = {
        "VALID": "VERIFIED_VALID",
        "INVALID": "VERIFIED_INVALID",
        "NEEDS_MORE_EVIDENCE": "MORE_EVIDENCE_REQUESTED",
    }
    item.reviewer_id = reviewer.id
    item.reviewer_decision = payload.decision
    item.reviewer_note = payload.note.strip()
    item.reviewed_at = datetime.now(timezone.utc)
    item.status = status_map[payload.decision]

    event = append_event(
        db, item.id, item.document_hash, "HUMAN_REVIEW_DECISION", reviewer.id,
        {"decision": payload.decision, "status": item.status},
    )

    try:
        tx_hash = anchor_verification(item.document_hash, item.status, event.event_hash)
        if tx_hash:
            event.blockchain_tx = tx_hash
    except Exception as exc:
        # Local SHA-256 chain remains valid even if optional blockchain anchoring is unavailable.
        event.payload = {**event.payload, "blockchain_warning": str(exc)}

    db.commit()
    return {
        "screening": _row(item),
        "event_hash": event.event_hash,
        "blockchain_tx": event.blockchain_tx,
        "message": "Human decision recorded. Public verification exposes only hash/status metadata.",
    }
