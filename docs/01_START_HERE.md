# 🚀 Comienza Aquí - Guía de 5 Minutos

## ¡Bienvenido! 

Tu aplicación FastAPI con arquitectura profesional está lista.

### Paso 1: Instalar Dependencias (1 minuto)

```bash
# Opción A: Con pip (recomendado si UV no está instalado)
pip install -r requirements.txt

# Opción B: Con pip en modo editable para desarrollo
pip install -e ".[dev]"

# Opción C: Con UV (si lo tienes instalado)
uv pip install -e ".[dev]"
```

### Paso 2: Ejecutar la Aplicación (1 minuto)

```bash
# Opción A: Script de acceso rápido
python AccesoRapido.py

# Opción B: Directo con uvicorn
uvicorn app.main:app --reload

# Opción C: Como módulo
python -m app.main
```

### Paso 3: Abrir el Navegador (1 minuto)

Abre uno de estos URLs:

- **Swagger UI (Recomendado)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API**: http://localhost:8000

### Paso 4: Probar un Endpoint (1 minuto)

En Swagger UI, expande "users" y presiona "Try it out":

```bash
# O desde terminal:
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User"
  }'
```

### Paso 5: Ejecutar Tests (1 minuto)

```bash
pytest -v
```

---

## 📚 Documentación

Para profundizar, lee estos archivos en este orden:

1. **QUICK_START.md** (20 min)
   - Ejemplos prácticos
   - Comandos útiles
   - Troubleshooting

2. **ARCHITECTURE.md** (40 min)
   - Explicación completa de la arquitectura
   - Cómo agregar nuevas características
   - Patrones de diseño

3. **El Código** (exploración)
   - Cada archivo tiene docstrings
   - Ejemplos en los modelos, servicios y controladores

---

## ✨ Lo Que Acabas de Obtener

### 3 Capas Claras

```
Controllers (app/controllers/)
    ↓
Services (app/services/)
    ↓
Models (app/models/)
```

### Clean Code + SOLID

- ✅ Código simple y mantenible
- ✅ Fácil de extender
- ✅ Bien documentado
- ✅ Con tests

### Característica Completa de Ejemplo

**Usuarios** con:
- Crear, leer, actualizar, eliminar
- Activar/desactivar
- Búsqueda por email
- Validaciones

---

## 🎯 Próximo: Agregar Nueva Característica

### Ejemplo: Agregar "Posts"

1. **Crear el modelo** (`app/models/post.py`)
   ```python
   class Post(BaseEntity):
       title: str
       content: str
       author_id: UUID
   ```

2. **Crear el servicio** (`app/services/post_service.py`)
   ```python
   class PostService(BaseService[Post]):
       def get_by_author(self, author_id: UUID):
           ...
   ```

3. **Crear esquemas** (`app/schemas/post_schemas.py`)
   ```python
   class PostCreateRequest(BaseModel):
       title: str
       content: str
   ```

4. **Crear endpoints** (`app/controllers/post_routes.py`)
   ```python
   router = APIRouter(prefix="/posts")
   
   @router.post("")
   def create(request: PostCreateRequest, service = Depends()):
       ...
   ```

5. **Registrar router** (`app/main.py`)
   ```python
   app.include_router(post_routes.router, prefix=settings.api_prefix)
   ```

6. **Escribir tests** (`tests/test_post.py`)

---

## 🆘 Problemas Comunes

### "ModuleNotFoundError: No module named 'app'"

**Solución**: Asegúrate de ejecutar desde el directorio raíz del proyecto

```bash
cd C:\Programas\RepositorioDesarrollo
python AccesoRapido.py
```

### "Address already in use"

**Solución**: El puerto 8000 está ocupado, usa otro puerto:

```bash
uvicorn app.main:app --reload --port 8001
```

### Los tests no pasan

**Solución**: Instala dependencias de desarrollo:

```bash
pip install -e ".[dev]"
pytest -v
```

---

## 📞 ¿Necesitas Ayuda?

1. **Revisa QUICK_START.md** - Tiene ejemplos completos
2. **Revisa ARCHITECTURE.md** - Documentación detallada
3. **Lee los docstrings** - Cada función está documentada
4. **Mira los tests** - Son ejemplos de uso

---

## 🎉 ¡Listo!

Ya tienes una aplicación profesional. Ahora:

1. ✅ Instala dependencias
2. ✅ Ejecuta la app
3. ✅ Abre http://localhost:8000/docs
4. ✅ Prueba los endpoints
5. ✅ Lee QUICK_START.md para más

**¡Felicidades! 🚀**
