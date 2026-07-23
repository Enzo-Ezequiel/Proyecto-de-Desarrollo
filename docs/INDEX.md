# Índice de Documentación

Documentación del proyecto PDF Extractor - Aplicación FastAPI con arquitectura de tres capas.

## Navegación Rápida

Nuevo en el proyecto
- [README.md](../README.md) - Inicio rápido y descripción general

Desarrollo
- [GUIA_COMPLETA.md](GUIA_COMPLETA.md) - Guía integral de arquitectura y uso
- [BIBLIOTECAS.md](BIBLIOTECAS.md) - Dependencias y justificación
- [VERIFICACION_CLEAN_CODE.md](VERIFICACION_CLEAN_CODE.md) - Análisis de calidad de código
- [LISTA_VERIFICACION_IMPLEMENTACION.md](LISTA_VERIFICACION_IMPLEMENTACION.md) - Estado de implementación

---

## Documentos Disponibles

### GUIA_COMPLETA.md
Guía completa: configuración, arquitectura de tres capas, endpoints, pruebas y solución de problemas. Referencia para desarrolladores.

### BIBLIOTECAS.md
Dependencias: FastAPI, Pydantic, Motor, Pytest. Justificación arquitectónica de cada librería.

### VERIFICACION_CLEAN_CODE.md
Análisis de violaciones a Clean Code (KISS, DRY, YAGNI, SOLID) con ejemplos de código y correcciones aplicadas.

### LISTA_VERIFICACION_IMPLEMENTACION.md
Estado de implementación: checklist de Clean Code, TDD, 12-Factor App y Arquitectura de Tres Capas.

---

## Estructura del Proyecto

```
app/
├── main.py                    # Punto de entrada
├── controllers/
│   └── pdf_routes.py         # Endpoints HTTP (Capa 3)
├── services/
│   ├── base_service.py       # Servicio genérico CRUD
│   └── pdf_service.py        # Lógica de negocio PDF (Capa 2)
├── models/
│   ├── base_model.py         # Clase base (BaseEntity)
│   └── pdf_document.py       # Entidad de dominio (Capa 1)
├── schemas/
│   └── pdf_schemas.py        # Validación Pydantic
└── core/
    ├── config.py             # Settings (12-Factor)
    ├── database.py           # Conexión MongoDB
    ├── exceptions.py         # Excepciones de dominio
    ├── repository.py         # Interfaz Repository + InMemory
    ├── mongo_repository.py   # Implementación MongoDB
    ├── utils.py              # Logger y utilidades
    └── middleware/
        └── middleware.py     # Middleware de tamaño

config/
├── .env.example              # Plantilla de entorno (desarrollo)
└── .env.example.docker       # Plantilla de entorno (Docker)

tests/
├── conftest.py               # Fixtures compartidas
└── test_pdfs.py              # Tests de PDFs

docs/                         # Documentación

scripts/
└── run.py                    # Lanzador de aplicación
```

## Stack Tecnológico

Python 3.10+, FastAPI, MongoDB (Motor), Pytest, Pydantic

## Rutas de Inicio

**Primer uso:** [README.md](../README.md)

**Desarrollo:** [GUIA_COMPLETA.md](GUIA_COMPLETA.md)

**Calidad:** [VERIFICACION_CLEAN_CODE.md](VERIFICACION_CLEAN_CODE.md)

---

**Última actualización:** 23 de julio de 2026
**Estado:** Desarrollo activo
