# RepositorioDesarrollo

Una aplicación profesional con arquitectura de tres capas usando FastAPI, siguiendo principios de Clean Code y Feature-Driven Development.

## ✅ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10+**
- **[uv](https://docs.astral.sh/uv/)** - Gestor de paquetes y entornos virtuales
- **Git**
- **Visual Studio Code** (recomendado)
- **Sistema operativo: Windows** (PowerShell)
- **Docker Desktop** - Para ejecutar la base de datos MongoDB localmente

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```powershell
# Clonar el repositorio
git clone <repository-url>
cd RepositorioDesarrollo
```

### 2. Instalar dependencias

```powershell
# Sincronizar dependencias (esto crea automáticamente el entorno virtual .venv)
uv sync
```

**Importante:** Una vez ejecutado `uv sync`, debes **activar el entorno virtual** antes de continuar:

#### Opción A: Activación Manual

Abre PowerShell en la raíz del proyecto y ejecuta:

```powershell
.venv\Scripts\Activate.ps1
```

> 💡 **Nota:** Si ves un error sobre políticas de ejecución, ejecuta primero:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

Verás `(Proyecto-de-Desarrollo)` al inicio de tu línea de comandos cuando esté activo.

#### Opción B: VS Code (Automático) ⭐⭐ **Recomendado**

El proyecto está configurado para activar el entorno automáticamente:

1. Abre VS Code desde la carpeta del proyecto (`code .`)
2. Abre una terminal integrada (`Ctrl + `` `)
3. El entorno se activará solo (verás `(Proyecto-de-Desarrollo)` en el prompt)

### 3. Verificar que el entorno funciona

Ejecuta en tu terminal:

```powershell
python -c "import fastapi; import uvicorn; print('✅ Entorno configurado correctamente')"
```

Si ves el mensaje ✅ sin errores, el entorno está listo.

### 4. Crear la carpeta .env

Buscar en config el archivo env.example copia el contenido, luego en la carpeta raiz crea el archivo .env y pega el contenido

### 5. Levantar la Base de Datos (Docker)

Antes de iniciar la aplicación, asegúrate de que Docker Desktop esté abierto y ejecuta este comando para iniciar MongoDB:

```powershell
docker-compose up -d
```

### 6. Ejecutar la Aplicación

```powershell
# Usando uv (recomendado - no requiere activar el entorno manualmente)
uv run uvicorn app.main:app --reload

# O si prefieres activar el entorno primero:
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

### 7. Acceder a la API

- **API**: http://127.0.0.1:8000
- **Documentación Swagger**: http://127.0.0.1:8000/docs
- **Documentación ReDoc**: http://127.0.0.1:8000/redoc

### 8. Ejecutar Tests

```powershell
# Ejecutar todos los tests
uv run pytest tests/ -v

# O con el entorno activado:
pytest tests/ -v

# Ejecutar con cobertura
pytest tests/ --cov=app --cov-report=html
```

---

## 📁 Estructura del Proyecto

```
RepositorioDesarrollo/
├── app/                      # Código fuente principal
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de FastAPI
│   ├── models/              # Entidades de dominio
│   │   ├── __init__.py
│   │   └── base_model.py    # Clase base genérica (BaseEntity)
│   ├── services/            # Capa de lógica de negocio
│   │   ├── __init__.py
│   │   └── base_service.py  # Servicio genérico CRUD (BaseService<T>)
│   ├── controllers/         # Capa de endpoints HTTP
│   │   └── __init__.py
│   ├── schemas/             # Esquemas de validación Pydantic
│   │   └── __init__.py
│   └── core/                # Configuración central
│       ├── __init__.py
│       ├── config.py        # Configuración de la aplicación
│       ├── exceptions.py    # Excepciones personalizadas
│       ├── repository.py    # Repositorio en memoria
│       └── utils.py         # Funciones auxiliares
├── tests/                   # Suite de tests
│   ├── __init__.py
│   ├── conftest.py         # Configuración de Pytest
│   ├── test_models.py      # Tests unitarios de modelos
│   ├── test_services.py    # Tests unitarios de servicios
│   └── test_api.py         # Tests de integración
├── docs/                    # Documentación
│   └── GUIA_COMPLETA.md    # Guía completa
├── scripts/                 # Scripts de utilidad
│   └── run.py              # Lanzador de aplicación FastAPI
├── config/                  # Archivos de configuración
│   ├── .env.example        # Plantilla de variables de entorno
│   └── requirements.txt    # Dependencias de Python
├── .vscode/                 # Configuración de VS Code
│   ├── settings.json       # Configuración de editor y Python
│   ├── extensions.json     # Extensiones recomendadas
│   └── launch.json         # Configuraciones de debug
├── pyproject.toml          # Configuración del proyecto Python
├── repositoriodesarrollo.toml  # Configuración adicional del proyecto
├── RepositorioDesarrollo.code-workspace  # Workspace de VS Code
├── .python-version         # Especificación de versión de Python
├── .gitignore             # Reglas de ignorado de Git
└── README.md              # Este archivo
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
│  CAPA 3: Controladores (Controllers/Routes)           │
│  Responsabilidad: Recibir solicitudes HTTP y responder │
│  Ejemplo: @router.post("/entities")                    │
└──────────────────────┬──────────────────────────────────┘
                       ↓ Delega al servicio
┌─────────────────────────────────────────────────────────┐
│  CAPA 2: Servicios (Business Logic)                     │
│  Responsabilidad: Implementar reglas de negocio        │
│  Ejemplo: def create(entity_data) -> BaseEntity        │
└──────────────────────┬──────────────────────────────────┘
                       ↓ Accede a los datos
┌─────────────────────────────────────────────────────────┐
│  CAPA 1: Modelos (Domain Entities)                    │
│  Responsabilidad: Representar y estructurar los datos │
│  Ejemplo: class BaseEntity: ...                        │
└─────────────────────────────────────────────────────────┘
                       ↑
                  Devuelve respuesta
```

### Desglose de Cada Capa

**CAPA 1: Modelos (Entidades de Dominio)**
- **Ubicación**: `app/models/`
- **Responsabilidad**: Definir la estructura de datos
- **Qué hace**: Representa entidades del negocio usando clases que extienden `BaseEntity`
- **Ejemplo**: `BaseEntity` con atributos como `id`, `created_at`, `updated_at`
- **Principio**: DRY mediante `BaseEntity` que reutiliza id, timestamps

**CAPA 2: Servicios (Lógica de Negocio)**
- **Ubicación**: `app/services/`
- **Responsabilidad**: Ejecutar la lógica de negocio compleja
- **Qué hace**: Procesa datos, valida reglas, orquesta operaciones usando genéricos
- **Ejemplo**: `BaseService<T>` que provee operaciones CRUD genéricas
- **Principio**: Una clase de servicio genérica reutilizable por entidad

**CAPA 3: Controladores (Endpoints HTTP)**
- **Ubicación**: `app/controllers/`
- **Responsabilidad**: Manejar solicitudes HTTP y respuestas
- **Qué hace**: Recibe JSON, delega al servicio, devuelve resultado
- **Principio**: Solo HTTP, sin lógica de negocio

### Ventajas de Esta Estructura

- **Separación de responsabilidades**: Cada capa tiene un propósito claro
- **Reutilización**: `BaseEntity` y `BaseService` se usan en múltiples características
- **Testabilidad**: Cada capa se puede probar de forma independiente
- **Mantenibilidad**: Cambios en la lógica no afectan endpoints
- **Escalabilidad**: Fácil agregar nuevas características siguiendo el patrón

```
HTTP Requests
↓
┌─────────────────────────────┐
│  Controllers (Routes)       │ ← Endpoints HTTP
│  BaseService<T>             │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Services (BaseService)     │ ← Lógica central, procesamiento
│  BaseService<T>             │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Models (BaseEntity)        │ ← Representación de datos
│  BaseEntity                 │
└─────────────────────────────┘
```

### Características Clave

- **Clases Base Genéricas**: `BaseEntity` y `BaseService<T>` para reutilización
- **Validación Pydantic**: Esquemas type-safe para solicitudes/respuestas
- **Clean Code**: KISS, DRY, YAGNI, principios SOLID
- **Tests Completos**: Suite de tests cubriendo modelos, servicios y endpoints
- **Estructura Profesional**: Directorios organizados siguiendo mejores prácticas

## 🧪 Endpoints de API

### Endpoints Genéricos (vía BaseService)

```
GET    /api/{entity}          - Obtener todos los registros
POST   /api/{entity}          - Crear nuevo registro
GET    /api/{entity}/{id}      - Obtener registro por ID
PUT    /api/{entity}/{id}      - Actualizar registro
DELETE /api/{entity}/{id}      - Eliminar registro
```

Los endpoints específicos se definen extendiendo las clases base genéricas.

## 🛠️ Tecnologías y Herramientas

- **Framework**: FastAPI
- **Validación**: Pydantic
- **Testing**: pytest
- **Calidad de Código**: Ruff, Black
- **Gestión de Entornos**: uv
- **Versión de Python**: 3.10+
- **Editor**: Visual Studio Code con extensión de Python

## 📋 Principios de Desarrollo

- **Clean Code**: KISS, DRY, YAGNI, SOLID
- **TDD**: Test-Driven Development
- **FDD**: Feature-Driven Development
- **Arquitectura**: Patrón de tres capas MVC

## 🔧 Integración con VS Code

Este proyecto incluye configuración de VS Code para:

- ✅ **Activación automática del entorno virtual** al abrir el proyecto
- ✅ **Formateo Python** con Ruff
- ✅ **Integración de Pytest** para ejecutar tests
- ✅ **Configuraciones de lanzamiento** para debug
- ✅ **Extensiones recomendadas** para el equipo

Abre `.vscode/settings.json` para ver la configuración completa del editor.

### Extensiones Recomendadas

Para una mejor experiencia de desarrollo, instala estas extensiones en VS Code:

- Python (Microsoft)
- Ruff (Astral)
- Pylance (Microsoft)

## 🔧 Solución de Problemas (Windows)

### Error: "No se puede cargar el archivo .venv\Scripts\Activate.ps1 porque la ejecución de scripts está deshabilitada..."

**Solución:** Ejecuta en PowerShell como administrador:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego vuelve a intentar: `.venv\Scripts\Activate.ps1`

---

### Los imports de `fastapi` y `uvicorn` aparecen en amarillo en VS Code

**Solución:**

1. Asegúrate de haber ejecutado `uv sync`
2. Presiona `Ctrl+Shift+P` → `Python: Select Interpreter`
3. Selecciona: `.\.venv\Scripts\python.exe` (debe decir "Recommended")

---

### El entorno no se activa automáticamente en VS Code

**Solución:**

1. **Verifica que abriste la carpeta del proyecto**, no solo un archivo individual
2. Cierra completamente VS Code y vuelve a abrirlo desde la carpeta raíz
3. Si persiste, actívalo manualmente:

```powershell
.venv\Scripts\Activate.ps1
```

---

### `uv` no está reconocido como comando

**Solución:** Instala uv siguiendo las instrucciones en:
https://docs.astral.sh/uv/getting-started/installation/

```powershell
# Usando winget (recomendado en Windows)
winget install --id=astral-sh.uv -e
```

---

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

**Última Actualización**: 28 de abril de 2026
**Versión de Python**: 3.10+
**Estado**: Desarrollo Activo
