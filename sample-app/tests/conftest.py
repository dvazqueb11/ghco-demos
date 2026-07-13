"""Shared pytest fixtures for the sample-app test suite.

Deliberadamente minimo: los estudiantes usaran la skill
`/generate-pytest-coverage` para generar los tests reales.
"""

from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.database import Base
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService


@pytest_asyncio.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    """Provide an isolated in-memory SQLite session per test."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.fixture
def repository(db_session: AsyncSession) -> ProductRepository:
    """Return a `ProductRepository` bound to the test session."""
    return ProductRepository(db_session)


@pytest.fixture
def service(repository: ProductRepository) -> ProductService:
    """Return a `ProductService` wired with the test repository."""
    return ProductService(repository)
