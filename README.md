# PDF Extractext

Aplicación FastAPI con arquitectura de tres capas siguiendo principios de Clean Code y Feature-Driven Development que extrae texto de archivos en formato PDF y convierte su contenido en formato txt.

## Integrantes
- Albarracín Valentina
- Buttini Ezequiel
- Cano Matías
- Gomez Manuel
- Pérez Buttini Nicolás
- Peñasco Valentina

## Requisitos Previos al uso de la aplicación

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) - Gestor de paquetes y entornos virtuales
- Git
- Visual Studio Code (recomendado)
- Docker Desktop - Para MongoDB

## Inicio rápido de desarollo 

### 1. Clonar el repositorio

```powershell
git clone <repository-url>
cd Proyecto-de-Desarrollo
```

### 2. Instalar dependencias

```powershell
uv sync
```

### 3. Activar entorno virtual

Opción A (Manual) para usuarios desde terminal powershell:

```powershell
.venv\Scripts\Activate.ps1
```

Si tienes error de políticas de ejecución:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Opción para usuarios desde wsl, ubuntu:
source .venv/bin/activate

Opción B-powershell-(VS Code - Recomendado):
Abre VS Code desde la carpeta del proyecto. El entorno se activará automáticamente.
Opción B-wsl-(VS Code - Recomendado):
Abre VS Code desde la carpeta del proyecto escribiendo code . en la terminal. El entorno se activará automáticamente si tienes la extensión de Python configurada.

### 4. Configurar variables de entorno

```powershell
# Copiar plantilla
cp config\.env.example .env
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

- http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 7. Ejecutar tests

```powershell
uv run pytest tests/ -v
```

---

## Inicio rapido para ejecucion

Para ejecutar este proyecto, ofrecemos dos alternativas: una ejecución rápida 100% en contenedores (ideal para evaluación) y una configuración local completa para desarrollo continuo. Esta opción despliega tanto la aplicación web como la base de datos MongoDB en contenedores aislados, sin necesidad de instalar dependencias ni configurar entornos virtuales en tu máquina local.

### 1. Clonar el repositorio

```powershell
git clone <repository-url>
cd Proyecto-de-Desarrollo
```

### 2. Configurar variables de entorno

```powershell
cp config\.env.example .env
```

### 3. Construir y levantar todo el ecosistema
Solo va a funcionar con docker desktop insatalado y abierto:

```powershell
docker-compose up --build -d
```
### 4. Acceder a la API
- API: http://127.0.0.1:8000
- Documentación Swagger: http://127.0.0.1:8000/docs
- Documentación ReDoc: http://127.0.0.1:8000/redoc

## Estructura del Proyecto

```
app/
├── main.py                 # Punto de entrada
├── controllers/            # Endpoints HTTP
├── services/              # Lógica de negocio
├── models/                # Entidades de dominio
├── schemas/               # Validación Pydantic
└── core/
    ├── config.py
    ├── database.py
    ├── exceptions.py
    ├── repository.py
    └── middleware/

config/
├── requirements.txt
└── .env.example

tests/                     # Suite de pruebas

docs/                      # Documentación

scripts/
└── run.py                 # Lanzador de aplicación
```

---

## Arquitectura de Tres Capas

El proyecto está organizado en tres capas independientes que se comunican de forma jerárquica:

```
Solicitud HTTP
     ↓
┌─────────────────────────────────────┐
│ CAPA 3: Controladores (Routes)     │
│ Responsabilidad: HTTP y routing    │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ CAPA 2: Servicios (Business Logic) │
│ Responsabilidad: Lógica de negocio │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ CAPA 1: Modelos (Domain Entities)  │
│ Responsabilidad: Estructura de datos│
└─────────────────────────────────────┘
```

### CAPA 1: Modelos

- Ubicación: `app/models/`
- Entidades del negocio que extienden `BaseEntity`
- Definen estructura y atributos

### CAPA 2: Servicios

- Ubicación: `app/services/`
- Lógica de negocio y orquestación
- Servicios genéricos CRUD mediante `BaseService<T>`

### CAPA 3: Controladores

- Ubicación: `app/controllers/`
- Endpoints HTTP y validación Pydantic
- Sin lógica de negocio

---

## Documentación

Consulta `/docs` para referencias completas:

- **Índice:** [INDEX.md](docs/INDEX.md)
- **Guía Completa:** [GUIA_COMPLETA.md](docs/GUIA_COMPLETA.md)
- **Dependencias:** [BIBLIOTECAS.md](docs/BIBLIOTECAS.md)
- **Análisis de Código:** [VERIFICACION_CLEAN_CODE.md](docs/VERIFICACION_CLEAN_CODE.md)

---

## Stack Tecnológico

- FastAPI
- Pydantic
- Motor (MongoDB async)
- Pytest
- Python 3.10+

---

## Principios de Desarrollo

- Clean Code (KISS, DRY, YAGNI, SOLID)
- Test-Driven Development (TDD)
- Feature-Driven Development (FDD)

---

## Solución de Problemas

**Error de políticas de ejecución en PowerShell:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Imports en amarillo en VS Code:**

1. Ejecutar `uv sync`
2. Ctrl+Shift+P → Python: Select Interpreter
3. Seleccionar `.\.venv\Scripts\python.exe`

**uv no reconocido:**

```powershell
winget install --id=astral-sh.uv -e
```

---

## Contribuyendo

1. Crear rama
2. Seguir arquitectura de tres capas
3. Agregar tests
4. Actualizar documentación
5. Crear pull request

---

**Última actualización:** 20 de mayo de 2026
**Versión de Python:** 3.10+
**Estado:** Desarrollo activo
