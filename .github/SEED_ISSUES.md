# Seed Issues & PRs para Demos 4 y 5

Ejecutar **antes** de las demos para pre-poblar el repo con contenido que los
attendees puedan ver. Requiere [`gh`](https://cli.github.com/) autenticado y
haber hecho `git remote add origin ...` + `git push` primero.

## 1. Verificar setup

```pwsh
gh auth status
gh repo view --json name,owner
```

## 2. Crear issues para Demo 4 (GitHub MCP Server)

Estos issues dan al presenter algo real que consultar cuando pida
`Lista los issues abiertos de este repositorio y dame un resumen de cada uno`.

```pwsh
# Issue 1 — feature request
gh issue create `
  --title "Agregar filtro por rango de precio en /products" `
  --label "enhancement" `
  --body "Permitir filtrar productos con query params ``min_price`` y ``max_price`` en el endpoint GET /products. Debe validar min_price <= max_price."

# Issue 2 — bug report
gh issue create `
  --title "PATCH /products/{id}/stock devuelve 500 cuando delta es cero" `
  --label "bug" `
  --body "Al enviar ``{'delta': 0, 'reason': 'no-op'}``, el service debería aceptar el request como no-op en lugar de fallar. Reproducible en commit main."

# Issue 3 — docs
gh issue create `
  --title "Documentar el flujo de adjust_stock con un diagrama en el README" `
  --label "documentation" `
  --body "Agregar diagrama Mermaid al README del sample-app mostrando el flujo Repository → Service → Route para adjust_stock."

# Issue 4 — refactor
gh issue create `
  --title "Extraer excepciones custom del service a app/exceptions.py" `
  --label "refactor" `
  --body "Mover DuplicateSkuError, ProductNotFoundError, InsufficientStockError a un módulo dedicado para reutilizar entre services."
```

## 3. Crear el issue de Demo 5 (Cloud Agent)

Este es el issue que se le asigna a Copilot en vivo. **No lo asignes ahora** —
solo créalo. Durante la demo, el presenter lo asigna a `@Copilot` frente a la
audiencia.

```pwsh
gh issue create `
  --title "Agregar endpoint de búsqueda de productos por categoría y precio" `
  --label "enhancement" `
  --body @"
Agregar un nuevo endpoint ``GET /products/search`` al sample-app que permita:

- Filtrar por ``category`` (query param, opcional)
- Filtrar por rango de precio: ``min_price`` y ``max_price`` (opcionales, Decimal >= 0)
- Paginación: ``limit`` (default 20, máx 100) y ``offset`` (default 0)
- Ordenar por ``price`` ascendente

## Criterios de aceptación

- [ ] Nueva ruta en ``sample-app/app/routes/products.py``
- [ ] Método ``search`` en ``ProductRepository`` que arme el query con SQLAlchemy 2.0 (select + where + limit + offset)
- [ ] Método ``search_products`` en ``ProductService`` con validación (min_price <= max_price)
- [ ] Nuevo Pydantic schema ``ProductSearchResult`` con lista + total count
- [ ] Tests en ``sample-app/tests/`` con cobertura ≥ 80% del código nuevo
- [ ] Manejo de errores con HTTPException 422 si min_price > max_price
- [ ] CI verde

## Referencias

- Convenciones: ``.github/copilot-instructions.md``
- Módulo objetivo: ``sample-app/app/``
- Ejecutar tests: ``cd sample-app && pytest --cov=app --cov-report=term-missing``
"@
```

## 4. Crear un PR de ejemplo para Demo 4 (opcional)

Si quieres que el presenter pueda mostrar `Analiza el PR #N`, abre un PR
trivial antes de la demo:

```pwsh
git checkout -b docs/root-readme-typo
# Editar README.md a mano — corregir un typo, agregar una línea
git add README.md
git commit -m "docs: corregir typo en README"
git push -u origin docs/root-readme-typo
gh pr create `
  --title "docs: corregir typo en README" `
  --body "Fix menor de documentación para tener un PR abierto durante la demo del MCP."
git checkout main
```

## 5. Cleanup post-workshop (opcional)

```pwsh
# Cerrar todos los issues abiertos creados en la demo
gh issue list --state open --json number --jq '.[].number' | ForEach-Object {
  gh issue close $_
}
```
