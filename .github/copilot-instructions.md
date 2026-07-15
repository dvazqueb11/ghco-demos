## Stack Tecnologico

- Python 3.12 con FastAPI y Pydantic v2
- Base de datos: PostgreSQL con SQLAlchemy 2.0 (async)
- Tests: pytest con pytest-asyncio
- Dependency injection con FastAPI Depends

## Convenciones de Codigo

- Type hints obligatorios en todas las funciones (PEP 484)
- Docstrings en formato Google (PEP 257) para funciones publicas
- Variables y funciones en snake_case
- Clases en PascalCase
- Constantes en UPPER_SNAKE_CASE
- Async/await para todas las operaciones de I/O

## Patrones

- Repository pattern para acceso a datos
- Pydantic models para request/response validation
- HTTPException para manejo de errores HTTP
- Structured logging con structlog
- Nunca usar bare except, siempre especificar la excepcion

## Tests

- pytest como framework de testing
- Fixtures para setup de datos
- Mock de servicios externos con unittest.mock
- Nombres: test_{metodo}_{escenario}_{resultado_esperado}
- Cobertura minima: 80%

## Estructura del Proyecto

- Aplicacion de referencia (usar como target para nuevos features y tests): `sample-app/`
  - Codigo: `sample-app/app/` (routes, services, repositories, models)
  - Tests: `sample-app/tests/`
  - Setup: `cd sample-app && pip install -r requirements.txt`
  - Ejecutar tests: `cd sample-app && pytest --cov=app --cov-report=term-missing`
- CI corre pytest + coverage sobre `sample-app/` en cada push/PR — todo PR debe pasar CI verde con cobertura >= 80%