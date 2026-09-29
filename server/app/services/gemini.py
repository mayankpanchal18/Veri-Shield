from __future__ import annotations

import json
import random
import re
import time
from dataclasses import dataclass

from google import genai
from google.genai import types

from ..core.config import settings
from ..schemas import GeminiReview

SYSTEM_PROMPT = """You are the AI reviewer inside VeriShield, an AI-assisted fake identity and document SCREENING system.
Your role is triage and explainable review support, not legal identity verification.

You receive: (1) the original uploaded identity document or certificate, (2) local Tesseract OCR text/field candidates,
(3) OpenCV forensic signals including ELA, sharpness, noise and edge density, and (4) a transparent deterministic screening score.

Tasks:
- Read the document multimodally and extract only visible fields.
- Compare visible text against OCR candidates and call out contradictions.
- Reason over the forensic signals; do not pretend a heuristic proves manipulation.
- Identify specific suspicious details or missing/contradictory elements.
- Produce a concise reviewer-facing explanation and a 0-100 SCREENING risk score.
- Give recommended human-review focus points.

Hard rules:
- Never auto-approve or declare a document definitively genuine/fake.
- Do not claim database, issuer, chip, QR, barcode, MRZ, signature or blockchain validation unless the supplied evidence actually proves it.
- When image quality is insufficient, mark checks UNKNOWN/WARN and lower confidence rather than guessing.
- Do not infer sensitive attributes that are not visibly printed.
- The limitations must state that human/authoritative verification is required for consequential decisions.
"""


@dataclass
class GeminiAnalysisResult:
    review: GeminiReview
    model: str
    mode: str
    service_note: str = ""
    attempts: list[str] | None = None


def _mock() -> GeminiReview:
    return GeminiReview.model_validate({
        "fields": {
            "full_name": "Demo User", "date_of_birth": "1999-04-08", "document_number": "DEMO-48219",
            "issue_date": "2024-01-01", "expiry_date": "2034-01-01", "issuing_authority": "Demo Authority",
            "issuing_country": "Demo", "address": "", "document_type": "Identity document"
        },
        "checks": [
            {"name": "OCR consistency", "status": "PASS", "details": "Demo OCR and visible fields are broadly consistent."},
            {"name": "Visual forensics", "status": "WARN", "details": "One visual signal is elevated in demo mode."},
        ],
        "suspicious_signals": ["Demo-only visual anomaly"],
        "risk_score": 31,
        "confidence": 0.83,
        "reviewer_summary": "Most visible elements are coherent; one visual anomaly should be checked by a reviewer.",
        "recommended_focus": ["Compare the expiry field typography with nearby text", "Check original source / issuer record if available"],
        "limitations": "Demo output only. Human review and authoritative verification are still required for consequential decisions."
    })


def _candidate_models() -> list[str]:
    models = [settings.gemini_model, *settings.gemini_fallback_models]
    out: list[str] = []
    for model in models:
        model = (model or "").strip()
        if model and model not in out:
            out.append(model)
    return out


def _status_code(exc: Exception) -> int | None:
    for attr in ("code", "status_code"):
        value = getattr(exc, attr, None)
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
    match = re.search(r"\b(400|401|403|404|408|409|429|500|502|503|504)\b", str(exc))
    return int(match.group(1)) if match else None


def _is_transient(exc: Exception) -> bool:
    code = _status_code(exc)
    if code in {408, 429, 500, 502, 503, 504}:
        return True
    text = str(exc).upper()
    return any(token in text for token in (
        "UNAVAILABLE", "RESOURCE_EXHAUSTED", "HIGH DEMAND", "OVERLOADED", "TIMEOUT", "TIMED OUT"
    ))


def _can_try_next_model(exc: Exception) -> bool:
    if _is_transient(exc):
        return True
    code = _status_code(exc)
    # A model alias may be unavailable to a project even though another supported model works.
    return code == 404 or "MODEL" in str(exc).upper() and "NOT FOUND" in str(exc).upper()


def _document_type_from_ocr(text: str) -> str:
    lowered = text.lower()
    if "aadhaar" in lowered or "aadhar" in lowered:
        return "Aadhaar card"
    if "passport" in lowered:
        return "Passport"
    if "driving licence" in lowered or "driving license" in lowered:
        return "Driving licence"
    if "permanent account number" in lowered or re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text):
        return "PAN card"
    if "certificate" in lowered:
        return "Certificate"
    return "Identity document"


