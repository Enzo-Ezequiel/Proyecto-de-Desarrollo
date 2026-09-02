# Índice de Documentación

Documentación del proyecto Repositorio Desarrollo - Aplicación FastAPI con arquitectura de tres capas.

## Navegación Rápida

Nuevo en el proyecto
- [README.md](../README.md) - Inicio rápido y descripción general

Desarrollo
- [GUIA_COMPLETA.md](GUIA_COMPLETA.md) - Guía integral de arquitectura y uso
- [bibliotecas.md](bibliotecas.md) - Dependencias y justificación

---

## Documentos Disponibles

### GUIA_COMPLETA.md
Guía completa: configuración, arquitectura de tres capas, endpoints, pruebas y solución de problemas. Referencia para desarrolladores.

### bibliotecas.md
Dependencias: FastAPI, Pydantic, Motor, Pytest. Justificación arquitectónica de cada librería.

---

## Estructura del Proyecto

```
app/
├── main.py                 # Punto de entrada
├── controllers/            # Endpoints HTTP
├── services/              # Lógica de negocio
├── models/                # Entidades de dominio
├── schemas/               # Validación
└── core/
    ├── config.py
    ├── database.py
    ├── exceptions.py
    ├── repository.py
    └── middleware/

config/
└── .env.example

tests/                     # Suite de pruebas

docs/                      # Documentación
```

## Stack Tecnológico

Python 3.10+, FastAPI, MongoDB (Motor), Pytest, Pydantic

## Rutas de Inicio

**Primer uso:** [README.md](../README.md)

**Desarrollo:** [GUIA_COMPLETA.md](GUIA_COMPLETA.md)

---

**Última actualización:** 2 de septiembre de 2026
**Estado:** Desarrollo activo
