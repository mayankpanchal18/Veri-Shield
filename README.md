# VeriShield

**AI-Based Fake Identity & Document Screening System**

**Principle:** `DETECT → REVIEW → VERIFY`

**Tagline:** *AI Eyes for Authentic Identities.*

VeriShield is a hackathon prototype for AI-assisted identity and document screening. The screening path combines **OCR + OpenCV/ELA + Gemini → human review → SHA-256 tamper-evident record → optional Solidity/Hardhat anchor → public hash/status verification**.

## Repository layout

- `client/` — React, Vite, and Tailwind frontend.
- `server/` — FastAPI backend, screening services, and encrypted evidence storage.
- `blockchain/` — optional Solidity registry and Hardhat deployment scripts.
- `docs/` — architecture, model pipeline, security, and presentation alignment notes.

Copy `server/.env.example` to `server/.env` for local configuration. Never commit API keys, private keys, databases, or uploaded identity documents. The demo credentials below are for local demonstrations only.

## What now matches the PPT

- **AI-assisted screening:** Tesseract OCR + OpenCV for ELA, sharpness, noise and edge-density signals.
- **Gemini reasoning:** Gemini receives the document **and** the local OCR/forensic evidence, then produces an explainable reviewer summary, field extraction, checks, risk signal, confidence and reviewer focus points.
- **Human-in-the-loop:** every completed AI scan becomes `PENDING_REVIEW`; only a reviewer can record `VALID`, `INVALID`, or `NEEDS_MORE_EVIDENCE`.
- **Tamper-evident history:** SHA-256 document hash + chained verification event hashes.
- **Blockchain:** optional Solidity + Hardhat registry stores only document/status/event hashes; no PII goes on-chain.
- **Privacy:** original evidence is encrypted at rest with **AES-256-GCM** and stored off-chain. Passwords use **Argon2**. Sessions use **JWT**.
- **Public verification:** anyone can query a 64-character document hash and see only verification status/hash metadata.
- **UI:** React + Tailwind, using the PPT's navy/cyan/green/indigo visual language and its Detect → Review → Verify framing.

## Architecture

```text
User / Institution
      |
      v
React + Tailwind portal
      |
      v
FastAPI
  |-- JWT + Argon2 auth
  |-- AES-256-GCM encrypted evidence storage
  |
  +--> Tesseract OCR
  |
  +--> OpenCV / ELA / sharpness / noise / edges
  |
  +--> transparent scikit-learn signal normalization
  |
  +--> Gemini multimodal reviewer reasoning
  |       receives OCR + forensic signals + document
  |
  +--> Human reviewer decision
  |
  +--> SHA-256 chained revision history
  |
  +--> optional Solidity / Hardhat anchor
  |
  +--> public hash/status lookup
```

## Quick start on Windows

### 1. Requirements

Install:
- Node.js 20+
- Python 3.11 or 3.12
- **Tesseract OCR** (recommended for the local OCR stage)

PostgreSQL is **not required** for the hackathon demo. SQLite is the default. PostgreSQL is supported through `DATABASE_URL`.

### 2. Create Python environment

From the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r server\requirements.txt
```

If PowerShell blocks activation, use Command Prompt:

```cmd
venv\Scripts\activate
```

### 3. Install frontend/root packages

```powershell
npm install
npm install --prefix client
```

The optional blockchain folder has its own packages and is not needed for the first run.

### 4. Configure server

```powershell
Copy-Item server\.env.example server\.env
notepad server\.env
```

Set at least:

```env
GEMINI_API_KEY=YOUR_NEW_KEY
JWT_SECRET=PUT_A_LONG_RANDOM_SECRET_HERE
GEMINI_MODEL=gemini-3.8-flash
GEMINI_MOCK=false
```

If Tesseract is installed but not on PATH, add for example:

```env
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### 5. Run the full app

```powershell
npm run dev
```

Open:
- Frontend: `http://localhost:5173`
- FastAPI docs: `http://localhost:8000/docs`

## Demo accounts

When `DEMO_MODE=true`:

| Role | Email | Password |
|---|---|---|
| Submitter | `submitter@verishield.ai` | `Demo@12345` |
| Reviewer | `reviewer@verishield.ai` | `Demo@12345` |

Change/disable demo credentials before any deployment.

## Demo flow for judges

1. Log in as **Submitter**.
2. Upload an ID or certificate.
3. Show **OCR fields**, **ELA/sharpness/noise/edge metrics**, **Gemini reviewer summary**, **risk score**, and `PENDING_REVIEW`.
4. Copy the displayed SHA-256 hash.
5. Log out and sign in as **Reviewer**.
6. Open **Review Queue**, open the original encrypted evidence, inspect AI reasoning, and record a final decision.
7. Open **Public Verify**, paste the same hash, and show the final status without exposing the private document.
8. Optional: enable the Hardhat chain and show the blockchain transaction hash after review.

## Gemini model behavior

Gemini is intentionally not the sole detector. `server/app/services/gemini.py` receives:
- original image/PDF,
- Tesseract OCR text and extracted candidates,
- OpenCV/ELA aggregate metrics and anomaly flags,
- deterministic local screening score.

It returns structured reviewer-facing fields/checks/reasons. The backend combines its score with the transparent local score, but **never auto-approves** a document.

## Scoring note

The scikit-learn component is a **normalization/calibration layer for forensic heuristics**, not a trained fraud classifier. It avoids falsely claiming that the hackathon prototype was trained on a verified fraud dataset. The final AI score is still a screening/triage signal only.

## Optional PostgreSQL

Set:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/verishield
```

The SQLAlchemy schema is created automatically on startup.

## Optional blockchain

See [`blockchain/README.md`](blockchain/README.md). The backend always maintains a local SHA-256 revision chain; blockchain anchoring is additive.

## Important limitation

VeriShield is positioned as a **screening / triage tool**, not a replacement for official legal identity verification. Production systems should add authoritative issuer/DigiLocker APIs with consent, deterministic QR/MRZ/signature checks where applicable, retention policies, malware scanning, role administration, key management and independent security testing.

## Demo login reliability

When `DEMO_MODE=true`, VeriShield repairs the two built-in demo accounts on every API start. This means an older/stale `server/data/verishield.db` cannot leave the displayed demo credentials out of sync.

- Submitter: `submitter@verishield.ai` / `Demo@12345`
- Reviewer: `reviewer@verishield.ai` / `Demo@12345`

If an older API process is still occupying port 8000, run `restart_windows.cmd` once to stop the stale dev servers and launch this build.

## Gemini 503 / high-demand resilience

This build treats `503 UNAVAILABLE` / high-demand responses as temporary provider-capacity errors, not as a failed VeriShield pipeline.

Default order:

1. `gemini-3.8-flash`
2. `gemini-3.5-flash`
3. `gemini-3.1-flash-lite`
4. If all configured Gemini models are temporarily unavailable, VeriShield returns a **clearly labelled local fallback** based only on Tesseract OCR + OpenCV/ELA and keeps the case pending for human review.

Configure in `server/.env`:

```env
GEMINI_MODEL=gemini-3.8-flash
GEMINI_FALLBACK_MODELS=gemini-3.5-flash,gemini-3.1-flash-lite
GEMINI_RETRY_ATTEMPTS=1
GEMINI_ALLOW_LOCAL_FALLBACK=true
```

The local fallback never claims Gemini ran and never auto-approves a document. A later screening can use Gemini again when capacity is available.
