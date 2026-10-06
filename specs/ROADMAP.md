# Lupa — Hoja de ruta y tablero de avance

Es la **única fuente de verdad del estado**. Cualquier agente (Claude Code, MiniMax, Antigravity u otro) o vos podés tomar una tarea, hacerla y marcarla. Para ver el avance: `make progress`.

**Estado:** `[ ]` pendiente · `[~]` en curso · `[x]` hecha · `[!]` bloqueada
**Tam:** `S` = 1 punto (≈1 sesión de agente + tu revisión) · `M` = 2 puntos · `H` = tarea humana (no se delega; cuenta aparte)
**Perfil (orientativo, NO atado a un agente):** `R` razonamiento fuerte (specs, planes, prompts, revisión, seguridad) · `E` ejecución con spec clara (adaptadores, tests, boilerplate) · `V` visual (front: conviene verificar en un navegador) · `H` humano
**Rol:** el archivo de `.agents/roles/` que se usa para la tarea (`human` si no se delega).

> Regla: una tarea = una rama = un PR. El detalle (criterios de aceptación, `touches`, comando de verificación) vive en `specs/NNN-*/tasks.md`; esta tabla solo ordena y mide.

## Preparación de cuentas (humano, antes del Hito 1)

- [ ] **OpenAI:** key; cargar USD 10 **sin auto-recarga**; límite mensual en el panel.
- [ ] **Google:** key de Gemini en un proyecto **con facturación**; revisar el vencimiento de los créditos de AI Pro y si permiten uso comercial; alerta de presupuesto.
- [ ] **Jina:** key (10M de tokens gratis; se comparten con Reader).
- [ ] **Firecrawl:** key.
- [ ] **Cloudflare:** dominio propio, subdominio para Lupa, sitio de Turnstile (site key y secret), bucket de R2, Tunnel.
- [ ] **Oracle:** revisar *Cost Analysis* (24 GB de RAM confirmados; verificar que no haya cargos).
- [ ] **GitHub:** protección de la rama `main`, Actions habilitadas, secrets (`OPENAI_API_KEY`, `GOOGLE_API_KEY`, `JINA_API_KEY`, `FIRECRAWL_API_KEY`).
- [ ] **API de X:** **NO activar todavía.** Los USD 20 gratis vencen a los 3 meses de otorgarse.

## Spec 000 · Fundación — Hito 0

| ID | Tarea | Rol | Tam | Perfil | Depende | Estado |
|---|---|---|---|---|---|---|
| T000.1 | Bootstrap del repo: carpetas, AGENTS.md y punteros, roles, constitución, READMEs | architect | S | R | — | [x] |
| T000.2 | ADR 0001: base de datos (SQLite o Postgres). El agente redacta; **decide el humano** | architect | S | R | T000.1 | [ ] |
| T000.3 | Makefile con targets de calidad (`api-test`, `web-build`, `evals`, `up`); `help` y `progress` ya los crea T000.1 | devops-infra | S | E | T000.1 | [ ] |
| T000.4 | CI de GitHub Actions (gofmt, vet, test -race, govulncheck, build web) | devops-infra | S | E | T000.3 | [ ] |
| T000.5 | Esqueleto del API solo con biblioteca estándar (desde la spec 001 y el scaffold de referencia, si lo tenés) | backend-go | M | E | T000.2, T000.4 | [ ] |

## Spec 001 · Streaming SSE — Hito 1

| ID | Tarea | Rol | Tam | Perfil | Depende | Estado |
|---|---|---|---|---|---|---|
| T001.1 | Contrato de eventos en `specs/contracts` (stage, source, verdict, failed, done) | architect | S | R | T000.1 | [ ] |
| T001.2 | Revisar el SSE contra el contrato: latido, reanudación, CORS y cierre limpio | reviewer | S | R | T000.5, T001.1 | [ ] |
| T001.3 | Persistir eventos para reanudar tras reinicios (opcional) | backend-go | M | E | T000.2, T001.2 | [ ] |

## Spec 002 · Corpus e ingesta — Hitos 1 y 2

| ID | Tarea | Rol | Tam | Perfil | Depende | Estado |
|---|---|---|---|---|---|---|
| T002.1 | Esquema de datos del corpus (sources, documents, versions, chunks) y migración | backend-go | S | E | T000.2 | [ ] |
| T002.2 | Adaptador de embeddings (puerto `Embedder` + Jina) con lotes y reintentos | backend-go | M | E | T000.5 | [ ] |
| T002.3 | Adaptador de Qdrant: colección, upsert y búsqueda híbrida con filtros | backend-go | M | E | T002.2 | [ ] |
| T002.4 | Descubrir y descargar páginas (Firecrawl map/scrape, Jina Reader para refrescos, `GuardNotX`) | backend-go | M | E | T002.1 | [ ] |
| T002.5 | Normalizar a Markdown, hash y versionado inmutable | backend-go | M | E | T002.4 | [ ] |
| T002.6 | Chunking por encabezados y embeddings incrementales | backend-go | M | E | T002.2, T002.3, T002.5 | [ ] |
| T002.7 | Ingesta de OpenAI de punta a punta (worker) | backend-go | M | E | T002.6 | [ ] |
| T002.8 | Ingesta de Anthropic, Google y xAI | backend-go | M | E | T002.7 | [ ] |
| T002.9 | Medir recall@5 con preguntas del gold set y decidir Jina o Gemini | evals-engineer | S | R | T002.7, T005.2 | [ ] |

