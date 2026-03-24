from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from datetime import date

from .database import create_db_and_tables, get_session
from .models import Users, Blog
from .auth import (
    hash_password,
    verify_password,
    create_token,
    get_current_user,
)

from agents.graph import app as graph_app


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# -----------------------
# Schemas
# -----------------------

class UserIn(BaseModel):
    email: str
    password: str


class BlogRequest(BaseModel):
    topic: str


# -----------------------
# Auth Routes
# -----------------------

@app.post("/signup")
def signup(user: UserIn, session: Session = Depends(get_session)):

    existing = session.exec(
        select(Users).where(Users.email == user.email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = Users(
        email=user.email,
        password=hash_password(user.password)
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User created"}

@app.post("/login")
def login(user: UserIn, session: Session = Depends(get_session)):
    db_user = session.exec(select(Users).where(Users.email == user.email)).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(db_user)
    return {"token": token}


# -----------------------
# Blog Routes
# -----------------------

from sqlmodel import select

@app.post("/generate")
def generate_blog(
    req: BlogRequest,
    user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    # verify user exists
    db_user = session.exec(
        select(Users).where(Users.id == user.id)
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")

    result = graph_app.invoke({
        "topic": req.topic
    })

    blog = Blog(
        user_id=user.id,
        topic=req.topic,
        content=result.get("final", "")
    )

    session.add(blog)
    session.commit()

    return result

@app.get("/blogs")
def get_blogs(
    user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    blogs = session.exec(
        select(Blog)
        .where(Blog.user_id == user.id)
        .order_by(Blog.created_at.desc())
    ).all()

    return blogs