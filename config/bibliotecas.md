# Bibliotecas Base para la Estructura del Proyecto

## Objetivo

Este documento define la base de bibliotecas recomendada para sostener una arquitectura Python sólida, escalable y mantenible, alineada con Clean Code, TDD y la estructura de tres capas del proyecto.

La selección prioriza:

- Tipado explícito y validación estricta.
- Bajo acoplamiento entre capas.
- Configuración centralizada y reproducible.
- Testing rápido y confiable.
- Observabilidad útil sin introducir complejidad innecesaria.

> Nota de alcance: se excluye el procesamiento de PDFs por ahora, para mantener el foco en el núcleo arquitectónico.

## Selección recomendada

La base recomendada para este proyecto queda así:

- **FastAPI** como framework web principal.
- **Pydantic Settings** para leer y validar configuración desde `.env` y variables de entorno.
- **Pydantic v2** para validar datos de entrada, salida y contratos intermedios.
- **Loguru** para logging profesional con una configuración simple y mantenible.
- **Pytest** como framework de pruebas para sostener TDD.
- **`Depends` de FastAPI** para inyección de dependencias interna, sin sumar una librería extra.

En términos prácticos, esto significa lo siguiente:

- **FastAPI** maneja la capa HTTP.
- **Pydantic Settings** maneja la configuración del entorno.
- **Pydantic v2** asegura que los datos tengan forma y tipo correctos.
- **Loguru** registra eventos, errores y trazas útiles.
- **Pytest** valida que cada capa se comporte como se espera.
- **Depends** conecta controladores, servicios y configuraciones de forma simple.

Esta selección es deliberadamente compacta: cubre lo esencial sin introducir dependencias que todavía no aportan valor real al alcance actual.

## 1. Framework Web: FastAPI

FastAPI debe ser el framework base del proyecto.

### Por qué es la mejor elección

- Está diseñado para trabajar de forma nativa con type hints, lo que mejora la legibilidad, reduce errores y fortalece el contrato entre capas.
- Integra Pydantic de manera directa, por lo que la validación de entrada y salida no requiere capas de traducción innecesarias.
- Genera OpenAPI y documentación interactiva automáticamente, lo que reduce mantenimiento manual.
- Permite endpoints síncronos o asíncronos sin cambiar la arquitectura general.
- Facilita la composición de controladores delgados, una regla clave de Clean Code.

### Por qué es superior para tipado estático

FastAPI aprovecha las anotaciones de tipo de Python como parte de su contrato funcional. Esto ofrece ventajas concretas frente a frameworks más dinámicos:

- Los parámetros de endpoints, dependencias y respuestas quedan explícitos en la firma de la función.
- Las herramientas de análisis estático como mypy, Pyright o el propio editor pueden detectar inconsistencias antes de ejecutar el código.
- La documentación generada y el código real no divergen, porque ambas cosas nacen de la misma definición tipada.
- Los modelos Pydantic sirven como frontera de entrada y salida, lo que evita que la lógica de negocio dependa de estructuras ambiguas.

### Encaje con Clean Code

- Controladores pequeños y predecibles.
- Separación clara entre transporte HTTP y lógica de negocio.
- Menor duplicación de validaciones.
- Mejor mantenibilidad cuando el proyecto crece por módulos funcionales.

## 2. Configuración y Entorno: Pydantic Settings

Pydantic Settings debe ser la solución base para cargar y validar configuración desde archivos `.env`, variables de entorno y valores por defecto.

### Justificación técnica

- Permite definir configuración como una clase tipada y versionable.
- Convierte la configuración en un contrato explícito, en lugar de dispersarla por el código.
- Valida tipos al arrancar la aplicación, detectando fallos de entorno de forma temprana.
- Reduce el riesgo de errores silenciosos por variables faltantes o mal tipeadas.

### Valor para mantenibilidad

- Un único punto de verdad para la configuración.
- Menos lógica condicional en módulos de arranque.
- Configuración más fácil de testear con fixtures y monkeypatch.

### Relación con el proyecto actual

El repositorio ya sigue este enfoque en `app/core/config.py`, donde la configuración central se modela con `BaseSettings`. Eso es coherente con una arquitectura limpia y debe conservarse como estándar.

## 3. Validación de Datos: Pydantic v2

Pydantic v2 debe ser la librería estándar para modelos de entrada, salida y validación intermedia.

### Por qué usar Pydantic v2

- Mejora rendimiento respecto de la generación anterior.
- Formaliza contratos de datos con modelos declarativos y expresivos.
- Facilita separar schemas de API, entidades de dominio y objetos de servicio.
- Se integra de forma natural con FastAPI y con settings de configuración.

### Beneficios bajo Clean Code

