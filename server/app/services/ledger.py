from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import VerificationEvent


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def append_event(
    db: Session,
    screening_id: int,
    document_hash: str,
    action: str,
    actor_user_id: int | None,
    payload: dict,
) -> VerificationEvent:
    previous = db.scalar(
        select(VerificationEvent)
        .where(VerificationEvent.screening_id == screening_id)
        .order_by(VerificationEvent.id.desc())
        .limit(1)
    )
    previous_hash = previous.event_hash if previous else "0" * 64
    timestamp = datetime.now(timezone.utc)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    material = f"{previous_hash}|{document_hash}|{action}|{timestamp.isoformat()}|{canonical}".encode()
    event_hash = hashlib.sha256(material).hexdigest()

    event = VerificationEvent(
        screening_id=screening_id,
        document_hash=document_hash,
        action=action,
        actor_user_id=actor_user_id,
        payload=payload,
        previous_event_hash=previous_hash,
        event_hash=event_hash,
        created_at=timestamp,
    )
    db.add(event)
    db.flush()
    return event
