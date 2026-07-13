# Demo 3 Companion - Test Instructions Template
# Usage: Copiar a .github/instructions/python-tests.instructions.md
# Prerequisites: Directorio .github/instructions/ creado

---
applyTo: "tests/**/*.py"
---

- Usar pytest como framework de testing
- Fixtures para setup y teardown de datos de prueba
- Cada funcion de test debe tener docstring descriptivo
- Nombres de tests: test_{metodo}_{escenario}_{resultado_esperado}
- Mock de dependencias externas con unittest.mock.patch
- Usar pytest.raises para validar excepciones
- Parametrize para cubrir multiples casos con un solo test
- Assertions descriptivas con mensajes claros
- No usar sleep() en tests, usar mocks para tiempo
- Separar unit tests de integration tests en directorios
