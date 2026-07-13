# GitHub Copilot: Zero to Agent - L300 Demo Guide

**Topic:** GitHub Copilot Zero to Agent Workshop
**Level:** L300
**Demos:** 5 x ~8-10 minutes
**Customer:** Walmart Mexico
**Presenter:** Diego Vazquez, Cloud Solutions Architect

---

## Demo Overview

| # | Demo | Duration | Key Skill | WOW Moment |
|---|------|----------|-----------|------------|
| 1 | Chat + Inline Chat | ~8 min | Prompt Engineering | Copilot refactoriza y genera tests en segundos |
| 2 | Agent Mode - API REST | ~10 min | Autonomous Coding | Copilot crea una API completa de cero |
| 3 | Custom Instructions | ~7 min | Personalization | Copilot sigue las convenciones del equipo automaticamente |
| 4 | MCP Server | ~7 min | Extensibility | Copilot consulta Issues y PRs sin salir del IDE |
| 5 | Cloud Agent | ~8 min | Full Autonomy | Copilot resuelve un issue y crea un PR de forma autonoma |

## Environment Setup

### Prerequisites

- VS Code con la extension GitHub Copilot (ultima version)
- Python 3.11+ con pip
- GitHub CLI (`gh`) autenticado
- Repositorio de demo preparado (ver companion scripts)
- Cuenta GitHub con Copilot Enterprise o Business habilitado
- Acceso a Cloud Agent habilitado en la organizacion

### Pre-Demo Checklist

- [ ] VS Code abierto con tema oscuro
- [ ] Font size minimo 16pt en el editor (Ctrl+= para zoom)
- [ ] Terminal visible en VS Code
- [ ] Copilot Chat panel cerrado (se abre durante la demo)
- [ ] Repositorio de demo clonado y listo
- [ ] Archivos de ejemplo preparados (ver scripts companion)
- [ ] Internet estable (MCP y Cloud Agent requieren conexion)
- [ ] Pestanas del navegador preparadas para Demo 4 y 5

---

## Demo 1: Chat + Inline Chat con Python

[*] WOW moment: Copilot refactoriza codigo complejo y genera tests con cobertura completa en menos de 2 minutos.

### Prerequisites

- Archivo `product_service.py` con codigo Python sin optimizar (ver companion script)
- VS Code con el archivo abierto

### Steps

**1. Mostrar el codigo inicial**

> Say this: "Vamos a empezar con un servicio de productos que tiene algunos problemas de calidad. Veamos como Copilot Chat nos ayuda a mejorarlo."

- Abrir `product_service.py` en VS Code
- Mostrar brevemente el codigo (funcion larga, sin type hints, sin docstrings)

**2. Usar Chat Panel para analisis**

> Say this: "Primero, voy a usar el panel de Chat para pedirle a Copilot que analice este codigo. Noten como le doy contexto con el participante @workspace."

- Abrir Chat panel (Ctrl+Shift+I o icono de chat)
- Escribir: `@workspace Analiza product_service.py. Identifica problemas de calidad, patrones anti-patron, y sugiere mejoras concretas.`
- Esperar respuesta y comentar los hallazgos

**3. Refactorizar con Inline Chat**

> Say this: "Ahora voy a usar Inline Chat para aplicar una de las mejoras. Selecciono la funcion que quiero refactorizar y uso Ctrl+I."

- Seleccionar la funcion `process_order` completa
- Presionar Ctrl+I
- Escribir: `Refactoriza esta funcion: extrae la validacion a funciones separadas, agrega type hints, y maneja errores con excepciones custom`
- Aceptar el cambio y mostrar la diferencia

**4. Generar Docstrings**

> Say this: "Con una sola instruccion, vamos a generar docstrings para todas las funciones del archivo."

- Seleccionar todo el archivo (Ctrl+A)
- Ctrl+I: `Agrega docstrings en formato Google a todas las funciones`
- Aceptar y mostrar el resultado

**5. Generar Tests**

> Say this: "Y para cerrar, vamos a generar tests unitarios. Copilot conoce el contexto del archivo porque lo tiene abierto."

