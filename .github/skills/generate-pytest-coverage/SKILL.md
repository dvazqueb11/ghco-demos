---
name: generate-pytest-coverage
description: 'Generate pytest tests for a Python file and run them with pytest-cov to produce an HTML coverage report. USE FOR: generate pytest, generate tests for python file, write unit tests, create pytest tests, add tests with coverage, run pytest with coverage, coverage report, pytest-cov, htmlcov, verify coverage, missing coverage, uncovered lines, test a python module, achieve 80% coverage. Follows repo conventions (Google docstrings, type hints, snake_case, async/await with pytest-asyncio, mock external I/O, test_{metodo}_{escenario}_{resultado} naming, 80% minimum coverage). DO NOT USE FOR: generating non-pytest tests (unittest, nose), JS/TS tests, load tests, or coverage on non-Python code.'
argument-hint: '<path/to/target_file.py>'
---

# Generate pytest Tests + Coverage Report

Generate pytest tests for a target Python file, execute them with `pytest-cov`, iterate until coverage meets the repo minimum (80%), and deliver a linkable HTML report.

## When to Use

Trigger on requests like:
- "generate tests for `product_service.py`"
- "add pytest tests with coverage"
- "test this file and show me coverage"
- "get me to 80% coverage on `<module>`"
- "run pytest with coverage report"

Do **not** use for: non-pytest frameworks, non-Python code, or when the user only wants to run existing tests without generating new ones (just run `pytest --cov` directly).

## Prerequisites

- Python 3.12
- Install if missing:
  ```pwsh
  pip install pytest pytest-cov pytest-asyncio
  ```
- Repo conventions from `.github/copilot-instructions.md` apply. Test-file conventions from `.github/instructions/*.instructions.md` (if present) override these.

## Procedure

### 1. Identify the target

- Take the file path from the argument. If none provided, use the currently open editor file.
- Reject if the target is not a `.py` file or does not exist.
- Derive the module import path from the file location relative to the project root (e.g. `src/services/product_service.py` → `src.services.product_service`).

### 2. Analyze the module

Read the target file end-to-end and enumerate:
- Public functions/classes (skip anything prefixed with `_`).
- Signatures: parameters, defaults, return types, `async def` vs `def`.
- Branches: `if/elif/else`, `try/except`, early returns, guard clauses.
- Side effects to mock: DB calls, HTTP, filesystem, `datetime.now()`, random, env vars.
- Exceptions raised explicitly.

### 3. Generate the test file

- Path: `tests/test_<module_name>.py` (create `tests/` and `tests/__init__.py` if missing; also create `tests/conftest.py` if fixtures are shared).
- Follow these conventions strictly:
  - Test names: `test_{metodo}_{escenario}_{resultado_esperado}` (e.g. `test_process_order_stock_insuficiente_returns_error`).
  - Every test function has a one-line Google-style docstring describing scenario and expected outcome.
  - Type-hint fixtures and helpers.
  - `@pytest.mark.parametrize` for enumerable input variations (discount codes, boundary values, etc.).
  - `pytest.raises(ExceptionType)` for error paths — never a bare `assert False` in `try/except`.
  - `unittest.mock.patch` (or `mocker` if `pytest-mock` is available) for external I/O; never call real network/DB/filesystem.
  - `@pytest.mark.asyncio` for async targets. If most tests are async, add `asyncio_mode = "auto"` to `pyproject.toml`/`pytest.ini` instead.
  - No `time.sleep()`; use `freezegun` or mock `datetime.now()`.
  - Assertion messages when the failure would be ambiguous: `assert result.status == "completed", f"expected completed, got {result.status}"`.
  - Split unit vs integration tests into `tests/unit/` and `tests/integration/` if both exist.

- Coverage checklist per public callable:
  - [ ] Happy path (valid inputs → expected output).
  - [ ] Each explicit branch / discount code / status code.
  - [ ] Boundary values (0, -1, empty string, `None`, empty collection, max int).
  - [ ] Every `raise` and every `except` path.
  - [ ] Idempotency / side-effect assertions (stock decremented, counter incremented, mock called with expected args).

### 4. Run tests with coverage

From the project root:

```pwsh
pytest tests/test_<module_name>.py `
  --cov=<module.dotted.path> `
  --cov-report=html `
  --cov-report=term-missing `
  -v
```

Notes:
- `--cov-report=html` writes `htmlcov/index.html` (the deliverable).
- `--cov-report=term-missing` prints uncovered line numbers in the terminal — required so the skill can decide whether to iterate. Do **not** drop it.
- If the module is at repo root, use `--cov=<module_name>` (no dots).
- Add `--cov-fail-under=80` on the final run to fail loudly if the repo minimum is not met.

### 5. Iterate until ≥ 80% coverage

- Parse the `term-missing` output. For each file below 80%, read the listed line ranges and generate targeted tests for those branches.
- Re-run pytest. Cap at 3 iterations — if still under 80%, stop and report the uncovered lines to the user with a short explanation (dead code, unreachable branch, requires integration test, etc.) rather than fabricating tests.

### 6. Report back

Deliver in the chat response:
- File(s) created/modified (as workspace-relative markdown links).
- Test count and pass/fail summary.
- Final coverage percentage per file and overall.
- Path to the HTML report as a link: `htmlcov/index.html`.
- Any uncovered lines that were intentionally left out, with the reason.
- Next-step suggestion (e.g. "add an integration test with a real DB fixture for the SQLAlchemy path").

## Output Contract

```
Generated: tests/test_<module>.py (<N> tests)
Result:    <passed>/<total> passed
Coverage:  <pct>% (target 80%)
Report:    htmlcov/index.html
Uncovered: <file>:<lines>  — <reason>  (only if any)
Next:      <one concrete suggestion>
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError` on the target | `tests/` not on `sys.path` | Add empty `tests/__init__.py` and/or `conftest.py` at repo root; verify `pyproject.toml` has `[tool.pytest.ini_options] pythonpath = ["."]`. |
| `PytestUnhandledCoroutineWarning` | Async test without marker | Add `@pytest.mark.asyncio` or set `asyncio_mode = "auto"` in `pyproject.toml`. |
| Coverage shows 0% | `--cov` path wrong | Use the dotted module path (`src.services.product_service`), not the file path. |
| HTML report not generated | `pytest-cov` not installed | `pip install pytest-cov`. |
| Coverage stuck below 80% | Genuinely unreachable code | Report it — do not silence with `# pragma: no cover` unless the user approves. |
| Mocks leak between tests | Missing teardown | Use `monkeypatch` fixture or `with patch(...)` context managers instead of module-level `patch`. |

## Anti-patterns

- Do not generate tests that only assert `assert result is not None` — assert the specific value.
- Do not import from `tests.*` in production code.
- Do not disable coverage with `# pragma: no cover` to hit the 80% number.
- Do not add `time.sleep()` to work around flaky async tests.
- Do not commit `htmlcov/`, `.coverage`, or `__pycache__/` — add to `.gitignore` if missing.
