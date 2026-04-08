# 📚 Guía Completa - RepositorioDesarrollo

Una aplicación profesional con **arquitectura de tres capas** usando FastAPI, siguiendo principios de **Clean Code** y **Feature-Driven Development**.

---

### Paso 1: Instalar Dependencias

```bash
# Opción A: Con pip (recomendado)
pip install -r config/requirements.txt

# Opción B: Con pip en modo editable para desarrollo
pip install -e ".[dev]"

# Opción C: Con UV (si lo tienes instalado)
uv pip install -e ".[dev]"
```

### Paso 2: Ejecutar la Aplicación

```bash
# Opción A: Script de acceso rápido
python scripts/run.py

# Opción B: Directo con uvicorn
uvicorn app.main:app --reload

# Opción C: Como módulo
python -m app.main
```

### Paso 3: Abrir en el Navegador

Elige una de estas opciones:

- **Swagger UI (Recomendado)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API**: http://localhost:8000

### Paso 4: Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=app --cov-report=html
```

---

## 🏗️ Entendiendo la Arquitectura de Tres Capas

Este proyecto implementa una **arquitectura de tres capas** que separa la aplicación en tres niveles independientes de responsabilidad. Cada capa tiene una función específica y se comunica de forma jerárquica.

### ¿Por qué Tres Capas?

La arquitectura de tres capas permite:
- ✅ **Separación de responsabilidades**: Cada capa tiene un propósito claro
- ✅ **Reutilización**: Componentes base se usan en múltiples características
- ✅ **Testabilidad**: Cada capa se puede probar de forma independiente
- ✅ **Mantenibilidad**: Cambios en la lógica no afectan endpoints
- ✅ **Escalabilidad**: Fácil agregar nuevas características

### Flujo de Solicitudes

Las solicitudes HTTP siguen este flujo:

```
Cliente (navegador, curl, postman, etc.)
    ↓ Solicitud HTTP (POST /api/users)
┌─────────────────────────────────────────────────┐
│  CAPA 3: Controladores (Controllers/Routes)     │
│  Responsabilidad: Recibir HTTP y delegar        │
│  Archivos: app/controllers/user_routes.py       │
│  Ejemplo: @router.post("/users")                │
└─────────────────────┬───────────────────────────┘
                      ↓ Delega al servicio
┌─────────────────────────────────────────────────┐
│  CAPA 2: Servicios (Business Logic)             │
│  Responsabilidad: Implementar reglas de negocio │
│  Archivos: app/services/user_service.py         │
│  Ejemplo: def create_user(user_data) -> User    │
└─────────────────────┬───────────────────────────┘
                      ↓ Accede a/modifica datos
┌─────────────────────────────────────────────────┐
│  CAPA 1: Modelos (Domain Entities)              │
│  Responsabilidad: Representar datos             │
│  Archivos: app/models/user.py                   │
│  Ejemplo: class User(BaseEntity): ...           │
└─────────────────────────────────────────────────┘
                      ↓ Procesa
                    Datos
    ↑ Respuesta JSON (201 Created)
    Cliente
```

### Desglose de Cada Capa

#### **CAPA 1: Modelos (Entidades de Dominio)**

**Ubicación**: `app/models/`

**Responsabilidad**: Definir y representar la estructura de datos

**Qué hace**:
- Representa entidades del negocio (Usuario, Producto, etc.)
- Contiene validaciones básicas de dominio
- Define atributos y su tipo

**Ejemplo**:
```python
# app/models/user.py
class User(BaseEntity):
    email: str
    full_name: str
    is_active: bool = True
    description: Optional[str] = None
```

**Principios**:
- **DRY**: Hereda de `BaseEntity` para reutilizar id, created_at, updated_at
- **KISS**: Solo representa datos, sin lógica compleja
- **Encapsulación**: Métodos para cambiar estado de forma segura

---

#### **CAPA 2: Servicios (Lógica de Negocio)**

**Ubicación**: `app/services/`

**Responsabilidad**: Ejecutar la lógica de negocio compleja

**Qué hace**:
- Procesa datos del controlador
- Valida reglas de negocio
- Orquesta operaciones complejas
- Maneja errores y excepciones

**Ejemplo**:
```python
# app/services/user_service.py
class UserService(BaseService[User]):
    def create_user(self, email: str, full_name: str) -> User:
        # Validar que el email no exista
        # Crear el usuario
        # Retornar el usuario creado
        pass
    
    def activate_user(self, user_id: UUID) -> User:
        # Verificar que el usuario existe
        # Cambiar is_active a True
        # Guardar y retornar
        pass