- En el Chat panel: `/tests Genera tests unitarios con pytest para product_service.py. Incluye casos edge como precios negativos y nombres vacios.`
- Mostrar los tests generados
- Ejecutar: `pytest test_product_service.py -v`

### Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Chat no responde | Extension desactualizada | Recargar VS Code (Ctrl+Shift+P > Reload) |
| Inline Chat no aparece | Shortcut bloqueado | Usar Command Palette > Copilot: Inline Chat |
| Tests fallan al ejecutar | Dependencias faltantes | `pip install pytest` antes de la demo |

> Transition: "Ahora que dominamos Chat, vamos a ver que pasa cuando le damos a Copilot la capacidad de actuar de forma autonoma con Agent Mode."

---

## Demo 2: Agent Mode - API REST con FastAPI

[*] WOW moment: Copilot crea una API REST completa con multiples archivos, ejecuta tests, y corrige errores automaticamente.

### Prerequisites

- Carpeta vacia o con un README basico
- Python 3.11+ disponible
- pip instalado

### Steps

**1. Activar Agent Mode**

> Say this: "Agent Mode es donde Copilot deja de sugerir y empieza a actuar. Noten que en el dropdown del chat, selecciono 'Agent' en lugar de 'Ask' o 'Edit'."

- En VS Code, abrir el Chat panel
- Cambiar el dropdown de "Ask" a "Agent"
- Mostrar que el icono cambia

**2. Dar la tarea**

> Say this: "Voy a darle una tarea completa. Noten que soy muy especifico en lo que quiero: el framework, la estructura, y los tests."

- Escribir el prompt:
```
Crea una API REST con FastAPI para gestion de inventario.
Estructura:
- models/product.py - Modelo Pydantic: id, nombre, precio, stock, categoria
- routes/products.py - Endpoints CRUD (GET all, GET by id, POST, PUT, DELETE)
- main.py - App FastAPI con router incluido
- tests/test_products.py - Tests con pytest para cada endpoint
- requirements.txt - Dependencias
Usa un diccionario en memoria como storage temporal.
Incluye validacion: precio > 0, stock >= 0, nombre no vacio.
```

**3. Observar el proceso**

> Say this: "Observen como Copilot primero planifica lo que va a hacer, luego crea los archivos uno por uno, y nos pide aprobacion para cada accion."

- No interrumpir el flujo
- Comentar cada paso: "Ahi esta creando el modelo...", "Ahora los endpoints...", "Va a instalar las dependencias..."
- Aprobar cada accion cuando Copilot lo solicite

**4. Ver la ejecucion de tests**

> Say this: "Ahora va a ejecutar los tests. Si algo falla, van a ver como corrige automaticamente."

- Dejar que Agent Mode ejecute `pytest`
- Si hay errores, mostrar como itera y corrige
- Mostrar el resultado final: tests pasando

**5. Probar la API**

> Say this: "Vamos a probar que la API funciona."

- Ejecutar: `uvicorn main:app --reload`
- Abrir `http://localhost:8000/docs` en el navegador
- Mostrar Swagger UI generado automaticamente
- Hacer un POST para crear un producto

### Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Agent Mode no disponible | Plan sin acceso | Verificar licencia Copilot |
| Tests fallan en loop | Bug en logica generada | Dar hint: "El test espera status 200 pero el endpoint devuelve 201" |
| uvicorn no encontrado | No instalado | `pip install uvicorn fastapi` |

> Transition: "Impresionante, verdad? Pero imaginen si Copilot ademas supiera las convenciones especificas de su equipo. Eso es exactamente lo que vamos a configurar ahora."

---

## Demo 3: Custom Instructions para Python

[*] WOW moment: Copilot cambia completamente su estilo de codigo al activar las instrucciones del equipo.

### Prerequisites

- Repositorio de demo con codigo Python
- Sin archivo copilot-instructions.md existente

### Steps

**1. Generar codigo SIN instrucciones**

> Say this: "Primero, vamos a ver como genera codigo Copilot sin ninguna instruccion personalizada. Le voy a pedir que cree un servicio."

