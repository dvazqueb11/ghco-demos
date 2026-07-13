# Sample App — Inventory API

FastAPI + SQLAlchemy 2.0 async + Pydantic v2. Sigue las convenciones de
[`.github/copilot-instructions.md`](../.github/copilot-instructions.md) al pie de la letra
para que sirva como **referencia** y como **campo de práctica** para los ejercicios de Copilot.

## Layout

```
sample-app/
├── app/
│   ├── main.py                     # FastAPI app + startup
│   ├── database.py                 # Async engine + session factory
│   ├── logging_config.py           # structlog setup
│   ├── models/product.py           # SQLAlchemy model + Pydantic schemas
│   ├── repositories/product_repository.py   # Repository pattern
│   ├── services/product_service.py # Business logic
│   └── routes/products.py          # CRUD endpoints
├── tests/                          # Casi vacío a propósito — para practicar
│   └── conftest.py
├── requirements.txt
└── pyproject.toml                  # pytest + coverage config
```

## Setup

```pwsh
cd sample-app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abre <http://localhost:8000/docs> para el Swagger UI.

## Ejercicios sugeridos con Copilot

Los archivos están diseñados para practicar cada capacidad del workshop.

| # | Ejercicio | Archivo objetivo | Capacidad de Copilot |
|---|---|---|---|
| 1 | Generar tests unitarios con cobertura ≥ 80% para el service | [`app/services/product_service.py`](app/services/product_service.py) | Skill `/generate-pytest-coverage` |
| 2 | Agregar endpoint `GET /products/search?category=&min_price=&max_price=` | [`app/routes/products.py`](app/routes/products.py) | Agent Mode |
| 3 | Documentar todas las funciones públicas del repository con docstrings Google | [`app/repositories/product_repository.py`](app/repositories/product_repository.py) | Inline Chat |
| 4 | Refactorizar `adjust_stock` para emitir un evento estructurado con `structlog` | [`app/services/product_service.py`](app/services/product_service.py) | Inline Chat |
| 5 | Crear un modelo `Order` con su repository, service y routes | (nuevos archivos) | Agent Mode + Custom Instructions |
| 6 | Agregar validación Pydantic v2: `sku` debe ser alfanumérico, precio ≤ 1e6 | [`app/models/product.py`](app/models/product.py) | Ask Chat |

## Ejecutar tests + coverage

```pwsh
pytest --cov=app --cov-report=html --cov-report=term-missing -v
```

El reporte HTML queda en `htmlcov/index.html`.

## Base de datos

Por defecto usa **SQLite async** (`aiosqlite`) con un archivo `inventory.db` local — cero setup.
Para apuntar a PostgreSQL, define:

```pwsh
$env:DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/inventory"
```
