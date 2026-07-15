"""Core SQLAlchemy database configuration for the Meeting Notes Manager."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"
DEFAULT_DATABASE_URL = "sqlite:///./meeting_notes.db"

load_dotenv(ENV_FILE)

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def _build_connect_args(database_url: str) -> dict[str, bool]:
    """Return engine connection arguments for the configured database."""
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


engine = create_engine(
    DATABASE_URL,
    connect_args=_build_connect_args(DATABASE_URL),
    future=True,
)


if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def _configure_sqlite_connection(dbapi_connection, connection_record) -> None:
        """Enable SQLite settings needed for local development."""
        del connection_record
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=MEMORY")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA busy_timeout=5000")
        cursor.close()


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""


def initialize_database() -> None:
    """Create database tables for all registered ORM models."""
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
