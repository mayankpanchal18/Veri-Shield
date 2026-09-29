# PPT → implementation alignment

| PPT concept | Implementation |
|---|---|
| Upload ID / Certificate | `POST /api/screenings` + React upload view |
| OCR + OpenCV + ELA + Gemini | `services/ocr.py`, `forensics.py`, `risk.py`, `gemini.py` |
| OCR extracts name / DOB / ID / issuer | Local OCR candidates + Gemini structured visible-field extraction |
| Gemini reviewer reasoning | Gemini receives OCR/forensic signals + original file and returns structured reviewer summary |
| Human verifier decision | Reviewer queue + `/api/reviews/{id}/decision` |
| SHA-256 immutable/revision record | `services/ledger.py` chained event hashes |
| Blockchain history | Solidity `VeriShieldRegistry.sol` + optional backend anchor |
| Sensitive evidence off-chain/encrypted | `services/crypto_storage.py` AES-256-GCM evidence files |
| Public status/hash lookup | `/api/verify/{document_hash}` + React Public Verify view |
| React + Tailwind | `client/` |
| FastAPI + Python | `server/` |
| OpenCV / Tesseract / Scikit-learn / Gemini | Python analysis services |
| JWT / Argon2 / AES-256-GCM | server auth/security/storage layer |
| Solidity / Hardhat / SHA-256 | `blockchain/` + ledger service |
