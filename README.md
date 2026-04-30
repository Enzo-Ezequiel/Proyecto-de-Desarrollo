# RepositorioDesarrollo

Una aplicación profesional con arquitectura de tres capas usando FastAPI, siguiendo principios de Clean Code y Feature-Driven Development.

#### ✅ Requisitos Previos
Antes de comenzar, asegúrate de tener instalado:
*   **Python 3.10+**
*   **uv** - Gestor de paquetes y entornos virtuales
*   **Git**
*   **Visual Studio Code** (recomendado)
*   **Sistema operativo: Windows** (PowerShell)
*   **Docker Desktop** - Para ejecutar la base de datos MongoDB localmente

#### 🚀 Inicio Rápido

##### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd Proyecto-de-Desarrollo
2. Instalar dependencias
uv sync
Importante: Una vez ejecutado uv sync, debes activar el entorno virtual antes de continuar:
Opción A: Activación Manual
Abre PowerShell en la raíz del proyecto y ejecuta:
.venv\Scripts\Activate.ps1
💡 Nota: Si ves un error sobre políticas de ejecución, ejecuta primero:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
Verás (Proyecto-de-Desarrollo) al inicio de tu línea de comandos cuando esté activo.
Opción B: VS Code (Automático) ⭐⭐ Recomendado
El proyecto está configurado para activar el entorno automáticamente:
Abre VS Code desde la carpeta del proyecto (code .)
Abre una terminal integrada (`Ctrl + ``)
El entorno se activará solo (verás (Proyecto-de-Desarrollo) en el prompt)
3. Levantar la Base de Datos (Docker)
Antes de iniciar la aplicación, asegúrate de que Docker Desktop esté abierto y ejecuta este comando para iniciar MongoDB:
docker-compose up -d
4. Verificar que el entorno funciona
Ejecuta en tu terminal:
python validate_fixes.py
Si ves el mensaje ✅ sin errores, el entorno está listo.
5. Ejecutar la Aplicación
uvicorn app.main:app --reload
6. Acceder a la API
API: http://127.0.0.1:8000
Documentación Swagger: http://127.0.0.1:8000/docs
Documentación ReDoc: http://127.0.0.1:8000/redoc
7. Ejecutar Tests
pytest

--------------------------------------------------------------------------------
📁 Estructura del Proyecto
📚 Documentación
Para información completa sobre cómo usar y desarrollar en este proyecto, consulta:
📖 Guía Completa - Todo lo que necesitas saber:
Inicio rápido (5 minutos)
Explicación detallada de la arquitectura de tres capas
Ejemplos de endpoints de API
Cómo agregar nuevas características
Ejecución de tests
Troubleshooting
Recursos útiles
🏗️ Arquitectura de Tres Capas
Este proyecto implementa una arquitectura de tres capas, que separa la aplicación en tres niveles independientes de responsabilidad. Esto permite que el código sea más modular, testeable y mantenible.
¿Qué significa "Arquitectura de Tres Capas"?
La arquitectura de tres capas divide la aplicación en tres componentes horizontales que se comunican entre sí de forma jerárquica:
CAPA 1: Modelos (Models) - La base que representa los datos
CAPA 2: Servicios (Services) - La lógica que procesa esos datos
CAPA 3: Controladores (Controllers) - Los puntos de acceso HTTP
El flujo de información es unidireccional: Las solicitudes HTTP bajan por las capas, y las respuestas suben.
Desglose de Cada Capa
CAPA 1: Modelos (Entidades de Dominio)
Ubicación: app/models/
Responsabilidad: Definir la estructura de datos
Ejemplo: DocumentoPDF que hereda de BaseEntity (reutilizando id y timestamps).
CAPA 2: Servicios (Lógica de Negocio)
Ubicación: app/services/
Responsabilidad: Ejecutar la lógica de negocio compleja, validaciones y conexión con el repositorio de Base de Datos.
Ejemplo: pdf_service.py que prepara el documento y usa MongoRepository para guardarlo.
CAPA 3: Controladores (Endpoints HTTP)
Ubicación: app/controllers/
Responsabilidad: Manejar solicitudes HTTP, validación Pydantic (Capa Schemas) y respuestas.
Ejemplo: pdf_routes.py (Endpoint POST /pdfs/) que solo maneja HTTP y delega la tarea al servicio.
Ventajas de Esta Estructura
Separación de responsabilidades: Cada capa tiene un propósito claro
Reutilización: BaseEntity y BaseService se usan en múltiples características
Testabilidad: Cada capa se puede probar de forma independiente
Mantenibilidad: Cambios en la lógica no afectan endpoints
🧪 Endpoints de API
Usuarios (/api/v1/users): Endpoints genéricos de lectura y eliminación.
Documentos PDF (/pdfs/): Creación y guardado de registros de archivos PDF extraídos.
🛠️ Tecnologías y Herramientas
Framework: FastAPI
Base de Datos: MongoDB (Motor / AsyncIOMotorClient)
Contenedores: Docker & Docker Compose
Validación: Pydantic
Testing: pytest
Gestión de Entornos: uv
Versión de Python: 3.10+
📋 Principios de Desarrollo
Clean Code: KISS, DRY, YAGNI, SOLID
TDD / FDD: Test-Driven & Feature-Driven Development
Arquitectura: Patrón de tres capas
🔧 Integración con VS Code
Este proyecto incluye configuración de VS Code para:
✅ Activación automática del entorno virtual al abrir el proyecto
✅ Formateo Python con Ruff
✅ Integración de Pytest para ejecutar tests
Abre .vscode/settings.json para ver la configuración completa del editor.
🔧 Solución de Problemas (Windows)
Error: "No se puede cargar el archivo .venv\Scripts\Activate.ps1 porque la ejecución de scripts está deshabilitada..."
Solución: Ejecuta en PowerShell como administrador:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
Luego vuelve a intentar: .venv\Scripts\Activate.ps1

--------------------------------------------------------------------------------
Los imports de fastapi y uvicorn aparecen en amarillo en VS Code
Solución:
Asegúrate de haber ejecutado uv sync
Presiona Ctrl+Shift+P → Python: Select Interpreter
Selecciona: .\.venv\Scripts\python.exe (debe decir "Recommended")

--------------------------------------------------------------------------------
El entorno no se activa automáticamente en VS Code
Solución:
Verifica que abriste la carpeta del proyecto, no solo un archivo individual
Cierra completamente VS Code y vuelve a abrirlo desde la carpeta raíz

--------------------------------------------------------------------------------
📝 Objetivos Originales del Proyecto
Extraer texto de archivos PDF
Resumir usando modelos de IA (Gemini)
Arquitectura profesional de tres capas
Principios de Clean Code
Documentación completa
🤝 Contribuyendo
Al agregar nuevas características:
Crear una nueva rama
Seguir la arquitectura de tres capas
Agregar tests unitarios e integración
Crear un pull request
📄 Licencia
Este es un proyecto de desarrollo. Consulte el archivo LICENSE para más detalles.
📞 Soporte
Para más información, consulte la documentación en el directorio docs/ o revise los comentarios en el código.

--------------------------------------------------------------------------------
Última Actualización: 29 de abril de 2026 | Versión de Python: 3.10+ | Estado: Desarrollo Activo