- En Chat (Ask mode): `Crea una funcion Python que conecte a una base de datos PostgreSQL y obtenga una lista de usuarios`
- Mostrar el resultado (probablemente sin type hints, sin docstrings estandarizadas)
- Guardar mentalmente el estilo

**2. Crear copilot-instructions.md**

> Say this: "Ahora vamos a crear las instrucciones del equipo. Este archivo le dice a Copilot como debe escribir codigo en este repositorio."

- Crear `.github/copilot-instructions.md` (usar companion script o escribir manualmente):

```markdown
## Convenciones Python

- Python 3.12 con type hints obligatorios (PEP 484)
- Docstrings en formato Google (PEP 257)
- Async/await para operaciones de I/O
- SQLAlchemy 2.0 con async sessions
- Pydantic v2 para validacion
- Manejo de errores: nunca usar bare except
- Logging con structlog (structured logging)
- Variables y funciones en snake_case
- Constantes en UPPER_SNAKE_CASE
```

**3. Generar codigo CON instrucciones**

> Say this: "Ahora voy a hacer exactamente la misma peticion. Vean la diferencia."

- Misma peticion: `Crea una funcion Python que conecte a una base de datos PostgreSQL y obtenga una lista de usuarios`
- Mostrar la diferencia: type hints, docstrings, async/await, SQLAlchemy 2.0
- Resaltar las diferencias lado a lado

**4. Crear instrucciones por ruta**

> Say this: "Podemos ir un paso mas alla con instrucciones especificas por tipo de archivo."

- Crear `.github/instructions/tests.instructions.md`:
```markdown
---
applyTo: "tests/**/*.py"
---
- Usar pytest con fixtures
- Nombres: test_{metodo}_{escenario}_{resultado_esperado}
- Cada test con docstring descriptivo
- Mock de servicios externos con unittest.mock.patch
- Parametrize para casos multiples
```
- Pedir: `Genera tests para la funcion de usuarios que acabamos de crear`
- Mostrar como sigue las convenciones de testing

### Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Instrucciones no aplican | Archivo en ubicacion incorrecta | Debe estar en `.github/copilot-instructions.md` exactamente |
| No se ve diferencia | Cache de Copilot | Recargar ventana de VS Code |
| Instrucciones por ruta no activan | Glob incorrecto | Verificar el campo `applyTo` con la ruta real |

> Transition: "Con instrucciones, Copilot sigue sus convenciones. Pero que tal si necesitan que Copilot acceda a informacion externa? Para eso esta MCP."

---

## Demo 4: GitHub MCP Server

[*] WOW moment: Copilot consulta issues y PRs del repositorio directamente desde el IDE, sin cambiar de ventana.

### Prerequisites

- Repositorio en GitHub con issues y PRs existentes
- VS Code con extension Copilot actualizada
- Token de GitHub configurado

### Steps

**1. Verificar MCP disponible**

> Say this: "MCP es el protocolo que le da a Copilot acceso a herramientas externas. El GitHub MCP Server ya viene integrado con Copilot. Vamos a verificar que esta activo."

- En VS Code, ir a Settings > buscar "MCP"
- Mostrar que el GitHub MCP Server esta habilitado
- O en Copilot Chat: escribir algo que active las tools de GitHub

**2. Consultar Issues**

> Say this: "Ahora le voy a pedir a Copilot que me muestre los issues abiertos de este repositorio. Esto antes requeria cambiar al navegador."

- En Chat (Agent mode): `Lista los issues abiertos de este repositorio y dame un resumen de cada uno`
- Mostrar como Copilot usa las herramientas MCP de GitHub
- Copilot invoca las tools del GitHub MCP Server automaticamente

**3. Analizar un PR**

> Say this: "Vamos a pedirle que analice un pull request existente."

- `Analiza el PR #[numero] de este repositorio. Resume los cambios y sugiere mejoras`
- Mostrar como lee los cambios del PR
- Mostrar las sugerencias

**4. Buscar en el codigo con GitHub Search**

