# Test-Driven Development (TDD)

##  Filosofía

Los tests deben verificar el comportamiento del sistema a través de sus interfaces públicas, no su implementación interna.

Un buen test describe qué hace el sistema, no cómo lo hace.

---

##  Anti-pattern: Horizontal Slicing

Incorrecto:
- Escribir todos los tests primero
- Luego todo el código

Correcto:
- Trabajar en ciclos pequeños (vertical slicing)

---

##  Ciclo TDD

1. RED → escribir un test que falle  
2. GREEN → implementar lo mínimo para que pase  
3. REFACTOR → mejorar el código  

---

##  Workflow

- Diseñar interfaces antes de implementar
- Definir comportamientos a testear
- Escribir un test por vez
- No anticipar funcionalidades futuras

---

##  Buenas prácticas

- Tests sobre comportamiento observable
- Usar solo interfaces públicas
- Tests independientes
- Código mínimo necesario

---

##  Checklist

- [ ] El test verifica comportamiento
- [ ] Usa interfaces públicas
- [ ] Sobrevive a refactorizaciones
- [ ] No hay código innecesario