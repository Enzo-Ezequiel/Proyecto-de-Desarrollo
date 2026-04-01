# Guía Rápida de Inicio

## Descripción

Esta es una **aplicación FastAPI con arquitectura de tres capas** que sigue los principios de **Clean Code** y **Feature-Driven Development (FDD)**.

### Estructura de Tres Capas

```
CONTROLADORES (Controllers)
    ↓ Delegan
SERVICIOS (Services)
    ↓ Orquestan
MODELOS (Models)
    ↓ Representan
DATOS
```

## Instalación Rápida

### 1. Instalar dependencias

```bash
# Con UV (recomendado según el proyecto)
uv pip install -e ".[dev]"

# O con pip
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

```bash
# Opción 1: Ejecutar el script de acceso rápido
python AccesoRapido.py

# Opción 2: Ejecutar directamente con uvicorn
uvicorn app.main:app --reload

# Opción 3: Ejecutar desde el módulo
python -m app.main
```

### 3. Acceder a la aplicación

- **API**: http://localhost:8000
- **Documentación interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Estructura del Proyecto

```
RepositorioDesarrollo/
├── app/                          # Código fuente
│   ├── models/                   # CAPA 1: Entidades de dominio
│   │   ├── base_model.py         # Clase base reutilizable
│   │   └── user.py               # Ejemplo: modelo Usuario
│   ├── services/                 # CAPA 2: Lógica de negocio
│   │   ├── base_service.py       # Operaciones CRUD genéricas
│   │   └── user_service.py       # Ejemplo: servicio Usuario
│   ├── controllers/              # CAPA 3: Endpoints HTTP
│   │   └── user_routes.py        # Ejemplo: rutas de Usuario
│   ├── schemas/                  # Validación con Pydantic
│   │   └── user_schemas.py       # Esquemas de entrada/salida
│   ├── core/                     # Configuración y utilidades
│   │   ├── config.py             # Variables de entorno
│   │   ├── exceptions.py         # Excepciones personalizadas
│   │   └── utils.py              # Funciones auxiliares
│   └── main.py                   # Punto de entrada (FastAPI)
├── tests/                        # Tests automatizados
│   ├── test_models.py            # Tests unitarios de modelos
│   ├── test_services.py          # Tests unitarios de servicios
│   ├── test_api.py               # Tests de integración API
│   └── conftest.py               # Configuración de pytest
├── ARCHITECTURE.md               # Documentación completa
├── pyproject.toml                # Dependencias del proyecto
├── .env.example                  # Variables de entorno ejemplo
└── AccesoRapido.py              # Script de ejecución rápida
```

## Ejemplos de Uso - API de Usuarios

### Crear usuario

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "full_name": "Juan Pérez",
    "description": "Desarrollador Python"
  }'
```

**Respuesta:**
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

### Listar usuarios

```bash
curl "http://localhost:8000/api/v1/users"
```

### Obtener usuario específico

```bash
curl "http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000"
```

### Actualizar usuario

```bash
curl -X PUT "http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Juan Carlos Pérez",
    "description": "Senior Python Developer"
  }'
```

### Desactivar usuario

```bash
curl -X POST "http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000/deactivate"
```

### Eliminar usuario

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/550e8400-e29b-41d4-a716-446655440000"
```

## Ejecutar Tests

```bash
# Todos los tests
pytest

# Con salida verbosa
pytest -v

# Con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_models.py -v

# Solo tests de integración
pytest tests/test_api.py
```

## Validación de Código

```bash
# Verificar tipos
mypy app/

# Formatear código
black app/ tests/

# Ordenar imports
isort app/ tests/

# Verificar calidad
flake8 app/ tests/
```

## Principios Aplicados

### Clean Code
- ✅ **KISS**: Código simple y directo
- ✅ **DRY**: No repetir (herencia, base services)
- ✅ **YAGNI**: Solo lo necesario
- ✅ **SOLID**: Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion

### Architecture
- ✅ **Separación de responsabilidades**: 3 capas claras
- ✅ **Inyección de dependencias**: Con FastAPI
- ✅ **Genéricos**: BaseService<T> reutilizable
- ✅ **Documentación**: Docstrings detallados

### Testing
- ✅ **Unitarios**: Modelos y servicios
- ✅ **Integración**: Endpoints HTTP completos
- ✅ **Fixtures**: Reutilizables con pytest

## Agregar Nueva Característica

Para agregar una nueva entidad (e.g., "Producto"):

1. **Crear modelo** (`app/models/product.py`)
   ```python
   class Product(BaseEntity):
       name: str
       price: float
       description: Optional[str] = None
   ```

2. **Crear servicio** (`app/services/product_service.py`)
   ```python
   class ProductService(BaseService[Product]):
       # Lógica específica de productos
       pass
   ```

3. **Crear esquemas** (`app/schemas/product_schemas.py`)
   ```python
   class ProductCreateRequest(BaseModel):
       name: str
       price: float
   ```

4. **Crear controlador** (`app/controllers/product_routes.py`)
   ```python
   router = APIRouter(prefix="/products")
   
   @router.post("")
   def create(request: ProductCreateRequest, service = Depends()):
       return service.create_product(...)
   ```

5. **Registrar en main.py**
   ```python
   app.include_router(product_routes.router, prefix=settings.api_prefix)
   ```

6. **Escribir tests** (`tests/test_product.py`)

## Variables de Entorno

Copiar `.env.example` a `.env`:

```bash
cp .env.example .env
```

Contenido ejemplo:
```
DEBUG=True
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=["http://localhost", "http://localhost:3000"]
```

## Recursos Útiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Clean Code - Robert C. Martin](https://www.oreilly.com/library/view/clean-code/9780136083238/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

## Troubleshooting

### "ModuleNotFoundError: No module named 'app'"

Asegúrate de ejecutar desde el directorio raíz del proyecto y que las dependencias estén instaladas.

### "Address already in use"

El puerto 8000 está ocupado. Usar otro puerto:

```bash
uvicorn app.main:app --reload --port 8001
```

### Tests fallan

Asegúrate de que las dependencias están instaladas:

```bash
pip install -e ".[dev]"
```

## ¿Preguntas o Sugerencias?

Para más detalles, revisar `ARCHITECTURE.md`.

---

**¡Felicidades! Ya tienes una aplicación FastAPI profesional con arquitectura limpia.** 🚀