```

**Principios**:
- **Single Responsibility**: Una clase de servicio por entidad
- **Generic Types**: Reutilización de CRUD mediante `BaseService<T>`
- **Fail-fast**: Validar y fallar temprano, antes de hacer cambios

---

#### **CAPA 3: Controladores (Endpoints HTTP)**

**Ubicación**: `app/controllers/`

**Responsabilidad**: Manejar solicitudes HTTP y respuestas

**Qué hace**:
- Recibe solicitudes HTTP (GET, POST, PUT, DELETE)
- Valida entrada con esquemas Pydantic
- Delega al servicio
- Retorna respuesta JSON

**Ejemplo**:
```python
# app/controllers/user_routes.py
@router.post("")
def create_user(
    request: UserCreateRequest,
    service: UserService = Depends()
) -> UserResponse:
    # El servicio se inyecta automáticamente
    user = service.create_user(
        email=request.email,
        full_name=request.full_name
    )
    return UserResponse(**user.dict())
```

**Principios**:
- **Separation of Concerns**: Solo HTTP, sin lógica de negocio
- **Dependency Injection**: FastAPI inyecta dependencias automáticamente
- **Validación**: Esquemas Pydantic validan automáticamente

---

## 📁 Estructura del Proyecto

```
RepositorioDesarrollo/
│
├── app/                              # Código fuente principal
│   ├── __init__.py
│   ├── main.py                       # Punto de entrada de FastAPI
│   │
│   ├── models/                       # CAPA 1: Entidades de Dominio
│   │   ├── __init__.py
│   │   ├── base_model.py            # Clase base genérica
│   │   └── user.py                  # Modelo de usuario
│   │
│   ├── services/                     # CAPA 2: Lógica de Negocio
│   │   ├── __init__.py
│   │   ├── base_service.py          # Servicio genérico CRUD
│   │   └── user_service.py          # Servicio de usuarios
│   │
│   ├── controllers/                  # CAPA 3: Endpoints HTTP
│   │   ├── __init__.py
│   │   └── user_routes.py           # Rutas de API de usuarios
│   │
│   ├── schemas/                      # Esquemas de Validación Pydantic
│   │   ├── __init__.py
│   │   └── user_schemas.py          # Esquemas de usuario
│   │
│   └── core/                         # Configuración Central
│       ├── __init__.py
│       ├── config.py                # Configuración global
│       ├── exceptions.py            # Excepciones personalizadas
│       └── utils.py                 # Funciones auxiliares
│
├── tests/                            # Suite de Tests Completa
│   ├── __init__.py
│   ├── conftest.py                  # Configuración de Pytest
│   ├── test_models.py               # Tests unitarios de modelos (7 tests)
│   ├── test_services.py             # Tests unitarios de servicios (8 tests)
│   └── test_api.py                  # Tests de integración (12 tests)
│
├── docs/                             # Documentación
│   └── GUIA_COMPLETA.md             # Esta guía
│
├── scripts/                          # Scripts de Utilidad
│   └── run.py                       # Lanzador de la aplicación
│
├── config/                           # Archivos de Configuración
│   ├── .env.example                 # Plantilla de variables de entorno
│   └── requirements.txt             # Dependencias de Python
│
├── .vscode/                          # Configuración de VS Code
│   ├── settings.json                # Configuración de editor
│   ├── extensions.json              # Extensiones recomendadas
│   └── launch.json                  # Configuraciones de debug
│
├── pyproject.toml                    # Configuración del proyecto Python
├── .python-version                   # Especificación de versión de Python
├── .gitignore                        # Reglas de ignorado de Git
└── README.md                         # Información general del proyecto
```

---

## 🧪 Endpoints de API

### Endpoints de Usuario

```
GET    /api/users                    - Obtener todos los usuarios
POST   /api/users                    - Crear nuevo usuario
GET    /api/users/{user_id}          - Obtener usuario por ID
PUT    /api/users/{user_id}          - Actualizar usuario
DELETE /api/users/{user_id}          - Eliminar usuario
POST   /api/users/{user_id}/activate    - Activar usuario
POST   /api/users/{user_id}/deactivate  - Desactivar usuario
```

### Ejemplos de Uso

#### Crear Usuario

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "full_name": "Juan Pérez",
    "description": "Desarrollador Python"
  }'
```

