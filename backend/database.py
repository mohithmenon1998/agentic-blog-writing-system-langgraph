from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_DB_PWD = os.getenv("SUPABASE_DB_PWD")
DATABASE_URL = f"postgresql://postgres:5213@localhost:5432/blog_db"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session