- Menos validación manual repetitiva.
- Mensajes de error consistentes y comprensibles.
- Menor riesgo de mutación accidental de objetos de entrada.
- Mejor aislamiento entre capa HTTP y lógica interna.

### Uso recomendado

- Modelos para requests y responses en la capa de schemas.
- Modelos de settings para configuración.
- Validación de invariantes simples en el borde del sistema, no dentro del core de negocio salvo necesidad real.

## 4. Logging Profesional: Loguru

Loguru es la opción recomendada para logging de aplicación en esta base.

### Por qué Loguru

- Reduce boilerplate frente al módulo `logging` estándar.
- Ofrece salida legible, niveles claros y configuración rápida.
- Soporta sinks múltiples, rotación, retención y formatos estructurados.
- Hace más simple instrumentar desarrollo, depuración y producción sin introducir demasiada complejidad.

### Encaje con Clean Code

- El logging debe ser transversal, no invasivo.
- Debe aportar trazabilidad sin ensuciar la lógica de negocio.
- Loguru permite centralizar configuración y mantener llamadas consistentes.

### Recomendación de uso

- Usar un módulo de logging centralizado en `app/core`.
- Evitar `print()` en toda la base de código.
- Registrar eventos de negocio relevantes, errores y puntos de entrada/salida de procesos.
- Si más adelante se necesita integración estricta con ecosistemas que dependen del logging estándar, Loguru puede convivir con él mediante un puente.

## 5. Testing y TDD: Pytest

Pytest debe ser la base del ciclo TDD del proyecto.

### Razones de selección

- Sintaxis simple y legible, ideal para pruebas orientadas al comportamiento.
- Excelente soporte para fixtures, parametrización y marcadores.
- Muy adecuado para pruebas unitarias, de integración y contract tests ligeros.
- Tiene un ecosistema amplio de plugins que cubre la mayoría de las necesidades sin fricción.

### Plugins mínimos recomendados

- `pytest-cov`: cobertura de pruebas.
- `pytest-asyncio` o soporte equivalente vía `anyio`: pruebas de código asíncrono.
- `httpx`: cliente para probar endpoints HTTP de FastAPI sin depender de herramientas externas.
- `pytest-mock`: mocking limpio y controlado cuando sea necesario aislar servicios.

### Por qué esto favorece TDD

- Permite escribir tests pequeños, rápidos y repetibles antes de implementar el código.
- Facilita la refactorización segura.
- Hace visible el contrato funcional de cada capa.
- Reduce la tentación de acoplar tests a detalles internos en lugar de comportamiento observable.

### Convención recomendada

- Tests unitarios para modelos y servicios.
- Tests de integración para rutas y composición con FastAPI.
- Uso de fixtures para construir estados reutilizables.
- Marcadores para separar `unit`, `integration` y `slow`.

## 6. Inyección de Dependencias

Para este proyecto no es necesario introducir una librería externa de inyección de dependencias.

### Decisión

Se recomienda usar la inyección nativa de FastAPI mediante `Depends`.

### Motivo

- Cubre el caso de uso actual con menor complejidad.
- Mantiene el grafo de dependencias visible en los endpoints.
- Evita capas extra de abstracción que suelen dificultar el debugging y el onboarding.
- Está alineada con YAGNI: no sumar infraestructura que todavía no aporta valor claro.

### Cuándo evaluar una librería externa

Recién tendría sentido considerar algo como `dependency-injector` si el proyecto empieza a requerir:

- Múltiples implementaciones intercambiables de servicios.
- Ciclos de vida complejos de recursos.
- Composición avanzada de módulos con muchas dependencias cruzadas.
- Necesidad de un contenedor explícito para aplicaciones grandes o multi-tenant.

Mientras eso no ocurra, `Depends` es la mejor decisión de arquitectura.

## 7. Selección final propuesta

### Base obligatoria

- FastAPI
- Pydantic v2
- Pydantic Settings
- Pytest
- httpx para pruebas de API
- pytest-cov
- pytest-asyncio o soporte equivalente de async testing

### Recomendadas

- Loguru
- pytest-mock

### No introducir por ahora

- Contenedor externo de inyección de dependencias
- Capas adicionales de abstracción que no resuelvan un problema real
- Dependencias enfocadas a PDFs o extracción documental hasta que exista ese requisito

## Conclusión

La combinación de FastAPI, Pydantic v2, Pydantic Settings, Pytest y Loguru ofrece una base moderna, tipada y mantenible para el proyecto.

Esta selección respeta Clean Code porque reduce acoplamiento, centraliza responsabilidades y mantiene la intención del código visible. También respeta TDD porque favorece pruebas rápidas, contratos claros y refactorización segura.

La decisión sobre inyección de dependencias debe mantenerse simple en esta etapa: usar `Depends` de FastAPI es suficiente, más legible y más sostenible para el alcance actual.