> Say this: "Tambien puede buscar en el codigo del repositorio usando las herramientas de GitHub."

- `Busca en este repositorio todas las funciones que manejan autenticacion`
- Mostrar resultados usando GitHub code search via MCP

### Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| MCP tools no aparecen | Extension desactualizada | Actualizar Copilot extension |
| Permisos denegados | Token sin permisos | Verificar que el token tiene acceso al repo |
| Timeout en consultas | Repositorio muy grande | Ser mas especifico en el query |

> Transition: "Ya vimos como extender a Copilot con MCP. Ahora vamos al nivel final: Cloud Agent, donde Copilot trabaja de forma completamente autonoma."

---

## Demo 5: Cloud Agent desde un Issue

[*] WOW moment: Copilot toma un issue, investiga el codigo, planifica, implementa, ejecuta tests, y crea un PR de forma completamente autonoma.

### Prerequisites

- Repositorio en GitHub con Cloud Agent habilitado
- Repositorio con un proyecto Python funcional (puede ser el de la Demo 2)
- copilot-instructions.md ya configurado (Demo 3)
- Navegador abierto en GitHub.com

### Steps

**1. Crear un Issue**

> Say this: "Vamos a crear un issue real en GitHub y asignarselo a Copilot. Van a ver como trabaja de forma completamente autonoma."

- En GitHub.com, crear un issue en el repositorio:
  - Titulo: "Agregar endpoint de busqueda de productos por categoria"
  - Descripcion:
```
Agregar un nuevo endpoint GET /products/search que permita:
- Buscar productos por categoria (query param)
- Filtrar por rango de precio (min_price, max_price)
- Paginacion con limit y offset
- Incluir tests para el nuevo endpoint
```

**2. Asignar a Copilot**

> Say this: "Para asignar a Copilot, simplemente lo selecciono como assignee. Tambien puedo mencionarlo con @copilot en un comentario."

- En el issue, asignar a "Copilot" como assignee
- O escribir un comentario: `@copilot implementa este feature`
- Copilot empezara a trabajar automaticamente

**3. Observar el proceso**

> Say this: "Copilot esta trabajando ahora mismo en un entorno de GitHub Actions. Vamos a ver los logs en tiempo real."

- Ir a la seccion de Copilot sessions en GitHub
- Mostrar los logs en tiempo real:
  - Investigacion del codebase
  - Plan de implementacion
  - Creacion de archivos
  - Ejecucion de tests
- Comentar cada fase: "Ahi esta leyendo el codigo existente...", "Ahora esta planificando..."

**4. Revisar el Pull Request**

> Say this: "Copilot ya creo el PR. Vamos a revisarlo como revisariamos cualquier PR de un companero."

- Abrir el PR creado por Copilot
- Revisar:
  - Descripcion del PR (generada automaticamente)
  - Cambios en el codigo
  - Tests incluidos
- Si hay algo que mejorar: comentar en el PR y Copilot iterara

**5. (Opcional) Iterar**

> Say this: "Si algo no esta bien, simplemente dejo un comentario y Copilot lo corrige."

- Dejar un comentario pidiendo un cambio menor
- Mostrar como Copilot procesa el feedback y pushea nuevos commits

### Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Copilot no aparece como assignee | Cloud Agent no habilitado | Admin debe habilitar en org settings |
| Session timeout (59 min) | Tarea demasiado compleja | Dividir en issues mas pequenos |
| Tests fallan en CI | Entorno diferente | Verificar que CI y Cloud Agent usan mismo Python |

> Transition: "Y asi llegamos al final de nuestro recorrido Zero to Agent. Veamos los proximos pasos."

---

## Cleanup

Despues de las demos:
- Cerrar los servidores locales (uvicorn)
- Limpiar archivos temporales si es necesario
- Los repositorios de demo se pueden reutilizar

## Resources

- Documentacion de Copilot: https://docs.github.com/copilot
- GitHub MCP Registry: https://github.com/mcp
- Custom Instructions: https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot
- Cloud Agent: https://docs.github.com/en/copilot/using-github-copilot/coding-agent
