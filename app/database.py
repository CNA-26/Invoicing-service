import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")


Base = declarative_base()
engine = None


def get_engine():
    global engine
    if engine is None:
        engine = create_engine(
            DATABASE_URL,
            echo=True,
            pool_pre_ping=True
        )
    return engine


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_engine()
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()