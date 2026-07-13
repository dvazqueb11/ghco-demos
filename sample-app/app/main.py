"""FastAPI application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.logging_config import configure_logging
from app.routes import products


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Configure logging and create tables at startup."""
    configure_logging()
    await init_db()
    yield


app = FastAPI(
    title="Inventory API",
    version="0.1.0",
    description=(
        "Sample FastAPI + SQLAlchemy 2.0 async application for the "
        "GitHub Copilot Zero to Agent workshop."
    ),
    lifespan=lifespan,
)

app.include_router(products.router)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}
