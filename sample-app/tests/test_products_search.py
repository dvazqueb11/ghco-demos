from collections.abc import AsyncIterator
from decimal import Decimal

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import ProductCreate
from app.repositories.product_repository import ProductRepository
from app.routes.products import get_service, router
from app.services.product_service import InvalidPriceRangeError, ProductService


@pytest_asyncio.fixture
async def async_client(db_session: AsyncSession) -> AsyncIterator[AsyncClient]:
    app = FastAPI()
    app.include_router(router)

    service = ProductService(ProductRepository(db_session))

    def override_get_service() -> ProductService:
        return service

    app.dependency_overrides[get_service] = override_get_service

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


async def _create_product(service: ProductService, sku: str, category: str, price: str) -> None:
    """Create a test product with a generated name and default stock.

    Args:
        service: Product service used to persist the product.
        sku: Unique SKU for the product.
        category: Category assigned to the product.
        price: Decimal price represented as string.
    """
    await service.create_product(
        ProductCreate(
            sku=sku,
            name=f"Product {sku}",
            category=category,
            price=Decimal(price),
            stock=10,
        )
    )


@pytest.mark.asyncio
async def test_search_products_con_filtros_retorna_items_ordenados_y_total(
    service: ProductService,
) -> None:
    await _create_product(service, "SKU-001", "tech", "19.99")
    await _create_product(service, "SKU-002", "tech", "49.99")
    await _create_product(service, "SKU-003", "home", "15.00")

    items, total = await service.search_products(
        category="tech",
        min_price=Decimal("10.00"),
        max_price=Decimal("50.00"),
        limit=10,
        offset=0,
    )

    assert total == 2
    assert [item.sku for item in items] == ["SKU-001", "SKU-002"]


@pytest.mark.asyncio
async def test_search_products_rango_invalido_lanza_invalid_price_range_error(
    service: ProductService,
) -> None:
    with pytest.raises(InvalidPriceRangeError):
        await service.search_products(
            category=None,
            min_price=Decimal("100.00"),
            max_price=Decimal("10.00"),
            limit=10,
            offset=0,
        )


@pytest.mark.asyncio
async def test_search_repository_con_paginacion_retorna_items_y_total(
    repository: ProductRepository,
) -> None:
    await repository.add(
        ProductCreate(
            sku="SKU-R-001",
            name="Repo 1",
            category="tech",
            price=Decimal("10.00"),
            stock=1,
        )
    )
    await repository.add(
        ProductCreate(
            sku="SKU-R-002",
            name="Repo 2",
            category="tech",
            price=Decimal("20.00"),
            stock=1,
        )
    )

    items, total = await repository.search(
        category="tech",
        min_price=Decimal("5.00"),
        max_price=Decimal("30.00"),
        limit=1,
        offset=1,
    )

    assert total == 2
    assert len(items) == 1
    assert items[0].sku == "SKU-R-002"


@pytest.mark.asyncio
async def test_search_products_endpoint_con_filtros_retorna_resultado_paginado(
    async_client: AsyncClient,
) -> None:
    await async_client.post(
        "/products",
        json={
            "sku": "SKU-E-001",
            "name": "Earbuds",
            "category": "tech",
            "price": "19.99",
            "stock": 10,
        },
    )
    await async_client.post(
        "/products",
        json={
            "sku": "SKU-E-002",
            "name": "Laptop",
            "category": "tech",
            "price": "999.99",
            "stock": 5,
        },
    )
    await async_client.post(
        "/products",
        json={
            "sku": "SKU-E-003",
            "name": "Cable",
            "category": "tech",
            "price": "29.99",
            "stock": 100,
        },
    )

    response = await async_client.get(
        "/products/search",
        params={
            "category": "tech",
            "min_price": "10",
            "max_price": "50",
            "limit": 1,
            "offset": 1,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 2
    assert len(payload["items"]) == 1
    assert payload["items"][0]["sku"] == "SKU-E-003"


@pytest.mark.asyncio
async def test_search_products_endpoint_con_rango_invalido_retorna_422(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(
        "/products/search",
        params={"min_price": "10", "max_price": "5"},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "min_price must be less than or equal to max_price"
