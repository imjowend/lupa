# Lupa — Guía de SDD (Spec-Driven Development) para el monorepo

> Para trabajar con agentes de código (MiniMax, Antigravity u otros) sin perder el control del proyecto.
> No necesitás instalar nada: son archivos Markdown y prompts para copiar y pegar.

## 0. Cómo usar esta guía

1. Leé la sección 1 una vez: es el "por qué" y el vocabulario.
2. Creá la estructura de la sección 3 y la constitución de la sección 4.
3. Generá los roles con el meta-prompt de la sección 5.
4. Para cada funcionalidad, recorré los prompts de la sección 6 en orden.
5. Usá la sección 9 como protocolo para dejar a los agentes trabajando "en segundo plano".

---

## 1. Qué es SDD

### La idea en una línea

En SDD **la especificación es el producto y el código es su consecuencia**. Primero escribís *qué* se construye, *por qué* y *cómo se sabe que está bien*; recién después un agente escribe el *cómo*.

### Vibe coding vs SDD

| | Vibe coding | SDD |
|---|---|---|
| Punto de partida | Un prompt suelto | Una especificación revisada |
| Quién decide la arquitectura | El agente, sobre la marcha | Vos, en el plan, antes de codificar |
| "¿Está terminado?" | Se ve bien | Se cumplen criterios de aceptación medibles |
| Cambiar de agente o de modelo | Se pierde el contexto | Los archivos son el contexto |
| Riesgo típico | Código que funciona hoy y nadie entiende | Papeleo si te pasás de detalle |

El problema que resuelve: un agente que codifica sin spec **rellena los huecos con suposiciones** y cada sesión nueva suposiciones distintas. La spec fija esas decisiones una sola vez.

### Las fases

| Fase | Pregunta que responde | Artefacto | Checkpoint humano |
|---|---|---|---|
| **Constitución** (una vez) | ¿Qué reglas no se negocian? | `.specify/memory/constitution.md` | Aprobás |
| **Especificar** | ¿Qué se construye y por qué? (sin tecnología) | `specs/NNN-x/spec.md` | Aprobás |
| **Clarificar** | ¿Qué está ambiguo? | Preguntas y respuestas dentro de la spec | Respondés |
| **Planificar** | ¿Cómo se construye? | `plan.md` (+ `contracts/`, ADRs) | Aprobás |
| **Tareas** | ¿En qué pasos chicos y verificables? | `tasks.md` | Aprobás |
| **Analizar** | ¿Spec, plan y tareas son coherentes? | Reporte GO / NO-GO | Decidís |
| **Implementar** | Una tarea por vez | Código + tests (una rama por tarea) | Revisás cada PR |
| **Converger** | ¿El código y la spec siguen alineados? | Diff propuesto a la spec | Aprobás |

La regla de oro: **cada fase tiene un humano que aprueba antes de pasar a la siguiente**.

### Herramientas que existen (para que sepas qué es qué)

- **GitHub Spec Kit** (open source): una CLI (`specify`) que deja plantillas y comandos en tu repo. Según su README, el ciclo es *constitución una vez por proyecto; y por funcionalidad: specify → plan → tasks → implement → converge*, con `clarify` y `analyze` como compuertas. Guarda la constitución en `.specify/memory/constitution.md` y cada funcionalidad en `specs/<feature>/` (`spec.md`, `plan.md`, `tasks.md`, `contracts/`…). Funciona con varios agentes (Copilot, Claude Code, Cursor, Gemini CLI y otros).
- **Kiro** (AWS): un IDE que genera `requirements.md` (con notación EARS), `design.md` y `tasks.md`.
- **Esta guía** usa la misma estructura de carpetas que Spec Kit, así que si más adelante lo instalás no hay conflicto. Pero **no lo necesitás**: los prompts de la sección 6 hacen lo mismo en cualquier herramienta.

### Cuándo NO usar SDD completo

- Cambios de menos de ~20 líneas, renombres, typos: carril rápido (prompt directo + tests).
- Experimentos descartables (un spike de una hora): sin spec, pero **no se mergean**.
- Todo lo que toque comportamiento, contratos, costos o seguridad: SDD completo.

### Críticas honestas (y cómo se mitigan)

| Crítica | Mitigación |
|---|---|
| "Mar de Markdown": demasiados documentos | Specs de 1–2 páginas; una por funcionalidad |
| La spec se pudre | Fase **Converger** después de cada merge |
| La spec describe el *cómo* y se vuelve un plan disfrazado | Spec = qué/por qué; plan = cómo (ver sección 11) |
| El agente igual se desvía | Tareas con `touches` (rutas permitidas) + revisión por otro modelo |

