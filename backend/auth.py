from fastapi import Depends, HTTPException, Header
from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session, select
from uuid import UUID

from .database import get_session
from .models import Users

SECRET = "SECRET"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    print("HASH INPUT:", password)
    print("HASH LENGTH:", len(password))
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def create_token(user: Users):
    return jwt.encode({"user_id": str(user.id)}, SECRET, algorithm=ALGORITHM)


def get_current_user(
    authorization: str = Header(...),
    session: Session = Depends(get_session),
):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user_id = UUID(payload["user_id"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.exec(select(Users).where(Users.id == user_id)).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user