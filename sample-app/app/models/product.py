"""SQLAlchemy ORM model and Pydantic schemas for Product."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Product(Base):
    """Product row in the inventory table."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(64), index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class ProductCreate(BaseModel):
    """Payload for creating a product."""

    sku: str = Field(min_length=3, max_length=32)
    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=64)
    price: Decimal = Field(gt=Decimal("0"))
    stock: int = Field(default=0, ge=0)


class ProductRead(BaseModel):
    """Response schema for a product."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    name: str
    category: str
    price: Decimal
    stock: int
    created_at: datetime


class ProductSearchResult(BaseModel):
    """Paginated search response with total count."""

    total: int = Field(
        ge=0,
        description="Total matching products before applying limit/offset.",
    )
    items: list[ProductRead]


class StockAdjustment(BaseModel):
    """Payload for adjusting a product's stock (positive or negative delta)."""

    delta: int = Field(description="Positive to add, negative to subtract.")
    reason: str = Field(min_length=1, max_length=200)
