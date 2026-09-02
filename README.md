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
- Docker Desktop — Para MongoDB en desarrollo local, o para levantar el proyecto completo en contenedores

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

### 5. Iniciar MongoDB

El desarrollo local necesita una instancia de MongoDB corriendo. Si no tenés una, levantá un contenedor:

```powershell
docker run -d --name mongo_dev -p 27017:27017 -v mongo_dev_data:/data/db mongo:7.0
```

Con `DATABASE_URL="mongodb://127.0.0.1:27017"` en tu `.env` (paso 4), la app se conecta ahí. Si preferís no instalar nada localmente, usá el stack Docker completo (ver [Inicio rápido con Docker](#inicio-rápido-con-docker)), que ya incluye la base.

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

Los 17 tests de `tests/test_pdfs.py` usan un repositorio en memoria (`InMemoryRepository`) inyectado vía `app.dependency_overrides`, así que corren solos, sin necesitar el paso 5 (Mongo levantada). Es el primer chequeo antes de probar contra la app real. El detalle de qué se cubre y qué queda fuera a propósito está en [Estrategia de testing](#estrategia-de-testing).

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

**8.5. Renombrarlo** (debe devolver `200` con el `nombre_pdf` nuevo):

```powershell
curl.exe -s -w "`nHTTP %{http_code}`n" -X PATCH http://127.0.0.1:8000/api/v1/pdfs/<ID> -H "Content-Type: application/json" -d "{\"nombre_pdf\": \"renombrado.pdf\"}"
```

**8.6. Borrarlo y confirmar que ya no existe** (`200` al borrar, `404` al volver a buscarlo):

```powershell
curl.exe -s -w "`nHTTP %{http_code}`n" -X DELETE http://127.0.0.1:8000/api/v1/pdfs/<ID>
curl.exe -s -w "`nHTTP %{http_code}`n" http://127.0.0.1:8000/api/v1/pdfs/<ID>
```

**8.7. Probar el límite de tamaño** (`PDF_MAX_SIZE_MB` en tu `.env`; debe devolver `413`):

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
| 8.5 — `PATCH` renombrando | `200`, con el `nombre_pdf` nuevo |
| 8.6 — `DELETE` y `GET` posterior | `200` y luego `404` |
| 8.7 — PDF de ~6MB (> límite configurado) | `413`, mensaje con el límite real (ej. `5MB`) |

Si los siete pasos dan el código esperado, el CRUD completo, la validación de tamaño, el anti-duplicados y la extracción de texto están funcionando de punta a punta contra una MongoDB real (no solo en los tests).

---

## Inicio rápido con Docker

El `docker-compose.yml` de la carpeta `docker/` levanta el proyecto completo desde un clon limpio: la aplicación FastAPI y una instancia de MongoDB con persistencia. No hace falta instalar Python, `uv` ni configurar entornos virtuales en la máquina.

### 1. Clonar el repositorio

```powershell
git clone <repository-url>
cd Proyecto-de-Desarrollo
```

### 2. Configurar variables de entorno

Copiar la plantilla a `docker/.env` y ajustar lo que haga falta:

```powershell
cp docker/.env.example docker/.env
```

`docker/.env` está ignorado por git; `docker/.env.example` es la plantilla versionada que exige 12-Factor. Compose lee `docker/.env` tanto para inyectar las variables dentro del contenedor (`env_file`) como para resolver `${APP_VERSION}` en el tag de la imagen.

### 3. Construir y levantar todo

```powershell
cd docker
docker compose up -d --build
```

Se construye la imagen de la app y arrancan dos servicios: `mongo` (contenedor `mongo_db`) y `app` (contenedor `fastapi_app`), que espera a `mongo` vía `depends_on`.

### 4. Ejecutar los tests dentro del contenedor

```powershell
docker exec -it fastapi_app uv run pytest tests/ -v
```

### 5. Acceder a la API

- API: http://127.0.0.1:8000
- Documentación Swagger: http://127.0.0.1:8000/docs
- Documentación ReDoc: http://127.0.0.1:8000/redoc

### 6. Detener el stack y persistencia de datos

```powershell
docker compose down      # detiene y elimina los contenedores; los datos de Mongo se conservan
docker compose down -v   # además elimina el volumen mongo_data: borra todos los datos
```

Los datos de MongoDB viven en el volumen nombrado `mongo_data`, no en la capa escribible del contenedor. Por eso sobreviven a `docker compose down`, a `docker rm` y a reconstrucciones de la imagen. La única forma de borrarlos es `docker compose down -v` (o `docker volume rm` sobre el volumen).

### Variables de entorno

Todas se definen en `docker/.env` (plantilla en `docker/.env.example`):

| Variable | Para qué sirve | Valor en Docker |
|---|---|---|
| `MONGO_DB_NAME` | Nombre de la base que usa la app. **Obligatoria**, sin default. | `repositorio_db` |
| `DATABASE_URL` | URI de conexión a MongoDB. **Obligatoria**, sin default. Dentro del compose apunta al servicio `mongo`. | `mongodb://mongo:27017` |
| `APP_NAME` | Nombre que la API expone en su metadata y usa el logger. | `Repositorio Desarrollo` |
| `APP_VERSION` | Versión de la API; Compose la usa además como tag de la imagen (`repositoriodesarrollo:<version>`). | `0.1.0` |
| `DEBUG` | Modo debug de la aplicación. | `False` |
| `HOST` | Interfaz donde escucha Uvicorn dentro del contenedor. | `0.0.0.0` |
| `PORT` | Puerto interno de la app (se mapea a `8000` del host). | `8000` |
| `CORS_ORIGINS` | Lista JSON de orígenes permitidos por CORS. | `["http://localhost", "http://localhost:3000", "http://localhost:8000"]` |
| `PDF_MAX_SIZE_MB` | Tamaño máximo al subir un PDF; si se supera, la API responde `413`. | `5` |
| `LOG_LEVEL` | Nivel del logger de la app (`DEBUG`, `INFO`, `WARNING`, ...). | `INFO` |

> **Stack de MongoDB separado.** Existe además un stack de MongoDB independiente, fuera de este repositorio, pensado para cuando el sistema se divida en microservicios y varios servicios compartan la misma base. En la etapa actual, monolítica, el `docker-compose.yml` de este repositorio es autocontenido y no depende de ese stack.

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
└── .env.example           # Plantilla de variables para desarrollo local (copiar a .env)

docker/
├── docker-compose.yml     # App + MongoDB con volumen nombrado mongo_data
└── .env.example           # Plantilla de variables (copiar a docker/.env)

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

### Convención de nombres: idioma por capa

El código mezcla idiomas de forma deliberada, no por descuido:

- **Infraestructura y contratos genéricos en inglés** — `BaseEntity`, `Repository`,
  `BaseService` y sus métodos (`add`, `get_by_id`, `get_all`, `update`, `delete`,
  `find_one`, `create`). Es vocabulario técnico estándar, reutilizable entre
  proyectos y alineado con las convenciones de FastAPI, Motor y la stdlib.
- **Dominio en español** — `DocumentoPDF`, `PdfService.procesar_y_guardar`,
  `renombrar`, `nombre_pdf`, `contenido_pdf`, `checksum`. El lenguaje del negocio es
  el del equipo y el de la cátedra; traducirlo agregaría una capa de mapeo mental
  sin valor.

Regla práctica: si el símbolo podría vivir igual en otro proyecto, va en inglés; si
solo tiene sentido hablando de este dominio (PDFs), va en español. Dentro de cada
capa el idioma es consistente.

---

## Estrategia de testing

La suite (`tests/test_pdfs.py`, 17 tests) entra al sistema por dos *seams* —
dos puntos de sustitución donde el test reemplaza una pieza real por otra.

### Qué se testea y en qué nivel

| Seam | Nivel | Tests | Cómo entra el test |
|---|---|---|---|
| **HTTP** | Integración capa 1 + capa 2 (controller + schemas + service) | 16 | `TestClient` de FastAPI contra la API real: rutas, status codes, validación Pydantic, flujo `controller → service → repository` |
| **Servicio** | Unitario | 1 (`test_pdf_service_unitario_sin_mongo`) | Instancia directa de `PdfService` con `InMemoryRepository`, sin HTTP, aislando las reglas de negocio (extracción de texto, rechazo de duplicados) |

### Sustitución por inversión de dependencias, no por mocks

El doble de test es `InMemoryRepository` (`app/core/repository.py`), una
implementación real del puerto abstracto `Repository[T]` — no un mock. Se inyecta
por el **mismo mecanismo que usa producción**:

- En los tests HTTP, `conftest.py` registra
  `app.dependency_overrides[get_pdf_service]` con un `PdfService` cableado a
  `InMemoryRepository`. FastAPI resuelve la dependencia igual que en producción;
  lo único que cambia es qué implementación del puerto recibe el service.
- En el test unitario, el repositorio se pasa por constructor:
  `PdfService(InMemoryRepository())`.

No se parchea ningún atributo privado ni se intercepta ningún internal. Es
inversión de dependencias real: el `type hint` apunta a la abstracción
(`repository: Repository[T]`) y el cableado concreto vive en un solo lugar.

### Las cuatro premisas

- **Rápidas** — la suite completa corre en fracciones de segundo (~0,3 s). Sin
  red y sin BD real: `conftest.py` fija `DATABASE_URL` a un host inexistente a
  propósito y ningún test abre una conexión.
- **Atómicas** — un comportamiento por test: un status code, una regla de
  validación o una transición de estado, no varios a la vez.
- **Inocuas** — no tocan estado externo. El almacenamiento es un `dict` en
  memoria que se descarta al terminar cada test.
- **Independientes** — cada test recibe un `InMemoryRepository` nuevo vía
  fixture; el orden de ejecución no altera el resultado.

**Herméticas:** la suite corre sobre un clon limpio sin `.env`, sin Mongo
levantada y sin configuración manual. Los settings se proveen desde
`conftest.py` antes de importar `app.*`.

### Qué queda fuera, a propósito

`MongoRepository` (`app/core/mongo_repository.py`) **no se ejercita** en la suite
automatizada: su coverage es ~36% y corresponde solo a las firmas de los
métodos, no a su lógica.

Es una decisión deliberada, no un olvido:

- `MongoRepository` es un adaptador delgado sobre Motor: traduce entre entidades
  del dominio y documentos de Mongo y delega en el driver. No contiene reglas de
  negocio propias.
- Cubrirlo exigiría una MongoDB real durante los tests, lo que rompería la
  hermeticidad recién conseguida: la suite dejaría de correr sobre un clon limpio
  sin infraestructura.
- El contrato que `MongoRepository` debe cumplir ya está definido por el puerto
  `Repository[T]` y verificado contra `InMemoryRepository`; ambas
  implementaciones son intercambiables (LSP).

Si la lógica de conversión del adaptador creciera lo suficiente como para
justificar la cobertura, se cubriría con un **test de integración** contra un
contenedor `mongo:7.0`, marcado `@pytest.mark.integration` y excluido de la
corrida unitaria por defecto. La verificación manual de punta a punta contra
Mongo real ya está en el [paso 8](#8-probar-el-flujo-completo-contra-la-app-real-verificación-manual)
del inicio rápido.

### Cómo correr la suite y el coverage

```powershell
# Suite completa — no necesita Mongo ni .env
uv run pytest tests/ -v

# Comprobar hermeticidad: la suite pasa aunque no exista .env
Rename-Item .env .env.bak ; uv run pytest tests/ ; Rename-Item .env.bak .env

# Coverage — requiere las dependencias de desarrollo
uv sync --extra dev
uv run pytest tests/ --cov=app --cov-report=term-missing
```

Coverage actual: **86% global**, con `mongo_repository.py` como única exclusión
relevante (ver arriba).

---

## Documentación

Consulta `/docs` para referencias completas:

- **Índice:** [INDEX.md](docs/INDEX.md)
- **Guía Completa:** [GUIA_COMPLETA.md](docs/GUIA_COMPLETA.md)
- **Dependencias:** [bibliotecas.md](docs/bibliotecas.md)

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