**Respuesta** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "juan@example.com",
  "full_name": "Juan Pérez",
  "is_active": true,
  "description": "Desarrollador Python",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### Obtener Todos los Usuarios

```bash
curl "http://localhost:8000/api/users"
```

#### Obtener Usuario por ID

```bash
curl "http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000"
```

#### Actualizar Usuario

```bash
curl -X PUT "http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Juan Carlos Pérez",
    "description": "Senior Python Developer"
  }'
```

#### Desactivar Usuario

```bash
curl -X POST "http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000/deactivate"
```

#### Eliminar Usuario

```bash
curl -X DELETE "http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000"
```

---

## 💻 Ejecutar Tests

### Todos los Tests

```bash
pytest tests/ -v
```

### Tests Específicos

```bash
# Solo tests de modelos
pytest tests/test_models.py -v

# Solo tests de servicios
pytest tests/test_services.py -v

# Solo tests de API
pytest tests/test_api.py -v

# Tests que contengan "create"
pytest -k "create" -v
```

### Con Cobertura

```bash
pytest tests/ --cov=app --cov-report=html
# Abre htmlcov/index.html en el navegador
```

---

## 🆕 Agregar Nueva Característica

Sigue este patrón para agregar una nueva entidad (ejemplo: "Producto").

### 1. Crear el Modelo

```python
# app/models/product.py
from .base_model import BaseEntity

class Product(BaseEntity):
    """Modelo de Producto"""
    name: str
    price: float
    description: Optional[str] = None
    is_available: bool = True
```

### 2. Crear el Servicio

```python
# app/services/product_service.py
from .base_service import BaseService
from app.models import Product

class ProductService(BaseService[Product]):
    """Servicio de lógica de negocio para Productos"""
    
    def get_available_products(self) -> List[Product]:
        """Obtener productos disponibles"""
        # Implementar lógica específica
        pass
    
    def apply_discount(self, product_id: UUID, discount: float) -> Product:
        """Aplicar descuento a un producto"""
        # Implementar lógica específica
        pass
```

### 3. Crear los Esquemas

```python
# app/schemas/product_schemas.py
from pydantic import BaseModel

class ProductCreateRequest(BaseModel):
    """Esquema para crear producto"""
    name: str
    price: float
    description: Optional[str] = None

class ProductResponse(BaseModel):
    """Esquema de respuesta de producto"""
    id: UUID
    name: str
    price: float
    is_available: bool
    created_at: datetime
```

### 4. Crear los Endpoints

```python
# app/controllers/product_routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.services import ProductService
from app.schemas import ProductCreateRequest, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", status_code=201)
def create_product(
    request: ProductCreateRequest,
    service: ProductService = Depends()
) -> ProductResponse:
    """Crear nuevo producto"""
    product = service.create(request.dict())
    return ProductResponse(**product.dict())

@router.get("")
def list_products(
    service: ProductService = Depends()
) -> List[ProductResponse]:
    """Obtener todos los productos"""
    products = service.get_all()
    return [ProductResponse(**p.dict()) for p in products]

@router.get("/{product_id}")
def get_product(
    product_id: UUID,
    service: ProductService = Depends()
) -> ProductResponse:
    """Obtener producto por ID"""
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return ProductResponse(**product.dict())

@router.put("/{product_id}")
def update_product(
    product_id: UUID,
    request: ProductCreateRequest,
    service: ProductService = Depends()
) -> ProductResponse:
    """Actualizar producto"""
    product = service.update(product_id, request.dict())
    return ProductResponse(**product.dict())

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: UUID,
    service: ProductService = Depends()
):
    """Eliminar producto"""
    service.delete(product_id)
```

### 5. Registrar en main.py

```python
# app/main.py
from app.controllers import product_routes

app.include_router(
    product_routes.router,
    prefix=settings.api_prefix
)
```

### 6. Escribir Tests

