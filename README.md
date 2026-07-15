# ghco-demos

Repositorio de referencia para trabajar con **GitHub Copilot** sobre un proyecto
Python real. Incluye una API de inventario limpia (FastAPI + SQLAlchemy async),
custom instructions con las convenciones del equipo, una skill personalizada de
Copilot y un pipeline de CI con cobertura.

Pensado para usarse como plantilla o campo de práctica: los archivos siguen
convenciones consistentes que Copilot puede aprender y replicar automáticamente.

---

## Contenido

```
ghco-demos/
├── README.md
├── sample-app/                                 # API de inventario de referencia
│   ├── app/
│   │   ├── main.py                             # FastAPI entrypoint
│   │   ├── database.py                         # Async engine + session factory
│   │   ├── logging_config.py                   # structlog setup
│   │   ├── models/product.py                   # SQLAlchemy + Pydantic schemas
│   │   ├── repositories/product_repository.py  # Repository pattern
│   │   ├── services/product_service.py         # Business logic
│   │   └── routes/products.py                  # CRUD endpoints
│   ├── tests/                                  # conftest.py + espacio para tests
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── README.md
└── .github/
    ├── copilot-instructions.md                 # Convenciones del repo
    ├── PULL_REQUEST_TEMPLATE.md
    ├── ISSUE_TEMPLATE/                         # bug_report + feature_request
    ├── skills/
    │   └── generate-pytest-coverage/           # Skill custom (SKILL.md)
    └── workflows/
        ├── ci.yml                              # pytest + coverage en push/PR
        └── copilot-setup-steps.yml             # Env setup para Copilot Coding Agent
```

---

## Stack

- **Python 3.12**
- **FastAPI** + **Pydantic v2**
- **SQLAlchemy 2.0** async (SQLite por defecto vía `aiosqlite`; PostgreSQL vía `asyncpg`)
- **structlog** para logging estructurado
- **pytest** + **pytest-asyncio** + **pytest-cov** para testing

---

## Quick start

```pwsh
# Clonar
git clone <URL-de-este-repo> ghco-demos
cd ghco-demos\sample-app

# Entorno virtual + dependencias
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Levantar la API
uvicorn app.main:app --reload
```

Swagger UI: <http://localhost:8000/docs>

### Ejecutar tests + coverage

```pwsh
cd sample-app
pytest --cov=app --cov-report=html --cov-report=term-missing -v
```

Reporte HTML en `sample-app/htmlcov/index.html`.

---

## Convenciones del repositorio

El archivo [.github/copilot-instructions.md](.github/copilot-instructions.md)
documenta las reglas que **cualquier código** dentro de este repo debe cumplir.
Copilot las lee automáticamente y las aplica al sugerir cambios.

- **Estilo:** type hints obligatorios, docstrings Google, `snake_case`,
  `PascalCase` para clases, `UPPER_SNAKE_CASE` para constantes.
- **I/O:** siempre `async`/`await`.
- **Errores:** nunca `bare except`; `HTTPException` para errores HTTP.
- **Patrones:** Repository pattern para datos, Pydantic para request/response,
  `structlog` para logging.
- **Tests:** `pytest`, fixtures para setup, mock de servicios externos con
  `unittest.mock`, naming `test_{metodo}_{escenario}_{resultado_esperado}`,
  cobertura mínima **80%**.

El workflow [.github/workflows/ci.yml](.github/workflows/ci.yml) valida estas
reglas en cada push y PR: cualquier PR que baje la cobertura por debajo de 80%
falla el CI.

---

## Skill custom: `generate-pytest-coverage`

El repo incluye una skill para GitHub Copilot que encapsula el flujo completo
de "generar tests unitarios con cobertura" en un solo comando.

Uso en Copilot Chat:

```
/generate-pytest-coverage <ruta/al/archivo.py>
```

La skill genera los tests siguiendo las convenciones del repo, corre
`pytest --cov` y reporta la cobertura obtenida junto con el HTML.

Definición: [.github/skills/generate-pytest-coverage/SKILL.md](.github/skills/generate-pytest-coverage/SKILL.md)

---

## Ejercicios sugeridos

Ver [sample-app/README.md](sample-app/README.md) para una lista de ejercicios
prácticos (agregar endpoints, generar tests, refactors, etc.) mapeados a las
distintas capacidades de GitHub Copilot (Ask Chat, Inline Chat, Agent Mode,
skills, Coding Agent).

---

## Recursos

- Documentación oficial de GitHub Copilot: <https://docs.github.com/copilot>
- Custom instructions: <https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot>
- Agent skills: <https://code.visualstudio.com/docs/copilot/customization/agent-skills>
- Copilot Coding Agent: <https://docs.github.com/en/copilot/using-github-copilot/coding-agent>
- `copilot-setup-steps.yml`: <https://docs.github.com/en/copilot/customizing-copilot/customizing-the-development-environment-for-copilot-coding-agent>
