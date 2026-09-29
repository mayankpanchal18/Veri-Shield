# Security notes

- **Passwords:** Argon2 via `argon2-cffi`.
- **Sessions:** signed JWT (HS256 for the hackathon prototype; use managed signing keys/rotation in production).
- **Evidence at rest:** AES-256-GCM with per-file random nonce and document hash as authenticated additional data.
- **Evidence location:** local off-chain encrypted storage for demo; use managed encrypted object storage in production.
- **Public verification:** intentionally excludes OCR text, extracted identity fields and original evidence.
- **Blockchain:** stores only hashes/status/event hashes; never place raw PII on a public chain.
- **Gemini key:** server-side environment variable only.
