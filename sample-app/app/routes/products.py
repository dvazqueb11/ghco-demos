"""FastAPI routes for products."""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.product import (
    ProductCreate,
    ProductRead,
    ProductSearchResult,
    StockAdjustment,
)
from app.repositories.product_repository import ProductRepository
from app.services.product_service import (
    DuplicateSkuError,
    InvalidPriceRangeError,
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


@router.get("/search", response_model=ProductSearchResult)
async def search_products(
    category: str | None = Query(default=None),
    min_price: Decimal | None = Query(default=None, ge=Decimal("0")),
    max_price: Decimal | None = Query(default=None, ge=Decimal("0")),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ProductService = Depends(get_service),
) -> ProductSearchResult:
    """Search products by optional category and price range."""
    try:
        items, total = await service.search_products(
            category=category,
            min_price=min_price,
            max_price=max_price,
            limit=limit,
            offset=offset,
        )
    except InvalidPriceRangeError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
        ) from exc

    return ProductSearchResult(
        total=total,
        items=[ProductRead.model_validate(item) for item in items],
    )


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
