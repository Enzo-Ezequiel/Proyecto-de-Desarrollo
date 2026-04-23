# RepositorioDesarrollo

Una aplicación profesional con arquitectura de tres capas usando FastAPI, siguiendo principios de Clean Code y Feature-Driven Development.

## 📁 Estructura del Proyecto

```
RepositorioDesarrollo/
├── app/                          # Código fuente principal
│   ├── __init__.py
│   ├── main.py                   # Punto de entrada de FastAPI
│   ├── models/                   # Entidades de dominio
│   │   ├── __init__.py
│   │   ├── base_model.py         # Clase base genérica
│   ├── services/                 # Capa de lógica de negocio
│   │   ├── __init__.py
│   │   ├── base_service.py       # Servicio genérico CRUD
│   ├── controllers/              # Capa de endpoints HTTP
│   │   ├── __init__.py
│   ├── schemas/                  # Esquemas de validación Pydantic
│   │   ├── __init__.py
│   └── core/                     # Configuración central
│       ├── __init__.py
│       ├── config.py             # Configuración de la aplicación
│       ├── exceptions.py         # Excepciones personalizadas
│       └── utils.py              # Funciones auxiliares
├── tests/                        # Suite de tests completa
│   ├── __init__.py
│   ├── conftest.py               # Configuración de Pytest
│   ├── test_models.py            # Tests unitarios de modelos (7 tests)
│   ├── test_services.py          # Tests unitarios de servicios (8 tests)
│   └── test_api.py               # Tests de integración (12 tests)
├── docs/                         # Documentación
│   └── GUIA_COMPLETA.md         # Guía completa (inicio, arquitectura, desarrollo)
├── scripts/                      # Scripts de utilidad
│   └── run.py                    # Lanzador de aplicación FastAPI
├── config/                       # Archivos de configuración
│   ├── .env.example              # Plantilla de variables de entorno
│   └── requirements.txt          # Dependencias de Python
├── .vscode/                      # Configuración de VS Code
│   ├── settings.json             # Configuración de editor y Python
│   ├── extensions.json           # Extensiones recomendadas
│   └── launch.json               # Configuraciones de debug
├── pyproject.toml                # Configuración del proyecto Python
├── repositoriodesarrollo.toml    # Configuración adicional del proyecto
├── RepositorioDesarrollo.code-workspace  # Workspace de VS Code
├── .python-version               # Especificación de versión de Python
├── .gitignore                    # Reglas de ignorado de Git
└── README.md                     # Este archivo
```

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```bash
# Clonar el repositorio (si no lo ha hecho aún)
git clone <repository-url>
cd RepositorioDesarrollo
```

### 2. Instalar dependencias

```bash
# Copiar en terminal
uv sync

# Crea el entorno virtual .venv
#instala las dependencias especificadas en uv.lock
```

### 3. Ejecutar la Aplicación

```bash
# Usando uvicorn 
uv run uvicorn app.main:app --reload
```

### 4. Acceder a la API

API: http://127.0.0.1:8000
Documentación Swagger: http://127.0.0.1:8000/docs

### 5. Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar con cobertura
pytest tests/ --cov=app --cov-report=html
```

## 📚 Documentación

Para información completa sobre cómo usar y desarrollar en este proyecto, consulta:

- **[📖 Guía Completa](docs/GUIA_COMPLETA.md)** - Todo lo que necesitas saber:
  - Inicio rápido (5 minutos)
  - Explicación detallada de la arquitectura de tres capas
  - Ejemplos de endpoints de API
  - Cómo agregar nuevas características
  - Ejecución de tests
  - Troubleshooting
  - Recursos útiles

## 🏗️ Arquitectura de Tres Capas

Este proyecto implementa una **arquitectura de tres capas**, que separa la aplicación en tres niveles independientes de responsabilidad. Esto permite que el código sea más modular, testeable y mantenible.

### ¿Qué significa "Arquitectura de Tres Capas"?

La arquitectura de tres capas divide la aplicación en tres componentes horizontales que se comunican entre sí de forma jerárquica:

1. **CAPA 1: Modelos (Models)** - La base que representa los datos
2. **CAPA 2: Servicios (Services)** - La lógica que procesa esos datos
3. **CAPA 3: Controladores (Controllers)** - Los puntos de acceso HTTP

El flujo de información es **unidireccional**: Las solicitudes HTTP bajan por las capas, y las respuestas suben:

```
Solicitudes HTTP
     ↓
┌─────────────────────────────────────────────────────────┐
│  CAPA 3: Controladores (Controllers/Routes)             │
│  Responsabilidad: Recibir solicitudes HTTP y responder  │
│  Archivos: user_routes.py                              │
│  Ejemplo: @router.post("/users")                        │
└──────────────────────┬──────────────────────────────────┘
                       ↓ Delega al servicio
┌─────────────────────────────────────────────────────────┐
│  CAPA 2: Servicios (Business Logic)                     │
│  Responsabilidad: Implementar reglas de negocio         │
│  Archivos: user_service.py                              │
│  Ejemplo: def create_user(user_data) -> User            │
└──────────────────────┬──────────────────────────────────┘
                       ↓ Accede a los datos
