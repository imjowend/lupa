# Lupa

Lupa verifica afirmaciones sobre inteligencia artificial (un precio, un límite, una fecha, una capacidad) contra documentación oficial. Responde con un veredicto, citas literales, el enlace a la fuente y la fecha de captura; si el dato no está en las fuentes, se abstiene y lo dice. Es un proyecto de portfolio, gratuito, construido con agentes de código bajo desarrollo guiado por especificaciones (SDD).

## Estado

**Todavía no hay código:** ver [`specs/ROADMAP.md`](specs/ROADMAP.md). Hoy el repo contiene la documentación, las reglas para agentes y el esqueleto de las specs. La base de datos (SQLite o Postgres) está pendiente del [ADR 0001](docs/adr/0001-base-de-datos.md).

## Estructura

| Ruta | Contenido |
|---|---|
| `AGENTS.md` | Reglas para cualquier agente (`CLAUDE.md` y `GEMINI.md` apuntan acá) |
| `.specify/memory/constitution.md` | Principios no negociables |
| `.agents/roles/` | Un perfil por rol de agente |
| `specs/` | Una carpeta por funcionalidad, `contracts/` y el `ROADMAP.md` |
| `docs/` | Diseño, guía de SDD, bootstrap y `adr/` |
| `api/` · `web/` · `evals/` · `infra/` | Paquetes (por implementar) |
| `scripts/` | `progress.py` |

## Cómo trabajar con agentes

1. Elegí una tarea lista en `specs/ROADMAP.md` (dependencias cumplidas).
2. Pegá al agente el prompt de arranque de [`docs/SDD-GUIA.md`](docs/SDD-GUIA.md) (sección 5): lee `AGENTS.md`, la constitución y su rol, y resume qué va a hacer antes de empezar.
3. Una tarea = una rama = un PR. Implementa un modelo y revisa otro distinto; el humano aprueba cada compuerta.

## Ver el avance

```bash
make progress
```

## Documentación

- [`docs/DESIGN.md`](docs/DESIGN.md): documento de diseño y plan.
- [`docs/SDD-GUIA.md`](docs/SDD-GUIA.md): guía de SDD, roles y prompts.
- [`docs/BOOTSTRAP.md`](docs/BOOTSTRAP.md): tarea T000.1.
- [`docs/adr/`](docs/adr/README.md): decisiones de arquitectura.
