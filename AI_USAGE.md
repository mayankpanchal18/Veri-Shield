# AI Usage — VeriShield

## Gemini's functional role

Gemini is part of the analysis layer, not a cosmetic mention. The backend first runs local OCR and forensic analysis, then passes the resulting evidence plus the uploaded document to Gemini.

Inputs to Gemini include:
- OCR text and field candidates from Tesseract,
- ELA score,
- sharpness,
- local noise residual,
- edge density,
- heuristic forensic flags,
- local screening risk,
- the original image/PDF for multimodal inspection.

Gemini returns structured data:
- document type,
- extracted visible identity fields,
- consistency checks (`PASS/WARN/FAIL/UNKNOWN`),
- suspicious visible signals,
- a 0–100 screening risk score,
- confidence,
- reviewer-facing explanation,
- human-review focus points,
- explicit limitations.

## Human control

The Gemini result does **not** approve or reject a document. The API stores the screening as `PENDING_REVIEW`. A user with the reviewer role must inspect the evidence and record the final outcome.

## Safety / accuracy boundaries

The prompt explicitly prevents claims of authoritative verification unless the system actually performs the check. Gemini is instructed not to claim chip, QR, barcode, MRZ, issuer-database or cryptographic verification from appearance alone.

## Privacy

The Gemini key remains server-side. Original documents are encrypted off-chain at rest using AES-256-GCM. Only hashes/status/event hashes are exposed through public verification and optional blockchain anchoring.