┌─────────────────────────────────────────────────────────┐
│  CAPA 1: Modelos (Domain Entities)                      │
│  Responsabilidad: Representar y estructurar los datos   │
│  Archivos: user.py                                      │
│  Ejemplo: class User(BaseEntity): ...                   │
└─────────────────────────────────────────────────────────┘
     ↑
     Devuelve respuesta
```

### Desglose de Cada Capa

**CAPA 1: Modelos (Entidades de Dominio)**
- **Ubicación**: `app/models/`
- **Responsabilidad**: Definir la estructura de datos
- **Qué hace**: Representa entidades del negocio (Usuario, Producto, etc.)
- **Ejemplo**: `User` con atributos como `id`, `name`, `email`, `is_active`
- **Principio**: DRY mediante `BaseEntity` que reutiliza id, timestamps

**CAPA 2: Servicios (Lógica de Negocio)**
- **Ubicación**: `app/services/`
- **Responsabilidad**: Ejecutar la lógica de negocio compleja
- **Qué hace**: Procesa datos, valida reglas, orquesta operaciones
- **Ejemplo**: `UserService` que crea, actualiza, activa usuarios
- **Principio**: Una clase de servicio por entidad para Single Responsibility

**CAPA 3: Controladores (Endpoints HTTP)**
- **Ubicación**: `app/controllers/`
- **Responsabilidad**: Manejar solicitudes HTTP y respuestas
- **Qué hace**: Recibe JSON, delega al servicio, devuelve resultado
- **Ejemplo**: `@router.post("/users")` que crea un usuario
- **Principio**: Solo HTTP, sin lógica de negocio

### Ventajas de Esta Estructura

✅ **Separación de responsabilidades**: Cada capa tiene un propósito claro
✅ **Reutilización**: `BaseEntity` y `BaseService` se usan en múltiples características
✅ **Testabilidad**: Cada capa se puede probar de forma independiente
✅ **Mantenibilidad**: Cambios en la lógica no afectan endpoints
✅ **Escalabilidad**: Fácil agregar nuevas características siguiendo el patrón

```
HTTP Requests
    ↓
┌─────────────────────────────┐
│  Controllers (Routes)       │  ← Endpoints HTTP, validación
│  user_routes.py             │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Services (Business Logic)  │  ← Lógica central, procesamiento
│  user_service.py            │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Models (Domain Entities)   │  ← Representación de datos
│  user.py                    │
└─────────────────────────────┘
```

### Características Clave

- **Clases Base Genéricas**: `BaseEntity` y `BaseService<T>` para reutilización
- **Validación Pydantic**: Esquemas type-safe para solicitudes/respuestas
- **Clean Code**: KISS, DRY, YAGNI, principios SOLID
- **Tests Completos**: 27 tests cubriendo modelos, servicios y endpoints
- **Estructura Profesional**: Directorios organizados siguiendo mejores prácticas

## 🧪 Endpoints de API

### Endpoints de Usuario

```
GET    /api/users              - Obtener todos los usuarios
POST   /api/users              - Crear nuevo usuario
GET    /api/users/{user_id}    - Obtener usuario por ID
PUT    /api/users/{user_id}    - Actualizar usuario
DELETE /api/users/{user_id}    - Eliminar usuario
POST   /api/users/{user_id}/activate    - Activar usuario
POST   /api/users/{user_id}/deactivate  - Desactivar usuario
```

## 🛠️ Tecnologías y Herramientas

- **Framework**: FastAPI
- **Validación**: Pydantic
- **Testing**: pytest
- **Calidad de Código**: Ruff, Black
- **Versión de Python**: 3.10+
- **Editor**: Visual Studio Code con extensión de Python

## 📋 Principios de Desarrollo

- **Clean Code**: KISS, DRY, YAGNI, SOLID
- **TDD**: Test-Driven Development
- **FDD**: Feature-Driven Development
- **Arquitectura**: Patrón de tres capas MVC

## 🔧 Integración con VS Code

Este proyecto incluye configuración de VS Code para:

- Formateo Python con Ruff
- Integración de Pytest
- Configuraciones de lanzamiento para debug
- Extensiones recomendadas

Abra `.vscode/settings.json` para ver la configuración del editor.

## 📝 Objetivos Originales del Proyecto

- Extraer texto de archivos PDF
- Resumir usando modelos de IA (Gemini)
- Arquitectura profesional de tres capas
- Principios de Clean Code
- Documentación completa

## 🤝 Contribuyendo

Al agregar nuevas características:

1. Crear una nueva rama
2. Seguir la arquitectura de tres capas
3. Agregar tests unitarios e integración
4. Actualizar documentación
5. Crear un pull request

## 📄 Licencia

Este es un proyecto de desarrollo. Consulte el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para más información, consulte la documentación en el directorio `docs/` o revise los comentarios en el código.

---

**Última Actualización**: 1 de abril de 2026
**Versión de Python**: 3.10+
**Estado**: Desarrollo Activo