## Spec 003 · Juez y Auditor — Hito 2

| ID | Tarea | Rol | Tam | Perfil | Depende | Estado |
|---|---|---|---|---|---|---|
| T003.1 | Adaptador de GPT-6 Luna (`Completer`): salida estructurada y costo por tokens | ai-engineer | M | E | T000.5 | [ ] |
| T003.2 | Adaptador de Gemini (`Completer` del Auditor) y lectura de imágenes | ai-engineer | M | E | T000.5 | [ ] |
| T003.3 | Cableado real en `cmd/api`, configuración y retrieval con Qdrant | backend-go | S | E | T003.1, T003.2, T002.3 | [ ] |
| T003.4 | Caché semántica de veredictos (colección aparte en Qdrant) | backend-go | M | E | T003.3 | [ ] |
| T003.5 | Turnstile y kill switch de gasto persistente | backend-go | M | E | T000.2, T003.3 | [ ] |
| T003.6 | Adaptador de la API de X (opcional, al final) | backend-go | S | E | T003.3 | [ ] |

## Spec 004 · Front en Astro — Hito 3

| ID | Tarea | Rol | Tam | Perfil | Depende | Estado |
|---|---|---|---|---|---|---|
| T004.1 | Proyecto Astro 7: layout, estilos y configuración para Workers | frontend-astro | S | V | T000.1 | [ ] |
| T004.2 | Isla de verificación con SSE (progreso, fuentes y veredicto) | frontend-astro | M | V | T001.1, T004.1 | [ ] |
| T004.3 | Página `/v/[id]` con SSR y metaetiquetas para compartir | frontend-astro | S | V | T004.2 | [ ] |
| T004.4 | Modo demo con 20–30 ejemplos precalculados | frontend-astro | S | V | T003.3 | [ ] |
| T004.5 | Despliegue con Workers Builds | devops-infra | S | E | T004.2 | [ ] |

## Spec 005 · Evals — Hitos 2 a 4

| ID | Tarea | Rol | Tam | Perfil | Depende | Estado |
|---|---|---|---|---|---|---|
| T005.1 | Arnés de evals con tope de gasto y CI de humo | evals-engineer | S | E | T000.4 | [ ] |
| T005.2 | Gold set v1 (60 casos escritos por vos) | human | H | H | T000.1 | [ ] |
| T005.3 | Informe de evals: acierto por tipo, costo y latencia p50/p95 | evals-engineer | S | E | T005.1, T003.3 | [ ] |
| T005.4 | Gold set v2 (120 casos) | human | H | H | T005.2 | [ ] |
| T005.5 | Benchmark manual contra Grok y primer artículo | human | H | H | T005.3 | [ ] |

## Spec 006 · Alertas de cambios — Hito 5

| ID | Tarea | Rol | Tam | Perfil | Depende | Estado |
|---|---|---|---|---|---|---|
| T006.1 | Esquema de `change_events`, `subscriptions` y `notifications` | backend-go | S | E | T002.5 | [ ] |
| T006.2 | Diff por secciones y umbral de materialidad | backend-go | M | E | T006.1 | [ ] |
| T006.3 | Extractor estructurado de precios y límites | ai-engineer | M | R | T002.8 | [ ] |
| T006.4 | Clasificador de cambios y chequeo de números | ai-engineer | M | R | T006.2, T006.3, T003.1 | [ ] |
| T006.5 | Changelog público y RSS | frontend-astro | S | V | T006.4 | [ ] |
| T006.6 | Evals de alertas (≈40 casos escritos por vos) | human | H | H | T006.4 | [ ] |

## Spec 007 · Despliegue y operación — Hito 3

| ID | Tarea | Rol | Tam | Perfil | Depende | Estado |
|---|---|---|---|---|---|---|
| T007.1 | Dockerfile ARM64 y docker-compose | devops-infra | S | E | T000.5 | [ ] |
| T007.2 | Cloudflare Tunnel y DNS | devops-infra | S | E | T007.1 | [ ] |
| T007.3 | Backups y prueba de restauración | devops-infra | M | E | T007.1, T000.2 | [ ] |
| T007.4 | Revisión de seguridad: reglas de X, prompt injection, secretos y dependencias | security-compliance | S | R | T003.3 | [ ] |
| T007.5 | Runbook y README final | architect | S | E | T007.4 | [ ] |

## Cómo elegir el agente para una tarea (orientativo)

Las tareas **no dependen** del agente: cualquiera puede tomarlas porque todo el contexto está en archivos (`AGENTS.md`, el rol, la constitución, la spec y la tarea). Esta guía solo ayuda a repartir esfuerzo:

| Perfil | Qué conviene | Por qué |
|---|---|---|
| **R** razonamiento | El modelo más fuerte que tengas | Un error acá se propaga a todo lo demás |
| **E** ejecución | Un modelo más barato, con la spec clara | La tarea ya está acotada y los tests la verifican |
| **V** visual | Una herramienta que te deje ver el resultado en un navegador | Hay que mirar la pantalla, no solo los tests |
| **H** humano | Vos | Es criterio y contenido propio |

**Siempre:** implementa un modelo y **revisa otro distinto** (principio IA-a-IA).
