"""Repository pattern for Product persistence."""

from collections.abc import Sequence
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product, ProductCreate


class ProductRepository:
    """Data access layer for the `products` table.

    All methods are `async` and require an `AsyncSession` provided at
    construction time. The repository does not commit — callers own the
    transaction boundary.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, product_id: int) -> Product | None:
        """Return a product by primary key, or `None` if not found."""
        return await self._session.get(Product, product_id)

    async def get_by_sku(self, sku: str) -> Product | None:
        """Return a product by its unique SKU, or `None` if not found."""
        stmt = select(Product).where(Product.sku == sku)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(
        self, category: str | None = None
    ) -> Sequence[Product]:
        """List products, optionally filtered by category.

        Args:
            category: Exact category to filter by. If `None`, returns all rows.

        Returns:
            Sequence of `Product` ordered by ascending id.
        """
        stmt = select(Product).order_by(Product.id.asc())
        if category is not None:
            stmt = stmt.where(Product.category == category)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def add(self, data: ProductCreate) -> Product:
        """Insert a new product and flush the session.

        Args:
            data: Validated payload.

        Returns:
            The persisted `Product` with `id` populated.
        """
        product = Product(**data.model_dump())
        self._session.add(product)
        await self._session.flush()
        return product

    async def update_stock(self, product: Product, new_stock: int) -> Product:
        """Persist a stock change for `product`.

        Args:
            product: Attached ORM instance.
            new_stock: New absolute stock value (must be non-negative).

        Returns:
            The updated `Product`.
        """
        product.stock = new_stock
        await self._session.flush()
        return product

    async def delete(self, product: Product) -> None:
        """Delete `product` from the session."""
        await self._session.delete(product)

    async def search(
        self,
        category: str | None,
        min_price: Decimal | None,
        max_price: Decimal | None,
        limit: int,
        offset: int,
    ) -> tuple[Sequence[Product], int]:
        """Search products by optional filters with pagination.

        Args:
            category: Exact category filter, or `None` to include all.
            min_price: Lower inclusive price bound, or `None`.
            max_price: Upper inclusive price bound, or `None`.
            limit: Maximum number of rows to return.
            offset: Number of rows to skip before returning results.

        Returns:
            A tuple with:
            - Sequence of matching `Product` rows ordered by price ascending.
            - Total number of matching rows before pagination.
        """
        filters = []
        if category is not None:
            filters.append(Product.category == category)
        if min_price is not None:
            filters.append(Product.price >= min_price)
        if max_price is not None:
            filters.append(Product.price <= max_price)

        stmt = (
            select(Product)
            .where(*filters)
            .order_by(Product.price.asc())
            .limit(limit)
            .offset(offset)
        )
        count_stmt = select(func.count()).select_from(Product).where(*filters)
        result = await self._session.execute(stmt)
        count_result = await self._session.execute(count_stmt)
        total = count_result.scalar_one()
        return result.scalars().all(), total
