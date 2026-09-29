from __future__ import annotations

import base64
import os
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from ..core.config import settings


def _load_or_create_key() -> bytes:
    if settings.data_encryption_key:
        try:
            key = base64.urlsafe_b64decode(settings.data_encryption_key.encode())
        except Exception as exc:
            raise RuntimeError("DATA_ENCRYPTION_KEY must be URL-safe base64") from exc
        if len(key) != 32:
            raise RuntimeError("DATA_ENCRYPTION_KEY must decode to exactly 32 bytes")
        return key

    if settings.env == "production":
        raise RuntimeError("DATA_ENCRYPTION_KEY is required in production")

    dev_key_path = settings.evidence_dir.parent / ".dev_aes_key"
    if dev_key_path.exists():
        return base64.urlsafe_b64decode(dev_key_path.read_bytes())
    key = AESGCM.generate_key(bit_length=256)
    dev_key_path.write_bytes(base64.urlsafe_b64encode(key))
    return key


_KEY = _load_or_create_key()
_AES = AESGCM(_KEY)


def encrypt_evidence(screening_id: int, plaintext: bytes, document_hash: str) -> str:
    nonce = os.urandom(12)
    aad = document_hash.encode("ascii")
    ciphertext = _AES.encrypt(nonce, plaintext, aad)
    path = settings.evidence_dir / f"{screening_id}.bin"
    path.write_bytes(nonce + ciphertext)
    return str(path)


def decrypt_evidence(path_value: str, document_hash: str) -> bytes:
    blob = Path(path_value).read_bytes()
    nonce, ciphertext = blob[:12], blob[12:]
    return _AES.decrypt(nonce, ciphertext, document_hash.encode("ascii"))
