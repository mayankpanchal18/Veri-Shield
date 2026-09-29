from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .database import Base, engine
from .demo import seed_demo_accounts
from .routers import auth, reviews, screenings, verification


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if not settings.jwt_secret:
        raise RuntimeError("JWT_SECRET is missing. Copy server/.env.example to server/.env")
    Base.metadata.create_all(bind=engine)
    seed_demo_accounts()
    yield


app = FastAPI(
    title="VeriShield API",
    version="2.0.1",
    description="Detect -> Review -> Verify: AI-assisted identity/document screening with human review and tamper-evident history.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.client_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(screenings.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(verification.router, prefix="/api")


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "service": "verishield-api",
        "pipeline": ["Tesseract OCR", "OpenCV + ELA", "Gemini reasoning", "Human review", "SHA-256 ledger"],
        "gemini_model": settings.gemini_model,
        "blockchain_enabled": settings.blockchain_enabled,
        "build": "2.0.1-login-fix",
        "demo_mode": settings.demo_mode,
    }
