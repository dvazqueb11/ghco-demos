# GitHub Copilot Zero to Agent — Workshop Demos

Repositorio de soporte para el workshop **GitHub Copilot: Zero to Agent (L300)** — Walmart Mexico.

## Estructura

```
├── walmart-mx-copilot-zero-to-agent-demos.md   # Guía completa de las 5 demos
├── walmart-mx-copilot-zero-to-agent/           # Companion scripts por demo
│   ├── demo-1-product-service.py               # Código Python sin optimizar (Demo 1)
│   ├── demo-3-copilot-instructions.md          # Template copilot-instructions.md
│   └── demo-3-test-instructions.md             # Template *.instructions.md
├── sample-app/                                 # App de referencia (FastAPI + SQLAlchemy async)
│   ├── app/                                    # main, routes, services, repositories, models
│   ├── tests/                                  # conftest.py (tests reales los generan los attendees)
│   └── README.md                               # Setup y ejercicios sugeridos
└── .github/
    ├── copilot-instructions.md                 # Convenciones del repo (Demo 3)
    ├── PULL_REQUEST_TEMPLATE.md
    ├── ISSUE_TEMPLATE/                         # Templates para Demo 4/5
    ├── SEED_ISSUES.md                          # Comandos gh para pre-poblar issues (Demo 4/5)
    ├── skills/
    │   └── generate-pytest-coverage/           # Skill custom (SKILL.md)
    └── workflows/
        ├── ci.yml                              # pytest + coverage on push/PR (Demo 5)
        └── copilot-setup-steps.yml             # Env setup para Cloud Agent (Demo 5)
```

## Mapa demo → activos

| Demo | Qué se usa de este repo |
|------|-------------------------|
| 1. Chat + Inline Chat | `walmart-mx-copilot-zero-to-agent/demo-1-product-service.py` |
| 2. Agent Mode | Directorio vacío nuevo (fuera de este repo) |
| 3. Custom Instructions | `.github/copilot-instructions.md` + `sample-app/` como campo de práctica |
| 4. GitHub MCP Server | Issues/PRs creados con `.github/SEED_ISSUES.md` |
| 5. Cloud Agent | Issue de `.github/SEED_ISSUES.md` §3 + `sample-app/` como target + `.github/workflows/*` |

## Setup del repo en GitHub (antes del workshop)

```pwsh
# 1. Crear repo en GitHub y publicar
gh repo create walmart-mx-copilot-demos --public --source=. --remote=origin --push

# 2. Habilitar Copilot Coding Agent en la organización / repo
#    Settings → Copilot → Coding agent

# 3. Pre-poblar issues para Demo 4 y 5
#    Ver .github/SEED_ISSUES.md

# 4. Verificar que CI corre verde
gh workflow run ci.yml
gh run watch
```

## Setup local del sample-app

```pwsh
cd sample-app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Ver [sample-app/README.md](sample-app/README.md) para los ejercicios sugeridos.

## Skill custom

El repo incluye una skill `generate-pytest-coverage` que se activa en chat con
`/generate-pytest-coverage <path/to/file.py>` o automáticamente cuando pides
"genera tests con cobertura". Vive en [.github/skills/generate-pytest-coverage/SKILL.md](.github/skills/generate-pytest-coverage/SKILL.md).
