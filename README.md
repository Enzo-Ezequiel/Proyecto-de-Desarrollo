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

## Inicio rápido para desarollo 

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
# Copiar plantilla para desarrollo
cp config/.env.example .env
```

### 5. Iniciar MongoDB (Docker)

Para desarrollar localmente, solo necesitamos levantar la base de datos simulando "la nube":

```powershell
# Abre una terminal en la carpeta `dockerMongo` (fuera del proyecto principal) y ejecuta:
docker-compose up -d
```

### 6. Ejecutar la aplicación

Con la base de datos encendida, levantamos la aplicación de forma local:

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

Los 10 tests de `tests/test_pdfs.py` usan un repositorio en memoria (`InMemoryRepository`) inyectado vía `app.dependency_overrides`, así que corren solos, sin necesitar el paso 5 (Mongo levantada). Es el primer chequeo antes de probar contra la app real.

### 8. Probar el flujo completo contra la app real (verificación manual)

Con Mongo y la app corriendo (pasos 5 y 6), esto es un paso a paso para confirmar en caliente que el CRUD completo funciona de punta a punta — subir un PDF, ver que se rechacen duplicados y archivos demasiado grandes, y confirmar que el borrado es real.

**8.1. Generar un PDF de prueba** (o usá cualquier `.pdf` real que tengas a mano):

```powershell
uv run python -c "import sys; sys.path.insert(0, 'tests'); from conftest import build_minimal_pdf; open('prueba.pdf','wb').write(build_minimal_pdf('Texto de prueba end-to-end.'))"
```

**8.2. Subir el PDF** (debe devolver `201` y el texto extraído):

```powershell
curl.exe -s -w "`nHTTP %{http_code}`n" -X POST http://127.0.0.1:8000/api/v1/pdfs/ -F "file=@prueba.pdf"
```

Guardá el `id` que te devuelve en `datos.id` — lo vas a necesitar en los pasos 8.4 y 8.5.

**8.3. Subir el mismo PDF de nuevo** (debe rechazarlo por duplicado, `400`):

```powershell
curl.exe -s -w "`nHTTP %{http_code}`n" -X POST http://127.0.0.1:8000/api/v1/pdfs/ -F "file=@prueba.pdf"
```

**8.4. Buscarlo por id** (reemplazá `<ID>` por el que guardaste en 8.2; debe devolver `200`):

```powershell
curl.exe -s -w "`nHTTP %{http_code}`n" http://127.0.0.1:8000/api/v1/pdfs/<ID>
```

**8.5. Borrarlo y confirmar que ya no existe** (`200` al borrar, `404` al volver a buscarlo):

```powershell
curl.exe -s -w "`nHTTP %{http_code}`n" -X DELETE http://127.0.0.1:8000/api/v1/pdfs/<ID>
curl.exe -s -w "`nHTTP %{http_code}`n" http://127.0.0.1:8000/api/v1/pdfs/<ID>
```

**8.6. Probar el límite de tamaño** (`PDF_MAX_SIZE_MB` en tu `.env`; debe devolver `413`):

```powershell
uv run python -c "import sys; sys.path.insert(0, 'tests'); from conftest import build_minimal_pdf; open('grande.pdf','wb').write(build_minimal_pdf('grande') + bytes(6*1024*1024))"
curl.exe -s -w "`nHTTP %{http_code}`n" -X POST http://127.0.0.1:8000/api/v1/pdfs/ -F "file=@grande.pdf"
```

Resultado esperado de todo el recorrido:

| Paso | Resultado esperado |
|---|---|
| 8.2 — subir PDF válido | `201`, `contenido_pdf` con el texto extraído |
| 8.3 — subir el mismo PDF de nuevo | `400`, `"... ya existe"` |
| 8.4 — `GET` por id | `200`, mismos datos que en 8.2 |
| 8.5 — `DELETE` y `GET` posterior | `200` y luego `404` |
| 8.6 — PDF de ~6MB (> límite configurado) | `413`, mensaje con el límite real (ej. `5MB`) |

Si los seis pasos dan el código esperado, el CRUD, la validación de tamaño, el anti-duplicados y la extracción de texto están funcionando de punta a punta contra una MongoDB real (no solo en los tests).

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
cp config/.env.example.docker docker/.env
```

### 3. Construir y levantar todo el ecosistema
Solo va a funcionar con docker desktop insatalado y abierto:

```powershell
# Abre una terminal en la carpeta dockerMongo (fuera del proyecto principal) y ejecuta:
docker-compose up -d
# En la terminal de tu proyecto principal, navega hacia la carpeta docker y levanta la app:
cd docker
docker-compose up -d --build
```
### 4. Ejecutar tests
Como el entorno es 100% Docker y no tienes dependencias locales, ejecuta los tests directamente dentro del contenedor de la aplicación:

```powershell
docker exec -it fastapi_app uv run pytest tests/ -v
```

### 5. Acceder a la API
- API: http://127.0.0.1:8000
- Documentación Swagger: http://127.0.0.1:8000/docs
- Documentación ReDoc: http://127.0.0.1:8000/redoc

---

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
├── .env.example
└── .env.example.docker

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

- **Clean Code** : KISS, DRY, YAGNI, SOLID
-   **TDD** : Test-Driven Development
-   **FDD** : Feature-Driven Development
-   **Arquitectura** : Patrón de tres capas MVC
-   **12-Factor App** : Gestión estricta de dependencias, configuraciones (vía Pydantic) y logs (stdout).

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

**Última actualización:** 26 de julio de 2026
**Versión de Python:** 3.10+
**Estado:** Desarrollo activo
