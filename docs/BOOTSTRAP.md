# BOOTSTRAP — Tarea T000.1 (instrucciones para cualquier agente)

**Rol:** `architect`. **Objetivo:** dejar el repositorio listo para trabajar con SDD (desarrollo guiado por especificaciones) usando cualquier agente (Claude Code, MiniMax, Antigravity u otro).

## Límites (no negociables)

- **No escribas código de aplicación** (nada de `.go`, `.ts`, `.astro`, `.py` de producto). Solo documentación, plantillas y configuración mínima.
- **No instales dependencias** ni crees `go.mod` / `package.json`.
- **No decidas la base de datos.** El ADR 0001 queda en estado *propuesta*; decide el humano (SQLite o Postgres).
- No inventes: si falta información, anotá una pregunta en tu reporte final. Idioma de la documentación: español. Identificadores de código y nombres de archivo: ASCII, en inglés.

## Precondiciones (verificá antes de empezar; si falta algo, detenete y avisá)

Deben existir: `docs/DESIGN.md`, `docs/SDD-GUIA.md`, `specs/ROADMAP.md` y `scripts/progress.py`.
Leelos en ese orden. `DESIGN.md` asume Postgres: **no lo edites**; la decisión final será el ADR 0001.

## Qué crear

### 1. Carpetas (con `.gitkeep` si quedan vacías)

```text
.specify/memory/
.agents/roles/
.github/
specs/contracts/
specs/000-fundacion/            specs/004-front-astro/
specs/001-streaming-sse/        specs/005-evals/
specs/002-corpus-e-ingesta/     specs/006-alertas/
specs/003-juez-y-auditor/       specs/007-despliegue-y-operacion/
docs/adr/
api/  web/  evals/  infra/
```

### 2. `AGENTS.md` (única fuente de reglas, máximo 120 líneas)

Contenido: qué es Lupa (3 líneas) · mapa del repo · reglas duras (resumen de la constitución, con enlace a ella) · flujo SDD (constitución → rol → spec/plan/tasks → tarea → PR) · cómo medir el avance (`specs/ROADMAP.md` y `make progress`) · convenciones (idioma, una tarea = una rama = un PR, tests primero) · qué NO hacer. Mencioná que la base de datos está **pendiente del ADR 0001**.

### 3. Punteros por herramienta

- `CLAUDE.md`: una línea que importe `@AGENTS.md` (verificá que Claude Code lo soporta; si no, "Seguí todas las instrucciones de ./AGENTS.md").
- `GEMINI.md` (Antigravity/Gemini): "Seguí todas las instrucciones de ./AGENTS.md." Si hubiera conflicto, `GEMINI.md` gana, así que **no declares reglas propias**.
- Estos archivos **no duplican reglas**. Si otra herramienta necesita su propio archivo, creá otro puntero.

### 4. Constitución

`.specify/memory/constitution.md` a partir de la sección 4 de `docs/SDD-GUIA.md`. Copiala fielmente con **un solo cambio**: el principio 7 pasa a decir *"Go: solo biblioteca estándar, más un único driver de base de datos (según el ADR 0001). Agregar otra dependencia exige un ADR aprobado."*

### 5. Roles (`.agents/roles/`)

Un archivo por rol: `architect`, `backend-go`, `frontend-astro`, `ai-engineer`, `evals-engineer`, `reviewer`, `security-compliance`, `devops-infra`. Usá la plantilla y el meta-prompt de la sección 5 de `docs/SDD-GUIA.md`. Reglas: máximo 60 líneas por archivo; rutas permitidas y prohibidas **reales** (salen de la estructura de carpetas de arriba); `reviewer` y `security-compliance` son solo lectura.

### 6. READMEs

- `README.md` (raíz): qué es Lupa, estado ("todavía no hay código: ver `specs/ROADMAP.md`"), estructura, cómo trabajar con agentes, cómo ver el avance, enlaces a `docs/`.
- `api/README.md`, `web/README.md`, `evals/README.md`, `infra/README.md`: propósito, estructura prevista (de `docs/DESIGN.md`, sección 4), reglas del paquete y qué tareas del ROADMAP lo implementan.
- `specs/README.md`: cómo leer una spec, el ciclo SDD, convención de IDs (`Tnnn.m`, `FR-`, `NFR-`, `AC-`).
- `docs/adr/README.md`, `docs/adr/0000-template.md` y `docs/adr/0001-base-de-datos.md` (estado: **propuesta**; contexto y opciones SQLite/Postgres sin decidir; "Decide: humano").

### 7. Esqueleto de specs

Para cada carpeta `specs/NNN-*`: `spec.md`, `plan.md`, `tasks.md` y `STATUS.md` con las plantillas de la sección 8 de `docs/SDD-GUIA.md`.
- `tasks.md`: precargá los IDs y títulos de esa spec desde `specs/ROADMAP.md`, sin marcar y sin detalle.
- `spec.md` y `plan.md`: encabezado + "Pendiente: generar con el prompt P1 / P3 de la guía".

### 8. Configuración mínima

- `Makefile` con solo `help` y `progress` (`python3 scripts/progress.py`). El resto lo hace T000.3.
- `.gitignore` (`.env`, `node_modules/`, `dist/`, `.astro/`, `.wrangler/`, `__pycache__/`, `*.dump`, `reference/`).
- `.env.example` con las variables del documento de diseño (sin valores reales).
- `.github/pull_request_template.md` (sección 8 de la guía).

## Verificación (obligatoria; reportá cada resultado)

1. Listá el árbol y confirmá que existe todo lo anterior.
2. `python3 scripts/progress.py` corre y muestra **44 tareas**.
3. `AGENTS.md` ≤ 120 líneas; cada rol ≤ 60 líneas.
4. No hay código de aplicación ni archivos de dependencias.
5. `CLAUDE.md` y `GEMINI.md` no duplican reglas.
6. El principio 7 de la constitución tiene el cambio pedido y `docs/DESIGN.md` quedó intacto.

## Entrega

- Rama `chore/bootstrap` y un commit: `T000.1: bootstrap del repo`. **No hagas push.**
- Marcá T000.1 como `[x]` en `specs/ROADMAP.md` **solo si** todas las verificaciones pasan.
- Imprimí: archivos creados, supuestos que hiciste y dudas que te quedaron.
