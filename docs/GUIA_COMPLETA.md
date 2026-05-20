# Guía Completa - RepositorioDesarrollo

Aplicación FastAPI con arquitectura de tres capas siguiendo principios de Clean Code y Feature-Driven Development.

## Instalación

### 1. Clonar el repositorio

```powershell
git clone <repository-url>
cd RepositorioDesarrollo
```

### 2. Instalar dependencias

```powershell
uv sync
```

### 3. Activar entorno virtual

Opción A (Manual):

```powershell
.venv\Scripts\Activate.ps1
```

Si tienes error de políticas de ejecución:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Opción B (VS Code - Recomendado):
Abre VS Code desde la carpeta del proyecto. El entorno se activará automáticamente.

### 4. Configurar base de datos

Copiar plantilla de entorno:

```powershell
cp config\.env.example .env
```

Contenido mínimo de `.env`:

```
DEBUG=True
HOST=localhost
PORT=8000
DATABASE_URL=mongodb://localhost:27017
MONGO_DB_NAME=repositorio_db
```

### 5. Iniciar MongoDB (Docker)

```powershell
docker-compose up -d
```

### 6. Ejecutar la aplicación

```powershell
uv run uvicorn app.main:app --reload
```

La API estará disponible en:

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 7. Ejecutar tests

```powershell
uv run pytest tests/ -v
```

Con cobertura:

```powershell
uv run pytest tests/ --cov=app --cov-report=html
```

---

## Arquitectura de Tres Capas

El proyecto está organizado en tres capas independientes:

```
Solicitud HTTP
     ↓
┌──────────────────────────┐
│ CAPA 3: Controladores   │
│ Responsabilidad: HTTP   │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ CAPA 2: Servicios       │
│ Responsabilidad: Lógica │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ CAPA 1: Modelos         │
│ Responsabilidad: Datos  │
└──────────────────────────┘
```

### CAPA 1: Modelos (Entidades de Dominio)

Ubicación: `app/models/`

Responsabilidad: Definir estructura de datos y entidades del negocio.

Ejemplo:

```python
# app/models/pdf_document.py
class DocumentoPDF(BaseEntity):
    nombre_pdf: str
    contenido_pdf: str
    checksum: str
```

Principios: DRY mediante `BaseEntity` que reutiliza id, created_at, updated_at.

### CAPA 2: Servicios (Lógica de Negocio)

Ubicación: `app/services/`

Responsabilidad: Lógica de negocio, validaciones, orquestación.

Ejemplo:

```python
# app/services/pdf_service.py
async def procesar_y_guardar_pdf(file: UploadFile):
    # Validar formato PDF
    # Extraer texto con pypdf
    # Verificar duplicados por checksum
    # Persistir en MongoDB
```

### CAPA 3: Controladores (Endpoints HTTP)

Ubicación: `app/controllers/`

Responsabilidad: Endpoints HTTP, validación de entrada, respuestas JSON.

Ejemplo:

```python
# app/controllers/pdf_routes.py
@router.post("/api/v1/pdfs/")
async def registrar_pdf(file: UploadFile = File(...)):
    documento = await procesar_y_guardar_pdf(file)
    return {"mensaje": "PDF procesado", "datos": documento}
```

---

## Estructura del Proyecto

```
app/
├── main.py                 # Punto de entrada FastAPI
├── controllers/            # Endpoints HTTP
│   ├── pdf_routes.py      # Endpoints para PDFs
│   └── user_routes.py     # Endpoints para usuarios
├── services/              # Lógica de negocio
│   ├── base_service.py    # Servicio genérico
│   └── pdf_service.py     # Procesamiento de PDFs
├── models/                # Entidades de dominio
│   ├── base_model.py      # Clase base
│   └── pdf_document.py    # Modelo de documento PDF
├── schemas/               # Validación Pydantic
│   └── pdf_schemas.py     # Esquemas de PDF
└── core/                  # Configuración central
    ├── config.py          # Settings
    ├── database.py        # Conexión MongoDB
    ├── exceptions.py      # Excepciones personalizadas
    ├── repository.py      # Repositorio en memoria
    ├── mongo_repository.py # Repositorio MongoDB
    └── middleware/
        └── middleware.py  # Limitador de tamaño

config/
├── requirements.txt       # Dependencias
└── .env.example          # Plantilla de entorno

tests/
└── test_pdfs.py          # Tests de PDFs

docs/                      # Documentación

scripts/
└── run.py                # Lanzador de aplicación
```

