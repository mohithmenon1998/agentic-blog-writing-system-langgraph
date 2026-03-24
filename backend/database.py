from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
load_dotenv()

import urllib.parse


DB_PWD = os.getenv("DB_PWD")

SUPABASE_DB_PWD = urllib.parse.quote_plus(DB_PWD)

# DATABASE_URL = f"postgresql://postgres:5213@localhost:5432/blog_db"
DATABASE_URL = f"postgresql://postgres.ywrmjjqeerebqhswzzuf:{SUPABASE_DB_PWD}@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session