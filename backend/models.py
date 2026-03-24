from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime


class Blog(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="users.id")
    topic: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["Users"] = Relationship(back_populates="blogs")


class Users(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(index=True, unique=True)
    password: str

    blogs: List[Blog] = Relationship(back_populates="user")