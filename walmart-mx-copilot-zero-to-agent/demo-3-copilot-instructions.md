# Demo 3 Companion - copilot-instructions.md Template
# Usage: Copiar a .github/copilot-instructions.md en el proyecto de demo
# Prerequisites: Repositorio con directorio .github/

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
