"""
Guía de arquitectura y estructura del proyecto.

## Descripción General

Esta aplicación sigue una arquitectura de **tres capas** (MVC) implementada con
FastAPI, aplicando principios de **Clean Code** y **Feature-Driven Development (FDD)**.

## Estructura del Proyecto

```
RepositorioDesarrollo/
├── app/                          # Código fuente principal
│   ├── __init__.py
│   ├── main.py                   # Punto de entrada de FastAPI
│   ├── models/                   # CAPA 1: Modelos de Dominio
│   │   ├── __init__.py
│   │   ├── base_model.py         # Entidad base reutilizable
│   │   └── user.py               # Modelo de Usuario
│   ├── services/                 # CAPA 2: Lógica de Negocio
│   │   ├── __init__.py
│   │   ├── base_service.py       # Servicio base genérico (CRUD)
│   │   └── user_service.py       # Servicio de Usuarios
│   ├── controllers/              # CAPA 3: Controladores/Endpoints
│   │   ├── __init__.py
│   │   └── user_routes.py        # Endpoints de Usuarios
│   ├── schemas/                  # Esquemas Pydantic
│   │   ├── __init__.py
│   │   └── user_schemas.py       # Esquemas de validación (API)
│   └── core/                     # Configuración y Utilidades
│       ├── __init__.py
│       ├── config.py             # Configuración global
│       ├── exceptions.py         # Excepciones personalizadas
│       └── utils.py              # Funciones auxiliares
├── tests/                        # Tests unitarios e integración
│   ├── __init__.py
│   ├── conftest.py              # Configuración de pytest
│   ├── test_models.py           # Tests de modelos
│   ├── test_services.py         # Tests de servicios
│   └── test_api.py              # Tests de endpoints
├── .env.example                  # Ejemplo de configuración
├── .gitignore                    # Archivo de Git
├── .python-version              # Versión de Python
├── pyproject.toml               # Configuración del proyecto
└── README.md                    # Este archivo
```

## Principios de Arquitectura

### 1. **Separación de Responsabilidades**

Cada capa tiene una responsabilidad única:

- **Modelos (Models)**: Representan las entidades del dominio y contienen reglas de negocio básicas.
- **Servicios (Services)**: Implementan la lógica de negocio compleja y orquestación.
- **Controladores (Controllers)**: Manejan las solicitudes HTTP y delegan al servicio.

### 2. **Principios de Clean Code**

- **KISS (Keep It Simple, Stupid)**: Código simple y directo.
- **DRY (Don't Repeat Yourself)**: Reutilización mediante herencia y composición.
- **YAGNI (You Aren't Gonna Need It)**: Solo lo necesario.
- **SOLID**: Principios SOLID en todas las capas.

### 3. **Feature-Driven Development (FDD)**

La aplicación está estructurada por características:

- **Característica**: "Gestión de Usuarios"
- **Archivos relacionados**: `user.py`, `user_service.py`, `user_routes.py`, `user_schemas.py`, `test_*.py`

### 4. **Inyección de Dependencias**

FastAPI proporciona inyección de dependencias automática:

```python
@router.get("")
def list_users(service: UserService = Depends(get_user_service)):
    # El servicio se inyecta automáticamente
    pass
```

## Cómo Desarrollar Nuevas Características

Sigue este patrón para agregar nuevas características:

### 1. Crear el Modelo

```python
# app/models/nueva_entidad.py
from .base_model import BaseEntity

class NuevaEntidad(BaseEntity):
    # Atributos y lógica de negocio específica
    pass
```

### 2. Crear el Servicio

```python
# app/services/nueva_entidad_service.py
from .base_service import BaseService
from app.models import NuevaEntidad

class NuevaEntidadService(BaseService[NuevaEntidad]):
    # Lógica de negocio específica
    pass
```

### 3. Crear los Esquemas

```python
# app/schemas/nueva_entidad_schemas.py
from pydantic import BaseModel

class NuevaEntidadCreateRequest(BaseModel):
    # Campos de creación
    pass
```

### 4. Crear los Endpoints

```python
# app/controllers/nueva_entidad_routes.py
from fastapi import APIRouter, Depends
from app.services import NuevaEntidadService
from app.schemas import NuevaEntidadCreateRequest

router = APIRouter(prefix="/nueva-entidad", tags=["nueva-entidad"])

@router.post("")
def crear(request: NuevaEntidadCreateRequest, service: NuevaEntidadService = Depends()):
    # Implementar endpoint
    pass
```

### 5. Registrar en main.py

```python
# app/main.py
from app.controllers import nueva_entidad_routes

app.include_router(
    nueva_entidad_routes.router,
    prefix=settings.api_prefix,
)
```

### 6. Escribir Tests

```python
# tests/test_nueva_entidad.py
def test_crear_nueva_entidad(client: TestClient) -> None:
    # Tests
    pass
```

## Ejecución

### Instalar dependencias

```bash
pip install -e ".[dev]"
```

### Ejecutar la aplicación

```bash
python -m app.main
# o
uvicorn app.main:app --reload
```

La aplicación estará disponible en `http://localhost:8000`
Documentación automática: `http://localhost:8000/docs`

### Ejecutar tests

```bash
pytest                  # Todos los tests
pytest -v              # Verboso
pytest --cov           # Con cobertura
pytest -k "test_create"  # Tests específicos
```

## Validación de Código

```bash
# Verificar tipos
mypy app/

# Formatear código
black app/ tests/
isort app/ tests/

# Verificar calidad
flake8 app/ tests/
```

## Variables de Entorno

Copiar `.env.example` a `.env` y ajustar según sea necesario:

```bash
cp .env.example .env
```

## Ejemplos de Uso de la API

### Crear un usuario

```bash
curl -X POST "http://localhost:8000/api/v1/users" \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "usuario@example.com",
    "full_name": "Nombre del Usuario",
    "description": "Descripción opcional"
  }'
```

### Listar usuarios

```bash
curl "http://localhost:8000/api/v1/users"
```

### Obtener un usuario

```bash
curl "http://localhost:8000/api/v1/users/{user_id}"
```

### Actualizar un usuario

```bash
curl -X PUT "http://localhost:8000/api/v1/users/{user_id}" \\
  -H "Content-Type: application/json" \\
  -d '{
    "full_name": "Nuevo nombre",
    "description": "Nueva descripción"
  }'
```

### Desactivar un usuario

```bash
curl -X POST "http://localhost:8000/api/v1/users/{user_id}/deactivate"
```

## Estructura de Respuestas

### Respuesta exitosa (201)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "usuario@example.com",
  "full_name": "Nombre del Usuario",
  "is_active": true,
  "description": "Descripción",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### Respuesta de error (400, 404, etc.)

```json
{
  "detail": "Mensaje de error descriptivo",
  "error_code": "VALIDATION_ERROR"
}
```

## Mejoras Futuras

- [ ] Integración con base de datos (SQLAlchemy + PostgreSQL)
- [ ] Autenticación y autorización (JWT)
- [ ] Logging centralizado
- [ ] Caché (Redis)
- [ ] Documentación OpenAPI mejorada
- [ ] Dockerización

## Contribuciones

Al contribuir, mantén:

1. El patrón de arquitectura de tres capas
2. Los principios de Clean Code
3. Los tests para nuevas características
4. La documentación actualizada

## Licencia

Especificar licencia aquí.