---

## Endpoints de API

### PDFs

```
POST   /api/v1/pdfs/                 - Subir y procesar PDF
GET    /api/v1/pdfs/                 - Listar todos los PDFs
GET    /api/v1/pdfs/{pdf_id}         - Obtener PDF por ID
DELETE /api/v1/pdfs/{pdf_id}         - Eliminar PDF
```

### Ejemplos de Uso

Subir PDF:

```powershell
curl -X POST "http://localhost:8000/api/v1/pdfs/" `
  -F "file=@documento.pdf"
```

Listar PDFs:

```powershell
curl "http://localhost:8000/api/v1/pdfs/"
```

Obtener PDF específico:

```powershell
curl "http://localhost:8000/api/v1/pdfs/{pdf_id}"
```

Eliminar PDF:

```powershell
curl -X DELETE "http://localhost:8000/api/v1/pdfs/{pdf_id}"
```

---

## Ejecución de Tests

Tests unitarios:

```powershell
uv run pytest tests/test_pdfs.py -v
```

Tests específicos:

```powershell
uv run pytest -k "test_name" -v
```

Con cobertura:

```powershell
uv run pytest tests/ --cov=app --cov-report=html
```

---

## Agregar Nueva Característica

Sigue el patrón de tres capas.

### 1. Crear el Modelo

```python
# app/models/entity.py
class Entity(BaseEntity):
    nombre: str
    descripcion: Optional[str] = None
```

### 2. Crear el Servicio

```python
# app/services/entity_service.py
async def procesar_entity(data):
    # Lógica de negocio
    pass
```

### 3. Crear Esquemas Pydantic

```python
# app/schemas/entity_schemas.py
class EntityCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class EntityResponse(BaseModel):
    id: str
    nombre: str
```

### 4. Crear Endpoints

```python
# app/controllers/entity_routes.py
@router.post("/api/v1/entities/")
async def crear_entity(request: EntityCreate):
    resultado = await procesar_entity(request.dict())
    return EntityResponse(**resultado.dict())
```

### 5. Registrar en main.py

```python
from app.controllers import entity_routes

app.include_router(entity_routes.router)
```

### 6. Escribir Tests

```python
# tests/test_entities.py
def test_crear_entity():
    response = client.post("/api/v1/entities/", json={...})
    assert response.status_code == 201
```

---

## Principios de Desarrollo

Clean Code: KISS, DRY, YAGNI, SOLID

Feature-Driven Development: Desarrollo organizado por características

Test-Driven Development: Tests para modelos, servicios y endpoints

---

## Stack Tecnológico

- FastAPI - Framework web
- Pydantic - Validación de datos
- Motor - Driver async para MongoDB
- Pytest - Framework de pruebas
- PyPDF - Extracción de texto de PDFs
- Python 3.10+

---

## Solución de Problemas

**ModuleNotFoundError:**

```powershell
uv sync
```

**Puerto 8000 ocupado:**

```powershell
uv run uvicorn app.main:app --reload --port 8001
```

**Tests no pasan:**
Asegurar que MongoDB está ejecutándose:

```powershell
docker-compose up -d
uv run pytest tests/ -v
```

**Problemas con imports:**

1. Ejecutar `uv sync`
2. Ctrl+Shift+P → Python: Select Interpreter
3. Seleccionar `.\.venv\Scripts\python.exe`

---

## Recursos Útiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Motor Documentation](https://motor.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [PyPDF Documentation](https://pypdf.readthedocs.io/)

---

**Última actualización:** 20 de mayo de 2026
**Versión de Python:** 3.10+
**Estado:** Desarrollo activo