def _local_fallback(ocr: dict, forensics: dict, deterministic_score: int, reason: str) -> GeminiReview:
    """Keep the hackathon demo usable when Gemini has a temporary capacity outage.

    This is deliberately labelled as a LOCAL fallback. It does not pretend Gemini ran.
    """
    ocr_fields = ocr.get("fields") or {}
    dates = ocr_fields.get("dates_detected") or []
    flags = list(forensics.get("flags") or [])
    ocr_available = ocr.get("engine") != "unavailable"

    fields = {
        "full_name": ocr_fields.get("full_name", ""),
        "date_of_birth": dates[0] if dates else "",
        "document_number": ocr_fields.get("document_number_candidate", ""),
        "issue_date": "",
        "expiry_date": "",
        "issuing_authority": "",
        "issuing_country": "",
        "address": "",
        "document_type": _document_type_from_ocr(ocr.get("text", "")),
    }

    checks = [
        {
            "name": "Local OCR extraction",
            "status": "PASS" if ocr_available and ocr.get("text") else "WARN",
            "details": "Tesseract extracted local text for reviewer inspection." if ocr_available and ocr.get("text")
                       else "Local OCR was unavailable or returned little usable text.",
        },
        {
            "name": "OpenCV / ELA forensics",
            "status": "WARN" if flags else "PASS",
            "details": "; ".join(flags[:3]) if flags else "No configured local forensic threshold was exceeded.",
        },
        {
            "name": "Gemini multimodal reasoning",
            "status": "UNKNOWN",
            "details": "Gemini was temporarily unavailable, so this result contains local OCR/forensic evidence only.",
        },
    ]

    focus = [
        "Review the original document because Gemini multimodal reasoning was temporarily unavailable.",
        "Compare OCR-extracted identity fields against the visible document.",
    ]
    if flags:
        focus.append("Inspect the visual regions related to the local forensic warnings.")

    short_reason = reason.replace("\n", " ")[:220]
    return GeminiReview.model_validate({
        "fields": fields,
        "checks": checks,
        "suspicious_signals": flags[:8],
        "risk_score": int(max(0, min(100, deterministic_score))),
        "confidence": 0.38 if ocr_available else 0.22,
        "reviewer_summary": (
            "Gemini is temporarily unavailable. VeriShield completed a degraded local screening using "
            "Tesseract OCR plus OpenCV/ELA signals so the evidence can still reach human review. "
            f"Service note: {short_reason}"
        ),
        "recommended_focus": focus,
        "limitations": (
            "Degraded local fallback: Gemini multimodal reasoning did not run for this screening. "
            "Local image-forensic heuristics do not prove authenticity or manipulation. Human review and "
            "authoritative verification are required for consequential decisions."
        ),
    })


def _generate_once(client: genai.Client, model: str, file_bytes: bytes, mime_type: str, evidence: dict) -> GeminiReview:
    response = client.models.generate_content(
        model=model,
        contents=[
            SYSTEM_PROMPT,
            "Local evidence JSON:\n" + json.dumps(evidence, ensure_ascii=False),
            types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=GeminiReview,
            temperature=0.2,
        ),
    )

    if getattr(response, "parsed", None):
        return response.parsed
    if not getattr(response, "text", None):
        raise RuntimeError("Gemini returned an empty response")
    return GeminiReview.model_validate_json(response.text)


def analyze_with_gemini(
    file_bytes: bytes,
    mime_type: str,
    ocr: dict,
    forensics: dict,
    deterministic_score: int,
) -> GeminiAnalysisResult:
    if settings.gemini_mock:
        return GeminiAnalysisResult(review=_mock(), model="mock", mode="MOCK", attempts=["mock"])

    if not settings.gemini_api_key or "PASTE_YOUR" in settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured in server/.env")

    evidence = {
        "ocr_engine": ocr.get("engine"),
        "ocr_text": ocr.get("text", "")[:9000],
        "ocr_field_candidates": ocr.get("fields", {}),
        "ocr_warnings": ocr.get("warnings", []),
        "forensic_aggregate": forensics.get("aggregate", {}),
        "forensic_flags": forensics.get("flags", []),
        "deterministic_screening_score": deterministic_score,
    }

    client = genai.Client(api_key=settings.gemini_api_key)
    attempts: list[str] = []
    last_exc: Exception | None = None

    for model in _candidate_models():
        max_attempts = max(1, settings.gemini_retry_attempts)
        for attempt in range(max_attempts):
            try:
                review = _generate_once(client, model, file_bytes, mime_type, evidence)
                note = "" if model == settings.gemini_model else f"Primary Gemini model was busy; completed with fallback model {model}."
                return GeminiAnalysisResult(
                    review=review,
                    model=model,
                    mode="GEMINI" if model == settings.gemini_model else "GEMINI_FALLBACK_MODEL",
                    service_note=note,
                    attempts=attempts + [f"{model}:success"],
                )
            except Exception as exc:  # Google SDK raises typed API errors; keep this resilient across SDK versions.
                last_exc = exc
                code = _status_code(exc)
                attempts.append(f"{model}:{code or type(exc).__name__}")

                if not _can_try_next_model(exc):
                    raise

                if attempt < max_attempts - 1:
                    # Short app-level retry. The Google SDK also performs its own retries for transient failures.
                    delay = min(4.0, 1.0 * (2 ** attempt)) + random.uniform(0.05, 0.35)
                    time.sleep(delay)
                    continue
                break

    if last_exc and settings.gemini_allow_local_fallback and _is_transient(last_exc):
        return GeminiAnalysisResult(
            review=_local_fallback(ocr, forensics, deterministic_score, str(last_exc)),
            model="local-ocr-opencv",
            mode="LOCAL_FALLBACK",
            service_note="Gemini capacity was temporarily unavailable after trying configured models.",
            attempts=attempts,
        )

    if last_exc:
        raise RuntimeError(f"Gemini analysis failed after configured model fallbacks: {last_exc}") from last_exc
    raise RuntimeError("No Gemini models are configured")
