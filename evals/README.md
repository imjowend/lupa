# evals/

Gold set y arnés de evaluación de Lupa. Los evals son los tests de aceptación del producto. **Sin código todavía.**

## Estructura prevista (DESIGN.md, secciones 4 y 7)

```text
evals/
├── cases/      casos en jsonl (~120 en total), escritos por el humano
└── harness/    arnés y métricas (acuerdo, validez de citas, abstención, latencia p50/p95, costo)
```

## Reglas del paquete

- Los casos del gold set los escribe el humano; ningún agente los modifica. No se copia texto de tweets.
- El arnés corta al superar el tope de gasto (`--budget-usd`).
- El informe se publica, incluyendo dónde falla.

## Tareas del ROADMAP que lo implementan

- Spec 005: T005.1 a T005.5 (T005.2, T005.4 y T005.5 son humanas)
- Spec 002: T002.9
- Spec 006: T006.6 (humana)
