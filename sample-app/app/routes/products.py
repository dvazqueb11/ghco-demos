"""FastAPI routes for products."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.product import ProductCreate, ProductRead, StockAdjustment
from app.repositories.product_repository import ProductRepository
from app.services.product_service import (
    DuplicateSkuError,
    InsufficientStockError,
    ProductNotFoundError,
    ProductService,
)

router = APIRouter(prefix="/products", tags=["products"])


def get_service(
    session: AsyncSession = Depends(get_session),
) -> ProductService:
    """Build a `ProductService` wired to the request-scoped session."""
    return ProductService(ProductRepository(session))


@router.get("", response_model=list[ProductRead])
async def list_products(
    category: str | None = Query(default=None),
    service: ProductService = Depends(get_service),
) -> list[ProductRead]:
    """List products, optionally filtered by category."""
    products = await service.list_products(category=category)
    return [ProductRead.model_validate(p) for p in products]


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_service),
) -> ProductRead:
    """Fetch a product by id."""
    try:
        product = await service.get_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    return ProductRead.model_validate(product)


@router.post(
    "", response_model=ProductRead, status_code=status.HTTP_201_CREATED
)
async def create_product(
    payload: ProductCreate,
    service: ProductService = Depends(get_service),
) -> ProductRead:
    """Create a new product."""
    try:
        product = await service.create_product(payload)
    except DuplicateSkuError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc)
        ) from exc
    return ProductRead.model_validate(product)


@router.patch("/{product_id}/stock", response_model=ProductRead)
async def adjust_stock(
    product_id: int,
    payload: StockAdjustment,
    service: ProductService = Depends(get_service),
) -> ProductRead:
    """Adjust stock by a signed delta."""
    try:
        product = await service.adjust_stock(
            product_id=product_id,
            delta=payload.delta,
            reason=payload.reason,
        )
    except ProductNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except InsufficientStockError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
        ) from exc
    return ProductRead.model_validate(product)


@router.delete(
    "/{product_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(
    product_id: int,
    service: ProductService = Depends(get_service),
) -> None:
    """Delete a product by id."""
    try:
        await service.delete_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
