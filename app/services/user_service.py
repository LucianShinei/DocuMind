from datetime import datetime

from app.auth.auth import create_access_token
from app.auth.security import hash_password, verify_password
from app.database.mongodb import get_database
from app.models.user import User


async def register_user(user):
    db = get_database()

    existing = await db.users.find_one({"email": user.email})

    if existing:
        raise ValueError("Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        created_at=datetime.utcnow(),
    )

    result = await db.users.insert_one(new_user.model_dump())

    return {
        "id": str(result.inserted_id),
        "username": user.username,
        "email": user.email,
    }


async def login_user(user):
    db = get_database()

    existing = await db.users.find_one({"email": user.email})

    if not existing or not verify_password(
        user.password,
        existing["hashed_password"],
    ):
        raise ValueError("Invalid credentials")

    token = create_access_token(
        {
            "sub": str(existing["_id"]),
            "email": existing["email"],
        }
    )

    return {"access_token": token, "token_type": "bearer"}