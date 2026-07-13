"""Async database engine and session management using SQLAlchemy 2.0."""

import os
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL: str = os.getenv(
    "DATABASE_URL", "sqlite+aiosqlite:///./inventory.db"
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""


async def get_session() -> AsyncIterator[AsyncSession]:
    """Yield an async database session (FastAPI dependency).

    Yields:
        An `AsyncSession` bound to the shared engine. The session is
        closed automatically when the request finishes.
    """
    async with async_session_factory() as session:
        yield session


async def init_db() -> None:
    """Create all tables declared on `Base.metadata`.

    Safe to call multiple times; existing tables are not modified.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
