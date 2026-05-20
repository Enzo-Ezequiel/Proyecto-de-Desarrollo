# Dependencias del Proyecto

Definición de librerías usadas en RepositorioDesarrollo con justificación arquitectónica.

## Dependencias Principales (Producción)

### FastAPI
Rol: Framework web principal

Razón: Diseñado para type hints nativos, integración directa con Pydantic, documentación automática OpenAPI, soporte async/await.

Uso real: Manejo de endpoints HTTP, CORS middleware, gestión del ciclo de vida de la aplicación.

### Pydantic v2
Rol: Validación de datos

Razón: Validación declarativa, mensajes de error claros, desempeño mejorado, integración automática con FastAPI.

Uso real: Esquemas de request/response, modelos de dominio, configuración tipada.

### pydantic-settings
Rol: Gestión de configuración

Razón: Carga de variables de entorno, validación tipada, un único punto de verdad para settings.

Uso real: Carga de DATABASE_URL, MONGO_DB_NAME, puertos, CORS, secrets desde .env.

### Motor
Rol: Driver asincrónico para MongoDB

Razón: Soporte completo async, integración con FastAPI, manejo eficiente de conexiones a base de datos.

Uso real: Conexión y operaciones con MongoDB en app/core/database.py, MongoRepository para persistencia.

### PyPDF
Rol: Extracción de texto de PDFs

Razón: Lectura de contenido PDF, integración simple, extracto de texto por página.

Uso real: Procesamiento de archivos PDF subidos en pdf_service.py, extracción de texto para almacenamiento.

### Uvicorn
Rol: Servidor ASGI

Razón: Servidor de producción para FastAPI, soporte async, fácil de configurar.

Uso real: Ejecución de la aplicación con `uvicorn app.main:app`.

### python-multipart
Rol: Parseo de file uploads

Razón: Soporte para form data con archivos en FastAPI.

Uso real: Manejo de UploadFile para subida de PDFs.

---

## Dependencias de Desarrollo

### Pytest
Rol: Framework de testing

Razón: Sintaxis simple, fixtures reutilizables, soporte para tests unitarios e integración, plugins abundantes.

Uso real: Tests en tests/test_pdfs.py, cobertura de funcionalidad crítica.

### pytest-cov
Rol: Reporte de cobertura

Razón: Métricas de cobertura de código, reportes HTML.

Uso real: Comando `pytest --cov=app --cov-report=html` para validar calidad de tests.

### httpx
Rol: Cliente HTTP para tests

Razón: Compatible con FastAPI TestClient, soporte async, alternativa moderna a requests.

Uso real: Tests de endpoints HTTP sin necesidad de servidor externo.

### Black
Rol: Formateo de código

Razón: Estilo consistente, sin configuración, opinionado.

Uso real: `black app/ tests/` para mantener formato uniforme.

### Flake8
Rol: Linting

Razón: Detección de errores comunes, estilo PEP 8.

Uso real: `flake8 app/ tests/` para validar calidad de código.

### isort
Rol: Ordenamiento de imports

Razón: Imports organizados según convención, evita conflictos.

Uso real: `isort app/ tests/` para organizar imports automáticamente.

### mypy
Rol: Type checking estático

Razón: Validación de tipos antes de ejecutar, integración con editors.

Uso real: `mypy app/` para verificar consistencia de tipos.

---

## Stack Actual de Producción

- FastAPI 0.136.0
- Pydantic 2.13.3
- pydantic-settings 2.14.0
- Motor 3.7.1+
- PyPDF 6.10.2+
- Uvicorn 0.45.0
- python-multipart 0.0.26

---

## Stack Actual de Desarrollo

- Pytest 9.0.3+
- pytest-cov 7.1.0
- httpx 0.28.1+
- Black 26.3.1
- Flake8 7.3.0
- isort 8.0.1
- mypy 1.20.2

---

## Patrones Arquitectónicos Soportados

Dependencia Inyección: Nativa de FastAPI con `Depends`

Persistencia: Patrón Repository con MongoRepository para MongoDB

Validación: Pydantic para bordes de entrada/salida

Excepciones: Excepciones personalizadas del dominio (AppException, ValidationException, etc.)

Async: Motor + FastAPI para operaciones no-bloqueantes

---

## Decisiones de Diseño

**No incluído: Loguru**
Razón: El proyecto usa logging estándar de Python. Si se requiere logging más avanzado en futuro, puede agregarse sin cambios en el código existente.

**No incluído: Dependency Injector externo**
Razón: FastAPI Depends es suficiente para la complejidad actual. Se evalúa si el proyecto crece.

**No incluído: ORM (SQLAlchemy)**
Razón: MongoDB + Motor proporciona acceso flexible sin ORM. Un ORM documentales no aplica a MongoDB.

---

**Última actualización:** 20 de mayo de 2026
**Compatible con:** Python 3.10+
