import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv(".env.local")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./job_tracker.db"
)

# Поддержка PostgreSQL через psycopg 3
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg://",
        1
    )
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

engine_kwargs = {"pool_pre_ping": True}

# Настройки SQLite
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {
        "check_same_thread": False
    }

engine = create_engine(
    DATABASE_URL,
    **engine_kwargs
)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def create_test_database():
    test_engine = create_engine(
        "sqlite:///./test_job_tracker.db",
        connect_args={"check_same_thread": False}
    )

    TestSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False
    )

    return test_engine, TestSessionLocal