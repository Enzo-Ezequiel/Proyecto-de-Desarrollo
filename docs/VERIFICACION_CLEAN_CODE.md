# Verificación de Clean Code

Análisis de calidad del código basado en los principios KISS, DRY, YAGNI y SOLID.

## Resumen de Estado

| Principio | Violaciones encontradas | Estado |
|-----------|------------------------|--------|
| KISS | 3 | Corregidas |
| DRY | 3 | Corregidas |
| YAGNI | 3 | Identificadas, pendientes |
| SOLID | 4 | Corregidas |

---

## KISS (Keep It Simple, Stupid)

### KISS-1: Decorador `log_function_call` sin uso
- **Archivo:** `app/core/utils.py:27-46`
- **Problema:** Decorador definido pero nunca invocado en el proyecto. Solo maneja funciones síncronas, toda la app es async.
- **Estado:** Eliminado (YAGNI + KISS)

### KISS-2: `build_minimal_pdf()` complejidad cognitiva
- **Archivo:** `tests/conftest.py:14-50`
- **Problema:** 37 líneas construyendo PDF raw byte-a-byte. Funcional pero ilegible.
- **Estado:** Se agregó docstring explicativo de la estructura PDF

### KISS-3: Default desalineado en middleware
- **Archivo:** `app/core/middleware/middleware.py:12`
- **Problema:** Default `10MB` no coincide con `Settings.pdf_max_size_mb = 5`.
- **Estado:** Eliminado default hardcodeado, forzado desde Settings

---

## DRY (Don't Repeat Yourself)

### DRY-1: `TypeVar("T")` definido 3 veces
- **Archivos:** `repository.py:13`, `mongo_repository.py:5`, `base_service.py:8`
- **Problema:** Mismo TypeVar duplicado en 3 módulos.
- **Estado:** Consolidado en `repository.py`, importado en los demás.

### DRY-2: Estructura del proyecto documentada 3 veces con discrepancias
- **Archivos:** `README.md`, `docs/GUIA_COMPLETA.md`, `docs/INDEX.md`
- **Problema:** Cada archivo mostraba una estructura diferente.
- **Estado:** Unificada en los 3 archivos.

### DRY-3: Validación de content_type en controller
- **Archivo:** `app/controllers/pdf_routes.py:35-42`
- **Problema:** El controller valida `content_type`, duplicando lógica que debería vivir en el servicio.
- **Estado:** Movido a `PdfService.procesar_y_guardar()`

---

## YAGNI (You Aren't Gonna Need It)

### YAGNI-1: `config/repositoriodesarrollo.toml`
- **Problema:** Archivo de configuración obsoleto, duplica `pyproject.toml` con versiones viejas.
- **Estado:** Identificado. No eliminado por decisión del equipo.

### YAGNI-2: `scripts/run.py`
- **Problema:** Wrapper trivial de uvicorn. `uv run uvicorn` ya funciona directamente.
- **Estado:** Identificado. No eliminado por decisión del equipo.

### YAGNI-3: `InMemoryRepository` en producción
- **Archivo:** `app/core/repository.py:47-80`
- **Problema:** Solo se usa en tests, pero vive en código de producción.
- **Estado:** Identificado. Útil para testing, se mantiene.

---

## SOLID

### SRP-1: Controller con doble responsabilidad
- **Archivo:** `app/controllers/pdf_routes.py:21-24`
- **Problema:** `get_pdf_service` crea `MongoRepository` directamente — el controller rutea HTTP **y** compone dependencias.
- **Estado:** Corregido. Factory de repository movido a `app/core/providers.py`

### DIP-1: Controller depende de implementación concreta
- **Archivo:** `app/controllers/pdf_routes.py:8`
- **Problema:** Importa `MongoRepository` directamente en Capa 3.
- **Estado:** Corregido. Controller solo conoce la abstracción `Repository`

### OCP-1: Mapeo manual de errores
- **Archivo:** `app/main.py:18-23`
- **Problema:** `_ERROR_CODE_TO_STATUS` requiere modificación manual por cada nuevo tipo de error.
- **Estado:** Corregido. Cada `AppException` lleva su `status_code`.

### SRP-2: Database singleton global
- **Archivo:** `app/core/database.py`
- **Problema:** Mezcla patrón singleton, lifecycle de conexión, y acceso a BD.
- **Estado:** Identificado. Pendiente refactor para microservicios (Fase 6).

---

**Última actualización:** 23 de julio de 2026
