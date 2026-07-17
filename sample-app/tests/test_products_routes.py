from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.product_repository import ProductRepository
from app.routes.products import get_service, router
from app.services.product_service import ProductService


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


@pytest.mark.asyncio
async def test_product_routes_crud_flow_covers_main_cases(
    async_client: AsyncClient,
) -> None:
    create_response = await async_client.post(
        "/products",
        json={
            "sku": "SKU-C-001",
            "name": "Chair",
            "category": "home",
            "price": "49.90",
            "stock": 3,
        },
    )

    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    duplicate_response = await async_client.post(
        "/products",
        json={
            "sku": "SKU-C-001",
            "name": "Chair Duplicate",
            "category": "home",
            "price": "50.00",
            "stock": 1,
        },
    )
    assert duplicate_response.status_code == 409

    get_response = await async_client.get(f"/products/{product_id}")
    assert get_response.status_code == 200

    list_response = await async_client.get("/products", params={"category": "home"})
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    adjust_ok_response = await async_client.patch(
        f"/products/{product_id}/stock",
        json={"delta": 2, "reason": "restock"},
    )
    assert adjust_ok_response.status_code == 200
    assert adjust_ok_response.json()["stock"] == 5

    adjust_fail_response = await async_client.patch(
        f"/products/{product_id}/stock",
        json={"delta": -10, "reason": "oversell"},
    )
    assert adjust_fail_response.status_code == 422

    not_found_stock_response = await async_client.patch(
        "/products/999/stock",
        json={"delta": 1, "reason": "test"},
    )
    assert not_found_stock_response.status_code == 404

    delete_response = await async_client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 204

    delete_missing_response = await async_client.delete("/products/999")
    assert delete_missing_response.status_code == 404

    get_missing_response = await async_client.get("/products/999")
    assert get_missing_response.status_code == 404
