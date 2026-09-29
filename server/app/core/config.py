from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

SERVER_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = SERVER_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
load_dotenv(SERVER_DIR / ".env")


class Settings:
    app_name = os.getenv("APP_NAME", "VeriShield")
    env = os.getenv("ENV", "development")
    client_origin = os.getenv("CLIENT_ORIGIN", "http://localhost:5173")

    gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    gemini_fallback_models = [m.strip() for m in os.getenv("GEMINI_FALLBACK_MODELS", "gemini-3.5-flash,gemini-3.1-flash-lite").split(",") if m.strip()]
    gemini_retry_attempts = max(1, int(os.getenv("GEMINI_RETRY_ATTEMPTS", "1")))
    gemini_allow_local_fallback = os.getenv("GEMINI_ALLOW_LOCAL_FALLBACK", "true").lower() == "true"
    gemini_mock = os.getenv("GEMINI_MOCK", "false").lower() == "true"

    jwt_secret = os.getenv("JWT_SECRET", "")
    jwt_expires_minutes = int(os.getenv("JWT_EXPIRES_MINUTES", "720"))

    raw_database_url = os.getenv("DATABASE_URL", "").strip()
    database_url = raw_database_url or f"sqlite:///{(DATA_DIR / 'verishield.db').as_posix()}"

    data_encryption_key = os.getenv("DATA_ENCRYPTION_KEY", "").strip()
    tesseract_cmd = os.getenv("TESSERACT_CMD", "").strip()

    demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"
    demo_password = os.getenv("DEMO_PASSWORD", "Demo@12345")

    blockchain_enabled = os.getenv("BLOCKCHAIN_ENABLED", "false").lower() == "true"
    blockchain_rpc_url = os.getenv("BLOCKCHAIN_RPC_URL", "http://127.0.0.1:8545")
    blockchain_contract_address = os.getenv("BLOCKCHAIN_CONTRACT_ADDRESS", "").strip()
    blockchain_private_key = os.getenv("BLOCKCHAIN_PRIVATE_KEY", "").strip()

    evidence_dir = DATA_DIR / "evidence"


settings = Settings()
settings.evidence_dir.mkdir(parents=True, exist_ok=True)
