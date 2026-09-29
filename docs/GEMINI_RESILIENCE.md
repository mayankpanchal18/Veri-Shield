# Gemini resilience

VeriShield's analysis sequence is intentionally resilient for live demos and transient provider outages:

`OCR -> OpenCV/ELA -> Gemini primary -> Gemini fallback model(s) -> labelled local fallback -> human review`

The primary and fallback Gemini calls use the same document, OCR evidence, forensic evidence, Pydantic response schema and screening-only safety prompt. Only transient/server/model-availability failures are eligible for automatic model failover. Authentication, permission and invalid-request errors are surfaced instead of being hidden.

If every configured Gemini model is unavailable because of temporary capacity, the app still creates a reviewable evidence package using local OCR + image forensics. The UI labels this as `LOCAL_FALLBACK`, reports the model as `local-ocr-opencv`, lowers confidence, and explicitly states that Gemini multimodal reasoning did not run.