### Requisitos en EARS (formato corto y verificable)

EARS son 5 plantillas de una oración. Hacen que un requisito sea testeable.

| Tipo | Plantilla | Ejemplo de Lupa |
|---|---|---|
| Ubicuo | El sistema deberá `<comportamiento>` | El sistema deberá registrar el costo de cada llamada a un modelo. |
| Evento | Cuando `<evento>`, el sistema deberá `<respuesta>` | Cuando el cliente se reconecte con `Last-Event-ID = n`, el sistema deberá reenviar solo los eventos con id > n. |
| Estado | Mientras `<estado>`, el sistema deberá `<comportamiento>` | Mientras el stream esté abierto, el sistema deberá enviar un latido cada 15 s. |
| No deseado | Si `<condición>`, entonces el sistema deberá `<respuesta>` | Si una cita no aparece literal en la evidencia, entonces el sistema deberá descartarla. |
| Opcional | Donde `<característica>`, el sistema deberá `<comportamiento>` | Donde la lectura de tweets esté habilitada, el sistema deberá usar solo la API oficial. |

---

## 2. SDD en un monorepo

Un monorepo tiene varios paquetes (`api`, `web`, `evals`, `infra`) que se afectan entre sí. Por eso las specs se organizan en **tres niveles**:

1. **Constitución (global):** reglas que valen para todos los paquetes.
2. **Spec de funcionalidad (`specs/NNN-nombre/`):** una carpeta por funcionalidad, aunque cruce paquetes. El `plan.md` dice qué paquetes toca.
3. **Contratos (`specs/contracts/`):** lo que comparten los paquetes (eventos SSE, JSON Schemas, formas de request/response). Es la única fuente de verdad de la frontera `api` ↔ `web`.

### Reglas propias del monorepo

- **Contrato primero.** Si una funcionalidad cambia la frontera entre paquetes, el orden de los PRs es: (1) contrato, (2) `api`, (3) `web`.
- **Propiedad por rutas.** Cada tarea declara `touches:` con las rutas que el agente puede modificar. Todo lo demás es solo lectura.
- **Paralelismo seguro.** Dos tareas pueden correr a la vez solo si sus `touches` no se pisan y viven en ramas distintas.
- **Una rama = una tarea = un PR.**

### Mapa de funcionalidades de Lupa

| Spec | Qué cubre | Paquetes |
|---|---|---|
| `000-fundacion` | Constitución, roles, CI, HTTP solo con la biblioteca estándar | api, infra |
| `001-streaming-sse` | POST + SSE con reanudación | api, web, contracts |
| `002-corpus-e-ingesta` | Descubrir → descargar → versionar → chunks → embeddings → Qdrant | api |
| `003-juez-y-auditor` | Adaptadores de Luna y Gemini, prompts, defensas | api |
| `004-front-astro` | Isla de verificación, páginas, `/v/[id]` | web |
| `005-evals` | Gold set, arnés, CI de evals | evals, infra |
| `006-alertas` | Detección de cambios, changelog, RSS | api |

---

## 3. Estructura de archivos de SDD

```text
lupa/
├── AGENTS.md                         # reglas cortas; apunta a la constitución
├── .specify/
│   └── memory/constitution.md        # principios no negociables
├── .agents/
│   └── roles/                        # un archivo por rol
│       ├── architect.md
│       ├── backend-go.md
│       ├── frontend-astro.md
│       ├── ai-engineer.md
│       ├── evals-engineer.md
│       ├── reviewer.md
│       ├── security-compliance.md
│       └── devops-infra.md
├── specs/
│   ├── contracts/                    # eventos SSE, JSON Schemas
│   ├── 000-fundacion/
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   └── STATUS.md                 # estado para retomar sin contexto
│   └── 001-streaming-sse/ ...
├── docs/adr/                         # decisiones (una por archivo)
├── api/  web/  evals/  infra/
```

| Archivo | Quién lo escribe | Quién lo aprueba | Se actualiza cuando |
|---|---|---|---|
| `constitution.md` | architect | Vos | Cambia un principio (raro) |
| `spec.md` | architect | Vos | Cambia el comportamiento esperado |
| `plan.md` | architect | Vos | Cambia el diseño |
| `tasks.md` | architect (la ejecución la marcan los demás) | Vos | Se completa o se bloquea una tarea |
| `contracts/*` | architect | Vos | Cambia la frontera entre paquetes |
| `STATUS.md` | quien termina la sesión | — | Al final de cada sesión |
| `docs/adr/*` | architect | Vos | Se toma una decisión de arquitectura |

