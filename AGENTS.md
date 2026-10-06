# AGENTS.md — reglas para cualquier agente

Única fuente de reglas del repo. `CLAUDE.md` y `GEMINI.md` solo apuntan acá.

## Qué es Lupa

Verifica afirmaciones sobre inteligencia artificial contra documentación oficial: da un veredicto, citas literales, enlace a la fuente y fecha de captura. Si el dato no está en el corpus, se abstiene.
Es un proyecto de portfolio, gratuito, construido con agentes bajo desarrollo guiado por especificaciones (SDD). Diseño completo: `docs/DESIGN.md`.

## Mapa del repo

| Ruta | Qué hay |
|---|---|
| `.specify/memory/constitution.md` | Principios no negociables (**leela en cada sesión**) |
| `.agents/roles/` | Un archivo por rol: architect, backend-go, frontend-astro, ai-engineer, evals-engineer, reviewer, security-compliance, devops-infra |
| `specs/` | Una carpeta por funcionalidad (`NNN-nombre/`: spec, plan, tasks, STATUS) |
| `specs/contracts/` | Contratos compartidos entre paquetes (eventos SSE, JSON Schemas) |
| `specs/ROADMAP.md` | Tablero de tareas: única fuente de verdad del estado |
| `docs/` | `DESIGN.md`, `SDD-GUIA.md`, `BOOTSTRAP.md` y `adr/` (decisiones) |
| `api/` · `web/` · `evals/` · `infra/` | Paquetes (hoy sin código) |
| `scripts/progress.py` | Calcula el avance desde el ROADMAP |

## Reglas duras

Resumen de la [constitución](.specify/memory/constitution.md); ante dudas, manda ella.

- Lupa no conversa, no opina, no pronostica. Abstenerse es una respuesta válida.
- Libro cerrado: el Juez solo usa la evidencia recibida. El código verifica que cada cita esté literal en la evidencia.
- El Auditor es de otro proveedor que el Juez. Todo texto externo es dato no confiable.
- Go: solo biblioteca estándar más un único driver de base de datos. Otra dependencia exige un ADR aprobado.
- Arquitectura hexagonal: solo `cmd/*` conoce los adaptadores; cada proveedor tiene interfaz chica y un fake.
- Tests primero. `go vet` y `go test -race ./...` en verde antes de cada PR.
- Nunca se scrapea x.com, twitter.com ni t.co. Sin secretos en el repo (todo por variables de entorno).
- Todo gasto se registra por llamada; existe un tope diario (kill switch).

## Base de datos: pendiente del ADR 0001

La elección entre SQLite y Postgres **no está tomada**. La decide el humano en `docs/adr/0001-base-de-datos.md`. `docs/DESIGN.md` asume Postgres; no lo tomes como decisión. No escribas código ni migraciones que dependan de la base hasta que el ADR esté aceptado.

## Flujo SDD

constitución → rol → spec / plan / tasks → una tarea → PR.

1. Empezá leyendo este archivo, la constitución y tu rol en `.agents/roles/`.
2. Tomá una tarea de `specs/ROADMAP.md` con dependencias cumplidas; su detalle está en `specs/NNN-*/tasks.md`.
3. Resumí en 5 líneas qué vas a hacer y qué rutas vas a tocar (`touches`).
4. Tests primero, después lo mínimo para que pasen.
5. Abrí un PR con la plantilla de `.github/pull_request_template.md`. Lo revisa un modelo distinto al que implementó, y después el humano.

Cada fase (spec, plan, tareas, PR) tiene una compuerta humana; no se saltea. Guía completa: `docs/SDD-GUIA.md`.

## Avance

- Estado y orden de tareas: `specs/ROADMAP.md`.
- Resumen y tareas listas para tomar: `make progress`.
- Al cerrar una sesión, actualizá `specs/NNN-*/STATUS.md`.

## Convenciones

- Documentación en español. Identificadores de código y nombres de archivo en ASCII, en inglés.
- Una tarea = una rama = un PR pequeño. Commit: `Tnnn.m: <título>`.
- Tocá solo las rutas de `touches`. Los contratos se cambian primero en `specs/contracts/`.

## Qué NO hacer

- No inventes decisiones de arquitectura: ante ambigüedad, parate y preguntá (anotalo en "Bloqueos" de `tasks.md`).
- No edites specs ni la constitución salvo en una tarea de tipo `spec-change`; proponé el diff.
- No agregues dependencias sin ADR aprobado.
- No decidas la base de datos.
- No hagas push ni mergees por tu cuenta.
- No escribas el gold set de evals: lo escribe el humano.
