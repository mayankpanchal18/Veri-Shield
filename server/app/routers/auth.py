from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.security import create_access_token, hash_password, verify_password
from ..database import get_db
from ..dependencies import current_user
from ..models import User
from ..schemas import LoginRequest, RegisterRequest

router = APIRouter(prefix="/auth", tags=["auth"])


def public_user(user: User) -> dict:
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role, "created_at": user.created_at}


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = User(name=payload.name.strip(), email=email, role="submitter", password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user": public_user(user), "token": create_access_token(user.id, user.role, user.email)}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.lower().strip()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return {"user": public_user(user), "token": create_access_token(user.id, user.role, user.email)}


@router.get("/me")
def me(user: User = Depends(current_user)):
    return {"user": public_user(user)}
