from __future__ import annotations

from hashlib import sha256
from io import BytesIO
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import current_user
from ..models import Screening, User, VerificationEvent
from ..services.crypto_storage import decrypt_evidence, encrypt_evidence
from ..services.forensics import analyze_forensics
from ..services.gemini import analyze_with_gemini
from ..services.ledger import append_event
from ..services.ocr import file_to_images, run_ocr
from ..services.risk import combine_risk, deterministic_risk, risk_level

router = APIRouter(prefix="/screenings", tags=["screenings"])
ALLOWED = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
MAX_FILE = 10 * 1024 * 1024


def _serialize(screening: Screening, include_private: bool = True) -> dict:
    data = {
        "id": screening.id,
        "filename": screening.filename,
        "mime_type": screening.mime_type,
        "document_hash": screening.document_hash,
        "document_type": screening.document_type,
        "risk_score": screening.risk_score,
        "risk_level": screening.risk_level,
        "confidence": screening.confidence,
        "deterministic_risk": screening.deterministic_risk,
        "status": screening.status,
        "reviewer_decision": screening.reviewer_decision,
        "reviewer_note": screening.reviewer_note,
        "reviewed_at": screening.reviewed_at,
        "created_at": screening.created_at,
    }
    if include_private:
        data.update({
            "ocr_fields": screening.ocr_fields,
            "ocr_preview": screening.ocr_text[:2500],
            "extracted_fields": screening.extracted_fields,
            "forensics": screening.forensics,
            "ai_review": screening.ai_review,
        })
    return data


def _can_access(screening: Screening, user: User) -> bool:
    return user.role == "reviewer" or screening.submitter_id == user.id


@router.post("")
async def create_screening(
    document: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    if document.content_type not in ALLOWED:
        raise HTTPException(status_code=415, detail="Use JPG, PNG, WebP, or PDF")
    raw = await document.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    if len(raw) > MAX_FILE:
        raise HTTPException(status_code=413, detail="File is larger than 10 MB")

    document_hash = sha256(raw).hexdigest()
    screening = Screening(
        submitter_id=user.id,
        filename=document.filename or "document",
        mime_type=document.content_type,
        document_hash=document_hash,
        evidence_path="",
        status="ANALYZING",
    )
    db.add(screening)
    db.flush()
    screening.evidence_path = encrypt_evidence(screening.id, raw, document_hash)
    db.commit()
    db.refresh(screening)

    try:
        images = file_to_images(raw, document.content_type)
        ocr = run_ocr(images)
        forensics = analyze_forensics(images)
        local_risk = deterministic_risk(forensics, ocr)
        gemini_result = analyze_with_gemini(raw, document.content_type, ocr, forensics, local_risk)
        gemini = gemini_result.review
        final_risk = combine_risk(local_risk, gemini.risk_score, gemini.confidence)

        screening.document_type = gemini.fields.document_type or "Unknown"
        screening.ocr_text = ocr.get("text", "")
        screening.ocr_fields = ocr.get("fields", {})
        screening.extracted_fields = gemini.fields.model_dump()
        screening.forensics = forensics
        ai_review = gemini.model_dump()
        ai_review["analysis_model"] = gemini_result.model
        ai_review["analysis_mode"] = gemini_result.mode
        ai_review["service_note"] = gemini_result.service_note
        ai_review["model_attempts"] = gemini_result.attempts or []
        screening.ai_review = ai_review
        screening.deterministic_risk = local_risk
        screening.risk_score = final_risk
        screening.risk_level = risk_level(final_risk)
        screening.confidence = float(gemini.confidence)
        screening.status = "PENDING_REVIEW"
        event = append_event(
            db, screening.id, document_hash, "AI_SCREENING_COMPLETE", user.id,
            {
                "risk_score": final_risk,
                "risk_level": screening.risk_level,
                "model": gemini_result.model,
                "analysis_mode": gemini_result.mode,
            },
        )
        db.commit()
        db.refresh(screening)
        return {"screening": _serialize(screening), "event_hash": event.event_hash}
    except Exception as exc:
        screening.status = "ANALYSIS_FAILED"
        append_event(db, screening.id, document_hash, "AI_SCREENING_FAILED", user.id, {"error_type": type(exc).__name__})
        db.commit()
        raise HTTPException(status_code=502, detail=f"Analysis failed: {exc}") from exc


@router.get("")
def list_screenings(db: Session = Depends(get_db), user: User = Depends(current_user)):
    stmt = select(Screening).order_by(Screening.created_at.desc()).limit(100)
    if user.role != "reviewer":
        stmt = stmt.where(Screening.submitter_id == user.id)
    rows = db.scalars(stmt).all()
    return {"items": [_serialize(item, include_private=False) for item in rows]}


@router.get("/{screening_id}")
def get_screening(screening_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = db.get(Screening, screening_id)
    if not item or not _can_access(item, user):
        raise HTTPException(status_code=404, detail="Screening not found")
    events = db.scalars(
        select(VerificationEvent).where(VerificationEvent.screening_id == item.id).order_by(VerificationEvent.id.asc())
    ).all()
    return {
        "screening": _serialize(item),
        "events": [{
            "action": e.action, "event_hash": e.event_hash, "previous_event_hash": e.previous_event_hash,
            "blockchain_tx": e.blockchain_tx, "created_at": e.created_at
        } for e in events],
    }


@router.get("/{screening_id}/evidence")
def get_evidence(screening_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    item = db.get(Screening, screening_id)
    if not item or not _can_access(item, user):
        raise HTTPException(status_code=404, detail="Evidence not found")
    data = decrypt_evidence(item.evidence_path, item.document_hash)
    return Response(content=data, media_type=item.mime_type, headers={"Content-Disposition": f'inline; filename="{item.filename}"'})
