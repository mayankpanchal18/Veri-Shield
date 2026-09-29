# VeriShield architecture

## Round 1 architecture mapped to code

```text
Issuing authorities / individual users
               |
               v
       React + Tailwind portal
               |
               v
         FastAPI backend
        /       |       \
       v        v        v
    OCR      Forensics  Encrypted evidence
 Tesseract  OpenCV/ELA  AES-256-GCM off-chain
       \        /
        \      /
         v    v
      Gemini reasoning
           |
           v
    PENDING HUMAN REVIEW
           |
           v
   reviewer final decision
           |
           v
   SHA-256 revision chain
           |
           +----> optional Solidity / Hardhat anchor
           |
           v
 public hash/status verification
```

### Security boundaries

- Raw identity evidence never goes to the public verification endpoint.
- Blockchain stores only hashes/status/event hashes.
- JWT authorizes private application endpoints.
- Argon2 hashes passwords.
- AES-256-GCM encrypts stored evidence.
- The local SHA-256 revision chain works even if the optional blockchain node is offline.
