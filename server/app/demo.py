from __future__ import annotations

from sqlalchemy import select

from .core.config import settings
from .core.security import hash_password
from .database import SessionLocal
from .models import User


def seed_demo_accounts() -> None:
    """Create or repair deterministic demo accounts when DEMO_MODE is enabled.

    This deliberately resets the two built-in demo credentials on API startup so
    an older/stale SQLite database cannot make the credentials displayed in the
    UI stop working. Production deployments should set DEMO_MODE=false.
    """
    if not settings.demo_mode:
        return

    seeds = [
        ("Demo Submitter", "submitter@verishield.ai", "submitter"),
        ("Demo Reviewer", "reviewer@verishield.ai", "reviewer"),
    ]

    with SessionLocal() as db:
        for name, email, role in seeds:
            user = db.scalar(select(User).where(User.email == email))
            if user is None:
                user = User(
                    name=name,
                    email=email,
                    role=role,
                    password_hash=hash_password(settings.demo_password),
                )
                db.add(user)
            else:
                user.name = name
                user.role = role
                user.password_hash = hash_password(settings.demo_password)

        db.commit()

    print("[VeriShield] Demo credentials repaired for this startup.")
