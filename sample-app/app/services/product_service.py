"""Business logic for Product operations.

Enforces business rules (unique SKUs, non-negative stock, existence checks)
on top of the ProductRepository.
"""

import structlog

from app.models.product import Product, ProductCreate
from app.repositories.product_repository import ProductRepository

logger = structlog.get_logger(__name__)


class DuplicateSkuError(Exception):
    """Raised when creating a product with a SKU that already exists."""


class ProductNotFoundError(Exception):
    """Raised when a requested product does not exist."""


class InsufficientStockError(Exception):
    """Raised when a stock adjustment would drop stock below zero."""


class ProductService:
    """Coordinates product operations and enforces business rules."""

    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    async def create_product(self, data: ProductCreate) -> Product:
        """Create a product, rejecting duplicate SKUs.

        Args:
            data: Validated product payload.

        Returns:
            The persisted product.

        Raises:
            DuplicateSkuError: If a product with the same SKU already exists.
        """
        existing = await self._repository.get_by_sku(data.sku)
        if existing is not None:
            logger.warning("product.create.duplicate_sku", sku=data.sku)
            raise DuplicateSkuError(f"SKU '{data.sku}' already exists")

        product = await self._repository.add(data)
        logger.info(
            "product.created",
            product_id=product.id,
            sku=product.sku,
            category=product.category,
        )
        return product

    async def get_product(self, product_id: int) -> Product:
        """Return a product by id.

        Raises:
            ProductNotFoundError: If no product exists with the given id.
        """
        product = await self._repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(f"Product {product_id} not found")
        return product

    async def list_products(
        self, category: str | None = None
    ) -> list[Product]:
        """Return products, optionally filtered by category."""
        products = await self._repository.list_all(category=category)
        return list(products)

    async def adjust_stock(
        self, product_id: int, delta: int, reason: str
    ) -> Product:
        """Increase or decrease a product's stock.

        Args:
            product_id: Target product id.
            delta: Amount to add (positive) or subtract (negative).
            reason: Free-text audit reason for the adjustment.

        Returns:
            The updated product.

        Raises:
            ProductNotFoundError: If the product does not exist.
            InsufficientStockError: If the resulting stock would be negative.
        """
        product = await self.get_product(product_id)
        new_stock = product.stock + delta
        if new_stock < 0:
            logger.warning(
                "product.stock.insufficient",
                product_id=product_id,
                current=product.stock,
                delta=delta,
            )
            raise InsufficientStockError(
                f"Cannot adjust stock by {delta}; current is {product.stock}"
            )

        updated = await self._repository.update_stock(product, new_stock)
        logger.info(
            "product.stock.adjusted",
            product_id=product_id,
            previous=product.stock - delta,
            new=updated.stock,
            reason=reason,
        )
        return updated

    async def delete_product(self, product_id: int) -> None:
        """Delete a product by id.

        Raises:
            ProductNotFoundError: If the product does not exist.
        """
        product = await self.get_product(product_id)
        await self._repository.delete(product)
        logger.info("product.deleted", product_id=product_id)
