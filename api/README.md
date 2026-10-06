# api/

Servidor HTTP y worker de Lupa en Go: endpoints, SSE, cuotas, kill switch de gasto, ingesta del corpus y detección de cambios. **Sin código todavía.**

## Estructura prevista (DESIGN.md, sección 4)

```text
api/
├── cmd/api · cmd/worker      puntos de entrada y cableado
├── internal/domain           tipos puros
├── internal/llm              puertos de IA + prompts versionados + validación
├── internal/pipeline         orquestador y defensas en código
├── internal/evidence         puertos de evidencia y guard anti x.com
├── internal/httpapi          rutas, CORS y handler SSE
├── internal/stream           bus de eventos con replay
├── internal/budget           kill switch de gasto
├── internal/store            persistencia (base de datos pendiente del ADR 0001)
├── internal/providers        adaptadores (openai, google, jina...)
├── internal/fakes            implementaciones de demo y de tests
└── migrations/
```

## Reglas del paquete

- Solo biblioteca estándar más un único driver de base de datos (ADR 0001). Otra dependencia exige un ADR aprobado.
- `domain` no importa nada; `llm`, `pipeline` y `evidence` no importan SDKs ni `providers`; solo `cmd/*` importa los adaptadores.
- Cada proveedor vive detrás de una interfaz pequeña y tiene un fake en `internal/fakes`.
- Tests primero; `go vet` y `go test -race ./...` en verde antes de cada PR.

## Tareas del ROADMAP que lo implementan

- Spec 000: T000.5
- Spec 001: T001.3
- Spec 002: T002.1 a T002.8
- Spec 003: T003.1 a T003.6
- Spec 006: T006.1 a T006.4
- Spec 007: T007.1