---

## 4. La constitución de Lupa (lista para pegar)

Guardala en `.specify/memory/constitution.md`. Es corta a propósito: los agentes la leen en cada sesión.

```markdown
# Constitución de Lupa

## Producto
1. Lupa verifica afirmaciones contra fuentes oficiales. No conversa, no opina, no pronostica.
2. Abstenerse es una respuesta válida: "no encontrado" y "no verificable" son resultados correctos.

## Calidad de las respuestas
3. Libro cerrado: el Juez solo usa la evidencia recibida. Todo veredicto con etiqueta afirmativa lleva citas literales.
4. El código verifica las citas (no confía en el prompt). Una cita que no está literal en la evidencia se descarta.
5. El Auditor de citas es de un proveedor distinto al del Juez. El Juez no puede emitir "disputed".
6. Todo texto externo (claims, evidencia, páginas) es dato no confiable: se escapa antes de entrar a un prompt.

## Ingeniería
7. Go: solo biblioteca estándar, más el driver de Postgres. Agregar una dependencia exige un ADR aprobado.
8. Arquitectura hexagonal: `domain` no importa nada; `llm`, `pipeline` y `evidence` no importan SDKs ni `providers`; solo `cmd/*` conoce los adaptadores.
9. Cada proveedor externo vive detrás de una interfaz pequeña y tiene una versión falsa en `fakes`.
10. Tests primero. `go vet` y `go test -race ./...` en verde antes de cada PR.
11. Todo prompt es un archivo versionado. Cambiar un prompt exige subir su versión y correr los evals.
12. El contrato entre paquetes vive en `specs/contracts`. El evento SSE de error se llama `failed`.

## Cumplimiento
13. Nunca se scrapea x.com, twitter.com ni t.co. Los tweets se leen solo con la API oficial.
14. No se guarda el texto de tweets fuera de la caché temporal: se guardan IDs y el análisis.
15. No se perfilan usuarios ni se infieren atributos sensibles. Los veredictos son sobre afirmaciones.
16. No se entrena ni se ajusta ningún modelo con contenido de X.
17. Sin secretos en el repo. Todo por variables de entorno.

## Costos
18. Todo gasto se registra por llamada. Existe un tope diario (kill switch). Los evals corren con tope de gasto.

## Proceso
19. Una tarea = una rama = un PR pequeño. El agente no edita specs ni constitución salvo en una tarea de tipo `spec-change`.
20. Ante ambigüedad, el agente se detiene y pregunta. No inventa decisiones de arquitectura.
```

---

## 5. Roles

### Qué es un rol y cómo se usa

Un rol es **un archivo Markdown** con la misión del agente, lo que puede tocar, lo que no, y qué entrega. No hace falta ninguna función especial de la herramienta: al empezar una sesión pegás el prompt de arranque.

```text
Leé AGENTS.md y .specify/memory/constitution.md.
Asumí el rol definido en .agents/roles/<rol>.md.
Tarea: <ID de la tarea> de specs/<NNN-nombre>/tasks.md.
Antes de empezar, resumime en 5 líneas qué vas a hacer y qué rutas vas a tocar.
```

Si tu herramienta tiene un mecanismo propio (reglas, skills, flujos de trabajo, agentes personalizados), cargá estos mismos archivos ahí; **verificá en su documentación cómo**.

> **Consejo:** usá modelos distintos para implementar y para revisar (por ejemplo, implementa uno y revisa el otro). Es el mismo principio IA-a-IA del Juez y el Auditor: los errores de dos modelos están menos correlacionados.

### Los 8 roles

| Rol | Misión | Puede tocar | No puede tocar | Entrega |
|---|---|---|---|---|
| **architect** | Escribir specs, planes, contratos, tareas y ADRs | `specs/`, `docs/adr/` | Código de producción | Documentos para aprobar |
| **backend-go** | Implementar tareas de la API | `api/` | `web/`, `specs/` | Código + tests |
| **frontend-astro** | Implementar la isla y las páginas | `web/` | `api/`, `specs/` | Código + tests |
| **ai-engineer** | Prompts, esquemas, pipeline, defensas | `api/internal/llm`, `api/internal/pipeline` | El gold set | Código + versión de prompt + resultado de evals |
| **evals-engineer** | Arnés, métricas y CI de evals | `evals/harness`, CI | Los casos del gold set (los escribe el humano) | Arnés + reportes |
| **reviewer** | Auditar un diff contra la spec | Nada (solo lectura) | Todo | Reporte PASS/FAIL por criterio |
| **security-compliance** | Revisar reglas de X, prompt injection, secretos, dependencias | Nada (solo lectura) | Todo | Checklist firmado |
| **devops-infra** | Docker, Tunnel, backups, CI | `infra/`, `docker-compose.yml`, `Dockerfile`, `.github/` | Código de aplicación | Infra + runbook |

### Plantilla de un archivo de rol

```markdown
# Rol: <nombre>

## Misión
<una oración>

## Leé siempre
- AGENTS.md, .specify/memory/constitution.md
- La spec, el plan y la tarea indicados

## Podés tocar
- <rutas>

## No podés tocar
- <rutas y cosas prohibidas>

## Cómo trabajás
1. Tests primero.
2. Lo mínimo para cumplir los criterios de aceptación.
3. <reglas propias del rol>

## Te detenés y preguntás cuando
- La spec es ambigua o contradictoria.
- Necesitás una dependencia nueva o tocar una ruta fuera de `touches`.
- Un criterio de aceptación falla dos veces seguidas.

## Entregás
- <formato de salida>
```

### Ejemplo completo: `backend-go.md`

```markdown
# Rol: backend-go

## Misión
Implementar tareas de la API en Go con la biblioteca estándar, respetando la arquitectura hexagonal.

## Leé siempre
- AGENTS.md, .specify/memory/constitution.md
- specs/<NNN>/spec.md, plan.md y la tarea indicada en tasks.md
- specs/contracts/ si la tarea toca la frontera con web

## Podés tocar
- Solo las rutas listadas en `touches` de la tarea (dentro de api/).

## No podés tocar
- web/, specs/, .specify/, docs/adr/ ni archivos fuera de `touches`.
- go.mod: no agregues dependencias.

## Cómo trabajás
1. Escribí primero el test que falla y mostrámelo.
2. Implementá lo mínimo para que pase.
3. `domain` no importa nada; `llm`, `pipeline` y `evidence` no importan SDKs ni `providers`.
4. Errores con `%w`; contexto (`context.Context`) en toda llamada externa; sin variables globales mutables.
5. Antes de entregar: `gofmt -l .`, `go vet ./...`, `go test -race ./...`.

## Te detenés y preguntás cuando
- La spec es ambigua, o el contrato no alcanza.
- Hace falta una dependencia nueva.
- Un criterio falla dos veces.

## Entregás
- Resumen de cambios (qué y por qué), salida de los comandos, criterios cumplidos y no cumplidos, y supuestos que hiciste.
```

### Meta-prompt: que el agente genere los demás roles

```text
Rol: architect. Leé AGENTS.md, .specify/memory/constitution.md y el árbol del repo.
Creá en .agents/roles/ un archivo por cada uno de estos roles: architect, backend-go,
frontend-astro, ai-engineer, evals-engineer, reviewer, security-compliance, devops-infra.

Usá exactamente la plantilla de rol (Misión, Leé siempre, Podés tocar, No podés tocar,
Cómo trabajás, Te detenés y preguntás cuando, Entregás). Reglas:
- Máximo 60 líneas por archivo. Sin relleno.
- Las rutas permitidas y prohibidas deben salir de la estructura real del repo.
- Cada regla debe poder verificarse (un comando, un archivo o un criterio observable).
- Los roles reviewer y security-compliance son solo lectura y entregan un reporte, no código.
- No inventes herramientas ni comandos que no existan en el repo (Makefile, package.json).
Cuando termines, listame qué asumiste y qué dudas te quedaron.
```

---

## 6. Prompts del ciclo (copiar y pegar)

Reemplazá lo que está entre `<...>`. Todos asumen que pegás antes el prompt de arranque de la sección 5.

### P0 · Constitución (una vez)

```text
Rol: architect. Leé AGENTS.md y docs/ (el documento de diseño).
Creá .specify/memory/constitution.md con los principios no negociables del proyecto.
Base: <pegá la constitución de la sección 4>.
Reglas: máximo 1 página; cada principio verificable; sin detalles de implementación que
cambien seguido. Marcá con [CONFIRMAR] lo que no puedas deducir de los documentos.
```

### P1 · Especificar

```text
Rol: architect. Leé la constitución y specs/contracts/.
Creá specs/<NNN-nombre>/spec.md para esta funcionalidad:
<descripción en 3–5 oraciones: QUÉ se quiere y POR QUÉ, sin tecnología>.

Estructura obligatoria:
1. Historias de usuario priorizadas (P1, P2, P3), cada una testeable por sí sola.
2. Requisitos funcionales FR-001… en formato EARS.
3. Requisitos no funcionales NFR-001… (costo, latencia, seguridad) con números.
4. Casos límite y errores.
5. Criterios de aceptación AC-001…, cada uno verificable con un test o un eval.
6. Fuera de alcance.
7. Preguntas abiertas, marcadas [NECESITA ACLARACIÓN].

Reglas: nada de librerías, archivos ni funciones (eso va en el plan). No inventes
requisitos: si falta información, hacé una pregunta. Máximo 2 páginas.
```

### P2 · Clarificar

```text
Rol: architect. Leé specs/<NNN>/spec.md.
Buscá ambigüedades, requisitos que se contradicen y criterios no verificables.
Hacéme hasta 5 preguntas, UNA por vez, cada una con 2–3 opciones y tu recomendación.
Cuando yo responda, actualizá spec.md y quitá la marca [NECESITA ACLARACIÓN] correspondiente.
```

### P3 · Planificar

```text
Rol: architect. Leé la constitución, specs/<NNN>/spec.md, specs/contracts/ y el
documento de diseño. Creá specs/<NNN>/plan.md con:
1. Paquetes y archivos afectados.
2. Cambios de contrato (si hay, creá o actualizá specs/contracts/).
3. Decisiones de diseño con alternativas descartadas. Si propone una dependencia nueva,
   escribí un ADR en docs/adr/ y marcá el plan como BLOQUEADO hasta que yo apruebe.
4. Modelo de datos y migraciones.
5. Riesgos (costos, seguridad, concurrencia).
6. Estrategia de pruebas: tabla AC-xxx → test unitario / de integración / eval.
No escribas código de producción.
```

### P4 · Tareas

```text
Rol: architect. Leé spec.md y plan.md de specs/<NNN>/. Creá tasks.md con tareas atómicas.
Cada tarea:
- ID (T01…), título y objetivo en una oración.
- Rol responsable.
- touches: rutas que se pueden modificar.
- Depende de: IDs.
- Criterios de aceptación: AC-xxx que cubre.
- Cómo verificar: el comando exacto (por ejemplo `make api-test`).
- Definición de listo.
Reglas: una tarea cabe en un PR (≈200 líneas netas o menos); ordenadas por dependencia;
marcá con [P] las que se pueden hacer en paralelo (touches disjuntos); la primera tarea
debe ser el contrato si hay cambios de frontera.
```

### P5 · Analizar (compuerta antes de implementar)

```text
Rol: reviewer. No modifiques ningún archivo.
Cruzá .specify/memory/constitution.md, specs/<NNN>/spec.md, plan.md y tasks.md.
Reportá en una tabla:
- Requisitos (FR/NFR/AC) sin tarea.
- Tareas sin requisito.
- Contradicciones entre documentos.
- Tareas cuyos touches se pisan pero están marcadas [P].
- Violaciones de la constitución.
Terminá con un veredicto: GO o NO-GO, y la lista priorizada de lo que hay que arreglar.
```

### P6 · Implementar UNA tarea

```text
Rol: <backend-go | frontend-astro | ai-engineer | devops-infra>.
Implementá SOLO la tarea <Tnn> de specs/<NNN>/tasks.md.

Proceso:
1. Resumime en 5 líneas qué vas a hacer y qué rutas vas a tocar. Esperá mi OK.
2. Escribí los tests primero y mostrame que fallan.
3. Implementá lo mínimo para que pasen.
4. Ejecutá <comandos de la tarea>. Pegame la salida.
5. No toques rutas fuera de `touches`. No agregues dependencias. No edites specs.
6. Si algo es ambiguo o la spec está mal, PARATE: escribí la duda en tasks.md bajo
   "Bloqueos" y avisame. No decidas solo.

Entregá: resumen de cambios, salida de los comandos, criterios cumplidos y no cumplidos,
y los supuestos que hiciste.
```

### P7 · Revisar (con un modelo distinto al que implementó)

```text
Rol: reviewer. No edites código.
Compará el diff de la rama <rama> con spec.md, plan.md y la tarea <Tnn>.
Por cada criterio AC-xxx de la tarea: PASS o FAIL, con evidencia (archivo:línea o nombre del test).
Buscá además:
- Cambios fuera de `touches` o dependencias nuevas.
- Violaciones de la constitución (especialmente los principios 3–6, 13–16).
- Tests débiles: que pasarían igual con una implementación incorrecta.
- Manejo de errores, cancelación de contexto, concurrencia y fugas de goroutines.
- Secretos, logs con datos sensibles.
Veredicto: APROBAR o PEDIR CAMBIOS, con la lista priorizada.
```

### P8 · Converger (después de cada merge)

```text
Rol: architect. Comparé el código mergeado de <Tnn> con spec.md, plan.md y specs/contracts/.
Si el código aprendió algo que la spec no dice (un límite, un nombre, un caso límite),
proponé el diff de la spec. NO lo apliques: mostrámelo y esperá mi aprobación.
Si hay divergencia que parece un error del código, abrí un bloqueo en tasks.md.
```

### P9 · Cambios de prompts (lazo con evals)

```text
Rol: ai-engineer. Cambiaste un prompt en api/internal/llm/prompts/.
1. Subí la constante *PromptVersion correspondiente.
2. Corré `make evals` con --budget-usd 1 y guardá el resultado.
3. Compará contra la corrida anterior en una tabla por tipo de caso.
4. Explicá cada regresión: qué caso, qué respuesta dio y por qué creés que pasó.
No modifiques evals/cases/: el gold set lo escribe el humano.
```

### P10 · Corregir un bug (spec primero)

```text
Rol: backend-go. Bug: <descripción y cómo reproducirlo>.
1. Escribí un test que reproduzca el bug y que falle.
2. Indicá qué requisito o criterio de aceptación debía cubrirlo; si no existe, proponé
   el cambio de spec (no lo apliques sin mi aprobación).
3. Recién entonces corregí lo mínimo. Corré `make api-test`.
```

### P11 · Cierre de sesión (higiene de contexto)

```text
Escribí specs/<NNN>/STATUS.md con: qué se hizo (tareas y ramas), qué falta, decisiones
tomadas y por qué, bloqueos abiertos y los próximos 3 pasos. Tiene que alcanzar para
que otro agente retome mañana sin esta conversación.
```

---

## 7. Ejemplo completo: `001-streaming-sse`

### `spec.md` (resumen)

**Qué y por qué:** el usuario quiere ver el avance de una verificación en vivo (leyendo, buscando fuentes, razonando, auditando) en lugar de esperar varios segundos sin señales.

**Requisitos funcionales (EARS)**

| ID | Requisito |
|---|---|
| FR-001 | Cuando el cliente envíe `POST /v1/verifications` con un input válido, el sistema deberá responder 202 con un `id` y la URL de eventos. |
| FR-002 | Si el input está vacío o supera 2000 caracteres, entonces el sistema deberá responder 400 sin crear la verificación. |
| FR-003 | Cuando el cliente abra `GET /v1/verifications/{id}/events`, el sistema deberá enviar los eventos en orden con un `id` numérico creciente. |
| FR-004 | Mientras el stream esté abierto, el sistema deberá enviar un latido (comentario SSE) cada 15 segundos. |
| FR-005 | Cuando el cliente se reconecte con `Last-Event-ID = n`, el sistema deberá reenviar solo los eventos con id > n. |
| FR-006 | El sistema deberá cerrar el stream después de enviar `done` o `failed`. |
| FR-007 | Si el `id` no existe, entonces el sistema deberá responder 404. |
| FR-008 | El sistema deberá permitir CORS solo para los orígenes configurados e incluir `Last-Event-ID` en los headers permitidos. |

**No funcionales**

| ID | Requisito |
|---|---|
| NFR-001 | El servidor HTTP deberá usar solo la biblioteca estándar de Go. |
| NFR-002 | La ruta SSE no deberá pasar por middleware de timeout ni de compresión. |
| NFR-003 | `go vet ./...` y `go test -race ./...` deberán pasar. |

**Criterios de aceptación**

| ID | Cubre | Verificación |
|---|---|---|
| AC-001 | FR-001, FR-002 | Test de `POST` válido e inválido |
| AC-002 | FR-003, FR-006 | Test del flujo completo: las etapas llegan en orden y el stream termina en `done` |
| AC-003 | FR-005 | Test de reanudación con `Last-Event-ID` |
| AC-004 | FR-007 | Test de id desconocido → 404 |
| AC-005 | FR-008 | Test de preflight con `Last-Event-ID` y de origen no permitido |
| AC-006 | NFR-001 | `go.mod` sin dependencias externas de HTTP |

**Fuera de alcance:** autenticación, persistencia de eventos en Postgres, múltiples instancias.

### `tasks.md` (esqueleto)

```markdown
## T00 · Migrar el HTTP de Go a la biblioteca estándar
- Rol: backend-go
- touches: api/internal/httpapi/**, api/go.mod, api/go.sum
- Depende de: —
- Criterios: AC-001…AC-006
- Qué se pide:
  - Reemplazar chi por `net/http` (`ServeMux` de Go 1.22: patrones con método y comodines,
    `r.PathValue("id")`).
  - Escribir a mano solo lo necesario: recuperación de pánicos, ID de petición y CORS.
  - Mantener la ruta SSE fuera de cualquier envoltorio de timeout o compresión.
  - Quitar `github.com/go-chi/chi/v5` de go.mod y go.sum.
- Cómo verificar: `make api-test` (los tests existentes deben pasar SIN modificarse)
  y `go list -m all` sin dependencias de HTTP de terceros.
- Definición de listo: criterios cumplidos, `gofmt`/`vet`/`test -race` en verde, diff < 200 líneas netas.

## T01 · Documentar el contrato de eventos
- Rol: architect
- touches: specs/contracts/**
- Qué se pide: describir cada evento (`stage`, `source`, `verdict`, `failed`, `done`) con su payload
  y un ejemplo; dejar explícito que `failed` no se llama `error`.
- Cómo verificar: el contrato coincide con `api/internal/domain` y `web/src/lib/types.ts`.

## T02 · Cabeceras de proxy de confianza  [P]
- Rol: backend-go
- touches: api/internal/httpapi/**
- Qué se pide: tomar la IP del cliente de `CF-Connecting-IP` solo si el origen está configurado
  como proxy de confianza.
...
```

> **T00 es una buena primera tarea real:** el scaffold actual usa chi y esta tarea lo elimina. Los tests existentes son la prueba de que el comportamiento no cambió.

---

## 8. Plantillas

### `spec.md`

```markdown
# Spec NNN · <nombre>

## Qué y por qué
<3–5 oraciones, sin tecnología>

## Historias de usuario
- P1 · Como <quién> quiero <qué> para <por qué>. Se prueba con: <cómo>.

## Requisitos funcionales (EARS)
| ID | Requisito |
|---|---|
| FR-001 | ... |

## Requisitos no funcionales
| ID | Requisito (con número) |
|---|---|

## Casos límite y errores
- ...

## Criterios de aceptación
| ID | Cubre | Verificación (test / eval / comando) |
|---|---|---|

## Fuera de alcance
- ...

## Preguntas abiertas
- [NECESITA ACLARACIÓN] ...
```

### `plan.md`

```markdown
# Plan NNN · <nombre>

## Paquetes y archivos afectados
## Cambios de contrato
## Decisiones y alternativas descartadas
## Modelo de datos y migraciones
## Riesgos
## Estrategia de pruebas
| AC | Tipo de prueba | Dónde |
|---|---|---|
```

### `tasks.md`

```markdown
# Tareas NNN · <nombre>

## Tnn · <título>
- [ ] Hecha
- Rol:
- touches:
- Depende de:
- Criterios (AC):
- Cómo verificar (comando exacto):
- Definición de listo:

## Bloqueos
- (el agente anota acá sus dudas; no decide solo)
```

### ADR (`docs/adr/NNNN-titulo.md`)

```markdown
# ADR NNNN · <decisión>
Estado: propuesta | aceptada | reemplazada · Fecha:
## Contexto
## Decisión
## Alternativas descartadas
## Consecuencias
```

### Plantilla de PR

```markdown
**Tarea:** specs/NNN-x · Tnn
**Criterios cubiertos:** AC-...
**Cómo se verificó:** (pegá la salida de make api-test / make evals)
**Rutas tocadas:** (deben estar dentro de `touches`)
**Dependencias nuevas:** ninguna / ADR NNNN
**Supuestos del agente:**
**Revisado por (otro modelo):** PASS / cambios pedidos
```

---

## 9. Protocolo para trabajar "en segundo plano"

1. **Preparación (una vez).**
   - Rama principal protegida: nada entra sin PR y sin CI en verde.
   - CI mínimo: `gofmt`, `go vet`, `go test -race`, build de `web` y evals de humo con tope de gasto.
   - Claves de desarrollo con **límite de gasto** propio. Nunca claves de producción en el entorno del agente.
2. **Compuertas humanas (no se saltean).**
   - Aprobás la spec, luego el plan y las tareas (después de P5), luego cada PR, luego el merge.
3. **Lotes.** Podés pedir varias tareas seguidas:
   ```text
   Ejecutá T00, T01 y T02 en orden, una rama por tarea. Commit por tarea con el mensaje
   "Tnn: <título>". Si un criterio falla dos veces seguidas, parate y escribí el bloqueo.
   Al terminar, ejecutá P11.
   ```
4. **Revisión cruzada.** Cada PR pasa por P7 con un modelo distinto al que implementó, antes de que lo mires.
5. **Anti-deriva.** El agente nunca edita `spec.md`, `plan.md` ni la constitución por su cuenta: propone el diff (P8) y vos aprobás.
6. **Paralelismo.** Solo tareas `[P]` con `touches` disjuntos y ramas separadas.
7. **Higiene de contexto.** Una sesión por tarea; pasá rutas en vez de pegar archivos; cerrá con `STATUS.md` (P11).
8. **Costo.** Tope de gasto por clave, `--budget-usd` en los evals y un máximo de intentos por tarea.

---

## 10. Trazabilidad

Cada requisito debe llegar hasta una prueba. Mantené una matriz mínima en cada `plan.md`:

| Requisito | Criterio | Tarea | Prueba |
|---|---|---|---|
| FR-005 | AC-003 | T00 | `TestSSEResumeWithLastEventID` |
| FR-008 | AC-005 | T00 | `TestCORSPreflightAllowsLastEventID` |
| Principio 4 (citas literales) | AC-0xx | T0x | `TestGroundingDowngradesInventedQuote` |

Regla: **un requisito sin prueba no existe**. La fase Analizar (P5) lo detecta.

---

## 11. Anti-patrones

| Anti-patrón | Por qué falla | Qué hacer |
|---|---|---|
| Spec que dice "usar la librería X" | Es un plan disfrazado; la spec no debería cambiar con la tecnología | El qué en la spec, el cómo en el plan |
| Criterios vagos ("debe ser rápido") | No se pueden testear | Números: "p95 < 3 s con 5 fuentes" |
| Tareas gigantes | El agente improvisa en el medio | Un PR, ≈200 líneas netas |
| El agente edita la spec "para que coincida con el código" | Borra la fuente de verdad | Solo propone el diff (P8) |
| Mismo modelo implementa y revisa | Puntos ciegos compartidos | Modelos distintos |
| Aprobar sin leer el diff | Delegaste el criterio | La revisión humana es la compuerta final |
| Agregar dependencias "porque sí" | Superficie de ataque y mantenimiento | ADR obligatorio |
| Pegar todo el repo en el prompt | Contexto saturado, respuestas peores | Rutas y archivos puntuales |
| Tests que se escriben después y "pasan siempre" | No prueban nada | Tests primero y verlos fallar |
| Specs eternas que nadie actualiza | Se pudren | Converger (P8) después de cada merge |

---

## 12. Tu primer día

1. Creá la estructura de carpetas de la sección 3 (carpetas vacías con un `.gitkeep`).
2. Pegá la constitución de la sección 4 en `.specify/memory/constitution.md` (o ejecutá P0).
3. Corré el meta-prompt de roles (sección 5) y **leé los 8 archivos**: son tu contrato con los agentes.
4. Creá `specs/000-fundacion/` y `specs/001-streaming-sse/` con P1 (usá la spec de la sección 7 como base).
5. Respondé las preguntas de P2.
6. Generá el plan (P3) y las tareas (P4). Revisá que T00 sea la migración a la biblioteca estándar.
7. Corré P5. Si da NO-GO, arreglá lo que marque; si da GO, aprobá.
8. Implementá **T00** con P6 (rol `backend-go`).
9. Pasá el diff por P7 con otro modelo. Leé el diff vos. Mergeá.
10. Corré P8 y P11. Recién entonces pasá a la siguiente tarea.

---

## Glosario

- **SDD:** desarrollo guiado por especificaciones.
- **Constitución:** reglas no negociables que todo agente lee en cada sesión.
- **Spec:** el *qué* y el *por qué*, con criterios verificables.
- **Plan:** el *cómo* (arquitectura, archivos, riesgos, pruebas).
- **Tarea:** un paso chico que cabe en un PR.
- **`touches`:** lista de rutas que una tarea puede modificar.
- **EARS:** plantillas de una oración para escribir requisitos testeables.
- **ADR:** registro de una decisión de arquitectura.
- **Converger:** volver a alinear spec y código después de implementar.
- **Compuerta (gate):** punto donde un humano aprueba antes de seguir.
- **IA-a-IA:** un modelo revisa el trabajo de otro, de un proveedor distinto.