```python
# tests/test_product.py
from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_create_product():
    """Test: crear un nuevo producto"""
    response = client.post(
        "/api/products",
        json={
            "name": "Laptop",
            "price": 999.99,
            "description": "Laptop profesional"
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Laptop"

def test_get_all_products():
    """Test: obtener todos los productos"""
    response = client.get("/api/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

---

## ✅ Principios de Desarrollo

### Clean Code

- **KISS (Keep It Simple, Stupid)**: Código simple y directo, sin complejidades innecesarias
- **DRY (Don't Repeat Yourself)**: Reutilización mediante herencia (`BaseEntity`, `BaseService`)
- **YAGNI (You Aren't Gonna Need It)**: Solo lo necesario, sin sobreingeniería
- **SOLID**:
  - **S**ingle Responsibility: Una responsabilidad por clase
  - **O**pen/Closed: Abierto para extensión, cerrado para modificación
  - **L**iskov Substitution: Subclases intercambiables
  - **I**nterface Segregation: Interfaces específicas
  - **D**ependency Inversion: Depender de abstracciones, no de implementaciones

### Feature-Driven Development (FDD)

La aplicación está estructurada por características:

- **Característica**: "Gestión de Usuarios"
- **Archivos relacionados**: 
  - `app/models/user.py`
  - `app/services/user_service.py`
  - `app/controllers/user_routes.py`
  - `app/schemas/user_schemas.py`
  - `tests/test_user.py` (o test_models.py, test_services.py, test_api.py)

### Testing (TDD)

- **Unitarios**: Pruebas de modelos y servicios de forma aislada
- **Integración**: Pruebas de endpoints HTTP completos
- **Fixtures**: Reutilizables con Pytest para mantener DRY

---

## 🛠️ Validación de Código

### Verificar Tipos

```bash
mypy app/
```

### Formatear Código

```bash
black app/ tests/
```

### Ordenar Imports

```bash
isort app/ tests/
```

### Verificar Calidad

```bash
flake8 app/ tests/
```

---

## 🔧 Variables de Entorno

Copiar `.env.example` a `.env`:

```bash
cp config/.env.example .env
```

Ejemplo de contenido:

```
DEBUG=True
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=["http://localhost", "http://localhost:3000"]
```

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'app'"

**Solución**: Ejecuta desde el directorio raíz del proyecto y asegúrate de que las dependencias están instaladas.

```bash
cd C:\Programas\RepositorioDesarrollo
pip install -r config/requirements.txt
python scripts/run.py
```

### "Address already in use"

**Solución**: El puerto 8000 está ocupado. Usa otro puerto:

```bash
uvicorn app.main:app --reload --port 8001
```

### Los tests no pasan

**Solución**: Instala las dependencias de desarrollo:

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

### Problemas con imports en VS Code

**Solución**: Abre el workspace correcto:

```bash
code RepositorioDesarrollo.code-workspace
```

---

## 🚀 Tecnologías y Herramientas

- **Framework**: FastAPI
- **Validación**: Pydantic
- **Testing**: pytest
- **Calidad de Código**: Ruff, Black, mypy
- **Versión de Python**: 3.10+
- **Editor**: Visual Studio Code con extensión de Python

---

## 📚 Recursos Útiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Clean Code - Robert C. Martin](https://www.oreilly.com/library/view/clean-code/9780136083238/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Python 3.10+ Features](https://docs.python.org/3/)

---

## 🤝 Contribuyendo

Al agregar nuevas características, mantén:

1. ✅ El patrón de arquitectura de tres capas
2. ✅ Los principios de Clean Code
3. ✅ Tests unitarios e integración para nuevas características
4. ✅ La documentación actualizada
5. ✅ Docstrings en todas las funciones

---

## 📄 Licencia

Este es un proyecto de desarrollo. Consulta el archivo `LICENSE` para más detalles.

---

## 📞 Soporte

Para más información:

1. Lee los docstrings del código (están documentados)
2. Revisa los tests como ejemplos de uso
3. Consulta la sección "Troubleshooting" arriba
4. Revisa los comentarios en el código fuente

---

**Última Actualización**: 8 de abril de 2026  
**Versión de Python**: 3.10+  
**Estado**: Desarrollo Activo

✨ **¡Felicidades! Ya tienes una aplicación FastAPI profesional con arquitectura limpia.** 🚀
