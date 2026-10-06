# Lupa — Documento de diseño y plan (versión final)

Documento de diseño y plan · versión final

5 de octubre de 2026 · Pensado para leer, no para ejecutar. Los costos son estimaciones y los precios pueden cambiar: verificalos en cada consola antes de cargar créditos. No es asesoría legal ni tributaria.

> **Lupa en una frase:** verifica afirmaciones sobre inteligencia artificial contra documentación oficial, con citas literales, fecha de captura y una abstención explícita cuando no hay datos. Es un proyecto de portfolio, gratuito, que se construye con agentes de código bajo desarrollo guiado por especificaciones (SDD).

## 1. Qué es y qué hace

### 1.1 El verificador (gratis)

**Qué hace**
- Recibe una afirmación sobre modelos de IA (un precio, un límite, una fecha, una capacidad) como texto, captura de pantalla o link de tweet.
- Responde con un veredicto por afirmación, las citas literales que lo respaldan, el enlace a la fuente y la fecha de captura. Si el dato no está en las fuentes, se abstiene y lo dice.
- No conversa, no opina y no hace pronósticos: es una herramienta de consulta puntual. Si el texto es un pronóstico o una opinión, lo informa como "no verificable".

**Cómo lo hace**
1.  **Router:** un modelo barato descarta lo que no tiene afirmaciones verificables y extrae hasta 3 afirmaciones atómicas.
2.  **Evidencia:** busca en un corpus cerrado de documentación oficial indexado en Qdrant. Si el claim trae un link externo, lo trae con Firecrawl. Los tweets se leen solo con la API oficial de X.
3.  **Juez (GPT-6 Luna):** razona solo con la evidencia recibida y devuelve el veredicto en JSON estricto, citando fragmentos.
4.  **Defensas en código:** cada cita debe aparecer literal en la evidencia; si no, se descarta y el veredicto se degrada a "no encontrado".
5.  **Auditor (Gemini):** un modelo de otro proveedor comprueba que cada cita respalde la afirmación (patrón IA a IA). Si discrepa, el veredicto queda "en disputa".
6.  **Streaming:** el progreso llega en vivo al navegador por SSE: leyendo, buscando fuentes, razonando, auditando, veredicto.

| **Veredicto**                    | **Cuándo se usa**                                           |
|----------------------------------|-------------------------------------------------------------|
| **Respaldado**                   | La fuente lo afirma de forma explícita y la cita es válida. |
| **Parcial**                      | Cierto con matices: otra versión, región, plan o condición. |
| **Contradicho**                  | La fuente dice otra cosa.                                   |
| **Desactualizado**               | Fue cierto hasta una fecha y luego cambió.                  |
| **No encontrado en las fuentes** | Abstención: el dato no está en el corpus.                   |
| **No verificable**               | Pronóstico u opinión.                                       |
| **En disputa**                   | Lo asigna el código cuando el Auditor no respalda al Juez.  |

### 1.2 Alertas de cambios (producto de pago, fase posterior)

**Qué hace**
- Vigila las fuentes oficiales y avisa cuando cambia algo que importa: **precios, límites (contexto, salida, rate limits), deprecaciones, modelos nuevos o retirados y políticas**.
- Cada alerta indica qué cambió (antes → después), desde cuándo, el enlace oficial y la fecha de captura.
- El usuario elige proveedores, modelos y tipos de cambio, y recibe el aviso por email, Telegram o webhook. Un changelog público con 24 h de retraso y un RSS son la versión gratuita.

**Cómo lo hace**
1.  Un job programado descarga las páginas vigiladas (precios, modelos, changelog, deprecaciones) y consulta los endpoints de listado de modelos de cada proveedor cuando existan.
2.  Normaliza el contenido, compara el hash con la versión anterior y, si cambió, calcula el diff por secciones.
3.  Un extractor estructurado lee precios y límites y compara valores: los números salen de la extracción, no de un resumen libre.
4.  Luna clasifica el cambio y redacta el resumen antes → después en JSON estricto. Un chequeo valida que cada número del resumen aparezca en el diff.
5.  Los cambios cosméticos se descartan por umbral de materialidad. El resto se guarda como evento y se cruza con las suscripciones.
6.  Se envía la alerta y se publica en el changelog y el RSS.

### 1.3 Qué no es
- No es un chat ni un asistente: no mantiene conversación.
- No emite veredictos sobre personas ni arma rankings de cuentas.
- No verifica pronósticos, opiniones ni especulación de trading.
- No es un bot que responde en X.

## 2. Decisiones: qué se eligió y qué se descartó

| **Tema**             | **Elegido**                                                                                  | **Descartado y por qué**                                                                                                                    |
|----------------------|----------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| **Front**            | Astro 7 con una sola isla de streaming; 95% HTML estático. Despliegue en Cloudflare Workers. | Next.js: el sitio es casi todo estático, ya dominás Astro y el bundle es más chico en Workers.                                              |
| **HTTP en Go**       | Solo la biblioteca estándar (net/http de Go 1.22+).                                          | chi: Go 1.22 ya trae rutas con método y comodines; el resto del middleware es corto. Menos dependencias.                                    |
| **Datos y vectores** | PostgreSQL (verdad) + Qdrant en Docker en la misma VM.                                       | DynamoDB (un salto de red de más) y pgvector (Qdrant da búsqueda híbrida y filtros). Redis: la cola vive en Postgres.                       |
| **Modelos**          | Router barato; Juez GPT-6 Luna; Auditor Gemini de otro proveedor.                            | Un solo modelo para todo (errores correlacionados) y Grok dentro del pipeline (queda solo como comparador en el benchmark).                 |
| **Embeddings**       | Jina por API; decisión final con recall@5 sobre tu gold set.                                 | Elegir por precio: la diferencia con Gemini es de ~USD 2 por 10M de tokens.                                                                 |
| **Tweets**           | API oficial de X, al final y de forma opcional.                                              | Scraping de x.com (incluido Firecrawl, que además cuesta ~30 créditos por URL) y bot que responda en X (exige aprobación previa).           |
| **Acceso**           | Sin login en el MVP: modo demo, cuota por IP y Turnstile.                                    | Correo y contraseña, cuentas y pagos desde el día uno.                                                                                      |
| **Cobro**            | Merchant of Record (Creem o Polar), solo después de validar demanda.                         | Stripe directo y Stripe Managed Payments: no están disponibles para vendedores en Perú.                                                     |
| **Qué se cobra**     | Alertas de cambios.                                                                          | Cobrar la verificación: compite con Grok gratis dentro de X.                                                                                |
| **Alcance**          | Corpus de IA (OpenAI, Anthropic, Google, xAI). Economía con datos duros, después.            | Trading y especulación, medicina, rankings de políticos o periodistas e inflación por provincia (el INDEC publica regiones, no provincias). |
| **Desarrollo**       | Agentes de código con SDD; vos sos dueño de la spec, los evals y la revisión.                | Vibe coding sin especificación.                                                                                                             |

## 3. Arquitectura

| **Capa**     | **Componente**                     | **Dónde corre**        | **Función**                                                              |
|--------------|------------------------------------|------------------------|--------------------------------------------------------------------------|
| **Cliente**  | Navegador                          | —                      | Formulario y progreso en vivo.                                           |
| **Borde**    | Cloudflare: DNS, Turnstile, Tunnel | Cloudflare             | Anti-bot, TLS y acceso a la VPS sin puertos abiertos.                    |
| **Front**    | Astro 7 + isla (Preact)            | Cloudflare Workers     | Páginas estáticas; SSR solo de /v/\[id\] para los previews al compartir. |
| **API**      | Go, net/http                       | VPS Oracle A1 (Docker) | Endpoints, SSE, cuotas y kill switch de gasto.                           |
| **Worker**   | Go                                 | VPS (Docker)           | Ingesta del corpus, detección de cambios y notificaciones.               |
| **Datos**    | PostgreSQL                         | VPS (Docker)           | Documentos, versiones, verificaciones, costos, evals.                    |
| **Vectores** | Qdrant                             | VPS (Docker)           | Corpus y caché semántica (colecciones separadas).                        |
| **Archivos** | Cloudflare R2                      | Cloudflare             | Backups y snapshots privados de páginas.                                 |
| **Modelos**  | Luna, Gemini, Jina                 | APIs externas          | Veredicto y clasificación; auditoría e imágenes; embeddings.             |
| **Fuentes**  | Firecrawl, Jina Reader, API de X   | APIs externas          | Páginas externas; tweets (opcional).                                     |

### 3.1 Streaming de Go a la isla de Astro
- **Dos pasos:** POST /v1/verifications crea el job y devuelve un id; GET /v1/verifications/{id}/events abre el stream SSE. El token de Turnstile viaja en el POST.
- **En Go:** se hace flush con http.ResponseController y se desactiva el tiempo límite de escritura solo para esa conexión. La ruta SSE no lleva timeout ni compresión.
- **Latido y reanudación:** un comentario SSE cada 15 s evita que un proxy cierre la conexión (Cloudflare corta conexiones inactivas tras unos 100 s: verificalo). El servidor guarda el historial de eventos y, si el cliente se reconecta con Last-Event-ID, reenvía lo que faltó.
- **En el navegador:** EventSource dentro de la isla. Al recibir "done" o "failed" se llama a close(); si no, el navegador reconecta solo. El evento de error de negocio se llama "failed" porque "error" ya lo usa EventSource para las fallas de conexión.
- **Qué se transmite:** etapas y el veredicto final validado, no los tokens del JSON del Juez (un JSON parcial no se puede mostrar).
- **CORS:** solo los orígenes configurados, con Last-Event-ID permitido en los headers.

### 3.2 Defensas contra alucinaciones
- **Libro cerrado:** el prompt del Juez prohíbe usar conocimiento previo. Si la evidencia no alcanza, la etiqueta es "no encontrado".
- **Verificación en código:** cada cita debe existir literal en la evidencia citada. Una cita inventada se descarta y baja la confianza; sin citas válidas, el veredicto se degrada.
- **IA a IA:** el Auditor es de otro proveedor, para que sus errores estén menos correlacionados con los del Juez.
- **Prompt injection:** todo texto externo (claims, evidencia, páginas) es dato. Se escapa antes de entrar a un prompt y los prompts lo declaran no confiable.
- **Salida estricta:** JSON Schema, una sola reintentada con el error como retroalimentación y rechazo de etiquetas que el Juez no puede emitir.

## 4. Estructura del monorepo

Un solo repositorio con cuatro paquetes y una capa de especificaciones. La regla de dependencias es hexagonal (puertos y adaptadores): el dominio no conoce a nadie y solo el punto de entrada conoce a los proveedores.

```text
lupa/
├── AGENTS.md                     reglas cortas para cualquier agente
├── README.md · Makefile · docker-compose.yml · .env.example
├── .specify/memory/constitution.md   principios no negociables (SDD)
├── specs/                        una carpeta por funcionalidad (SDD)
│   ├── contracts/                eventos SSE y JSON Schemas compartidos
│   ├── 000-fundacion/            spec.md · plan.md · tasks.md
│   ├── 001-streaming-sse/
│   ├── 002-corpus-e-ingesta/
│   ├── 003-juez-y-auditor/
│   ├── 004-front-astro/
│   ├── 005-evals/
│   └── 006-alertas/
├── .agents/roles/                perfiles de rol para los agentes
├── docs/                         este documento y adr/ (decisiones)
├── api/                          Go (solo biblioteca estándar + driver de Postgres)
│   ├── cmd/api · cmd/worker      puntos de entrada y cableado
│   ├── internal/domain           tipos puros
│   ├── internal/llm              puertos de IA + prompts versionados + validación
│   ├── internal/pipeline         orquestador y defensas en código
│   ├── internal/evidence         puertos de evidencia y guard anti x.com
│   ├── internal/httpapi          rutas, CORS y handler SSE
│   ├── internal/stream           bus de eventos con replay
│   ├── internal/budget           kill switch de gasto
│   ├── internal/store            persistencia en Postgres
│   ├── internal/providers        adaptadores (openai, google, jina...)
│   ├── internal/fakes            implementaciones de demo y de tests
│   └── migrations/
├── web/                          Astro 7 + Preact (src/pages, components, lib)
├── evals/                        casos (jsonl) y arnés de evaluación
└── infra/                        Tunnel, backups, scripts
```

| **Carpeta**                | **Qué contiene**                                                                                   | **Regla**                                                                                               |
|----------------------------|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| **specs/**                 | Qué construir y por qué (spec), cómo (plan) y en qué pasos (tasks), una carpeta por funcionalidad. | Es la fuente de verdad. Si el código y la spec discrepan, se corrige uno de los dos de forma explícita. |
| **specs/contracts/**       | Eventos SSE, JSON Schemas y formas de request/response compartidas.                                | Contrato primero: se cambia aquí y luego en api y web.                                                  |
| **.agents/roles/**         | Un archivo por rol (arquitecto, backend, frontend, IA, evals, revisor, seguridad).                 | Cada sesión de agente empieza leyendo su rol.                                                           |
| **api/internal/domain**    | Tipos y reglas puras.                                                                              | No importa nada del proyecto ni de terceros.                                                            |
| **api/internal/llm**       | Puertos (LLMJudge, CitationAuditor, Router, Completer, Embedder), prompts y esquemas.              | No importa SDKs ni providers. Los prompts se versionan.                                                 |
| **api/internal/pipeline**  | Orquestación y defensas en código.                                                                 | Solo depende de domain, llm, evidence y budget.                                                         |
| **api/internal/providers** | Un adaptador por servicio externo, con HTTP de la biblioteca estándar.                             | Implementa una interfaz chica. Solo cmd/\* los importa.                                                 |
| **api/internal/fakes**     | Implementaciones deterministas.                                                                    | Permiten correr y testear sin claves ni red.                                                            |
| **web/**                   | Sitio estático y la isla de streaming.                                                             | La isla es el único componente cliente. Los tipos replican specs/contracts.                             |
| **evals/**                 | Gold set y arnés.                                                                                  | Los casos los escribe el humano; el arnés corta al superar el tope de gasto.                            |
| **infra/**                 | Cloudflare Tunnel, backups a R2 y scripts.                                                         | Sin secretos en el repo.                                                                                |

**Dependencias externas de Go:** solo el driver de Postgres (pgx). Todo lo demás es biblioteca estándar: net/http, encoding/json, log/slog, embed, context y testing. Agregar una dependencia exige un ADR.

## 5. Servicios, presupuesto y estimaciones

### 5.1 Servicios

| **Servicio**   | **Rol**                                      | **Precio y límites**                                                                                                                                                                                  | **Notas**                                                                                       |
|----------------|----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| **GPT-6 Luna** | Router (opcional) y Juez.                    | USD 0,10 / 0,50 por millón de tokens (entrada/salida). Contexto de ~1M. El razonamiento se factura como salida.                                                                                       | Cargá USD 10 sin auto-recarga y poné límite en el panel.                                        |
| **Gemini**     | Auditor de citas y lectura de capturas.      | Modelo barato (2.5 Flash-Lite): ~USD 0,10 por millón de tokens de entrada. Gemini 3.8 Flash: 0,75 / 3,75 hasta el 31/12/2026 y 1,50 / 7,50 desde 2027. Las imágenes se cobran como tokens de entrada. | USD 30 en créditos de Google AI Pro: verificá el vencimiento y si permiten uso comercial.       |
| **Jina**       | Embeddings y Reader.                         | 10M de tokens gratis por key nueva, compartidos entre embeddings y Reader. Reader sin key: 20 pedidos/min.                                                                                            | Por API, el uso comercial no pide licencia extra.                                               |
| **Qdrant**     | Vectores.                                    | Gratis, autoalojado.                                                                                                                                                                                  | Con 24 GB sobra; poné límite de memoria.                                                        |
| **Firecrawl**  | Páginas externas y carga inicial del corpus. | ~102k créditos. Scrape: 1 crédito; map: 1 por llamada; search: 2 por 10 resultados.                                                                                                                   | Nunca para x.com (~30 créditos y resuelve con Grok).                                            |
| **API de X**   | Leer tweets (opcional).                      | USD 0,005 por post. USD 20 gratis al guardar la primera tarjeta; vencen a los 3 meses y se gastan primero.                                                                                            | Activarlos al final. Sin auto-recarga, se bloquea al llegar a cero.                             |
| **Cloudflare** | DNS, Turnstile, Workers, Tunnel, R2.         | Workers gratis: 100.000 requests/día y 3 MiB de script. El plan de USD 5/mes sube a 10 MiB y quita el tope diario.                                                                                    | Astro 7 con @astrojs/cloudflare 14 despliega solo en Workers.                                   |
| **VPS Oracle** | API, worker, Postgres, Qdrant, cloudflared.  | 24 GB de RAM confirmados. USD 0 dentro del Always Free.                                                                                                                                               | Revisá Cost Analysis: tu plan previo estimó ~USD 28/mes de excedente si la VM supera el límite. |

### 5.2 Embeddings: qué sirve para qué

| **Modelo**                 | **Qué embebe**                           | **Precio**                                   | **Notas**                                                                                                                  |
|----------------------------|------------------------------------------|----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| **Jina v5-text**           | Solo texto                               | 10M de tokens gratis por key                 | Por API, uso comercial sin licencia extra. Los pesos son CC-BY-NC: autoalojarlos en un producto de pago requiere licencia. |
| **Jina v5-omni / clip-v2** | Texto + imagen (omni suma audio y video) | Igual                                        | Solo si hace falta buscar por imagen.                                                                                      |
| **Gemini embedding-001**   | Solo texto (entrada máx. 2.048 tokens)   | USD 0,15 por millón                          | 10M de tokens ≈ USD 1,50.                                                                                                  |
| **Gemini Embedding 2**     | Texto, imágenes, video, audio y PDF      | USD 0,20 por millón de texto; 0,45 de imagen | Entrada de 8.192 tokens; nació como preview.                                                                               |
- **Para Lupa alcanza con texto.** Las capturas las lee Gemini (que genera texto) y ese texto se embebe. Los embeddings de imagen solo sirven para buscar imágenes similares.
- **La dimensión del vector depende del modelo:** si cambiás de modelo hay que reindexar. La colección de Qdrant se crea con la dimensión que informa el embedder, y el modelo queda registrado en cada chunk.
- **Decisión por calidad:** calculá recall@5 (si el fragmento correcto aparece entre los 5 primeros) con 50–100 preguntas de tu gold set. Si Jina queda a pocos puntos de Gemini, usá Jina.

### 5.3 Presupuesto de créditos

| **Rubro**     | **Monto**               | **Rinde aproximadamente**                                                  |
|---------------|-------------------------|----------------------------------------------------------------------------|
| **Luna**      | USD 10                  | ~2.000–3.000 verificaciones más varias campañas de evals.                  |
| **Gemini**    | USD 30 en créditos      | Miles de auditorías y lecturas de capturas con un modelo Flash-Lite.       |
| **Jina**      | 10M de tokens gratis    | Una pasada completa del corpus inicial; luego solo los chunks que cambian. |
| **Firecrawl** | ~102k créditos          | Carga inicial de 1.200–2.000 créditos; los refrescos van por Jina Reader.  |
| **X API**     | USD 20 gratis (3 meses) | Hasta ~4.000 lecturas de posts.                                            |
| **Front**     | USD 0                   | Workers gratis; USD 5/mes solo si el bundle o las requests lo exigen.      |
| **VPS**       | USD 0                   | Dentro del Always Free; verificá cargos.                                   |
| **Dominio**   | ~USD 10–15 al año       | Estimación. El nombre del producto es un subdominio.                       |

### 5.4 Estimación de costo por verificación

Supuesto: ~3.000 tokens de entrada y ~500 de salida por llamada. Son órdenes de magnitud, no mediciones: la traza por llamada (tabla llm_calls) permite medir el costo real desde el primer día.

| **Componente**                      | **Costo**            | **Nota**                                                        |
|-------------------------------------|----------------------|-----------------------------------------------------------------|
| **Router** (modelo barato)          | ~USD 0,0003          | Luna con razonamiento mínimo o Flash-Lite; se decide con evals. |
| **Embedding de la consulta** (Jina) | ≈ USD 0              | Dentro del cupo gratuito.                                       |
| **Búsqueda en Qdrant**              | USD 0                | Local, sin salto de red.                                        |
| **Juez** (Luna)                     | ~USD 0,001–0,003     | El razonamiento suma.                                           |
| **Auditor** (Gemini Flash-Lite)     | ~USD 0,0005–0,004    | Con 3.8 Flash el costo se acerca al extremo alto.               |
| **Lectura de un tweet** (opcional)  | USD 0,005            | Solo si el pedido trae un link de tweet.                        |
| **Total**                           | **~USD 0,003–0,008** | Sin tweet. Con lectura de tweet, +USD 0,005.                    |
- **Costos fijos mensuales:** USD 0 si el front cabe en Workers gratis y la VM está dentro del Always Free. Pueden sumar USD 5 (Workers de pago) o ~USD 28 (excedente de Oracle).
- **Una campaña de evals completa** (~120 casos) cuesta ~USD 1–3 según cuántas variantes compares.
- **Kill switch:** un tope diario de gasto (por ejemplo USD 1–2). Al alcanzarlo se pausan las verificaciones nuevas y se muestran ejemplos precalculados.

## 6. Corpus de IA

| **Fase**    | **Fuentes**                                                                         | **Qué se indexa**                                                                                             |
|-------------|-------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| **1 (MVP)** | OpenAI, Anthropic, Google (Gemini API), xAI                                         | Precios, modelos y límites, changelog y release notes, deprecaciones, model/system cards, anuncios oficiales. |
| **1.5**     | Independientes: Artificial Analysis, LMArena, SWE-bench, Epoch AI                   | Resultados de benchmarks con fecha y metodología.                                                             |
| **2**       | Mistral, Meta, DeepSeek; OpenRouter (agregador)                                     | Igual que la fase 1. OpenRouter es fuente secundaria: solo para cruzar precios.                               |
| **3**       | Herramientas y agentes: OpenCode, OpenClaw, Hermes Agent, Command Code, Claude Code | Funcionalidades y configuración. Son herramientas, no modelos: otros tipos de claims.                         |
- **Clases de fuente:** primaria (documentación oficial), independiente (benchmarks de terceros) y secundaria (agregadores, prensa). Cada respuesta indica de cuál es su evidencia.
- **Oficial no es igual a cierto:** los benchmarks de un proveedor los autoinforma el propio proveedor.
- **Temporalidad:** cada chunk lleva su fecha de captura y las versiones de una página nunca se sobrescriben. Ejemplos reales: GPT-6 Luna bajó de USD 0,20 / 1,20 a USD 0,10 / 0,50, y Gemini 3.8 Flash tiene precio introductorio hasta el 31/12/2026.
- **Antes de crawlear:** confirmar dominios exactos, robots.txt y términos de cada sitio.
- **Economía (fase posterior):** solo datos duros y oficiales. Los números se consultan por API (Series de Tiempo de datos.gob.ar) con tool calling, y el RAG queda para metodología y conceptos. El IPC del INDEC se publica para el total del país y seis regiones, no por provincia.

## 7. Evals y calidad

Los evals son la pieza que más pesa en el portfolio. Un gold set de ~120 casos escritos por vos, con la respuesta esperada y la fuente. No se copia texto de tweets.

| **Tipo de caso**                  | **Cantidad** | **Qué mide**                                         |
|-----------------------------------|--------------|------------------------------------------------------|
| **Verificable**                   | 40           | Acierto del veredicto y validez de la cita.          |
| **Temporal / desactualizado**     | 20           | Manejo de "era cierto hasta…".                       |
| **No está en el corpus**          | 20           | Abstención correcta, sin inventar.                   |
| **Pregunta cargada**              | 15           | Separar la premisa de lo verificable.                |
| **Pronóstico u opinión**          | 15           | Rechazo correcto con explicación.                    |
| **Prompt injection en la fuente** | 10           | Tratar el texto externo como dato, nunca como orden. |
- **Métricas:** acuerdo con el gold set, validez de las citas, precisión y recall de la abstención, latencia p50/p95 y costo por verificación.
- **Evals de alertas:** ~20 cambios históricos reales y ~20 no-cambios o cambios cosméticos; precisión y recall de la detección y exactitud de los números.
- **CI:** los evals corren ante cada cambio de prompt o modelo, con un tope de gasto por corrida. El informe se publica, incluyendo dónde falla.
- **Benchmark público:** comparación manual contra Grok sobre un subconjunto, con los resultados completos.

## 8. Monetización

Lupa es gratis y de portfolio. Si más adelante se decide cobrar, lo que se cobra son las **alertas de cambios**, no la verificación.

| **Plan**         | **Precio (hipótesis)** | **Incluye**                                                                                             | **Costo para vos**                                         |
|------------------|------------------------|---------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| **Gratis**       | USD 0                  | Verificador con tope diario, changelog público con 24 h de retraso y RSS.                               | ~USD 0,003–0,008 por verificación.                         |
| **Pro**          | USD 9–12 al mes        | Alertas inmediatas por email o Telegram, filtros por proveedor, modelo y tipo, e historial de 12 meses. | Casi nulo por usuario: el costo es el crawling compartido. |
| **Equipo / API** | USD 49–79 al mes       | Webhooks, API key, servidor MCP, varios destinatarios y límites altos.                                  | Igual que Pro.                                             |

### 8.1 Merchant of Record

Un Merchant of Record (MoR) figura como vendedor: cobra, calcula y paga los impuestos al consumidor, gestiona disputas y te transfiere el neto. Precios de septiembre de 2026; confirmalos antes de elegir.

| **Proveedor**               | **Tarifa**                                                   | **Neto en USD 10\*** | **Pagos a Perú**                          | **Notas**                                                                                                   |
|-----------------------------|--------------------------------------------------------------|----------------------|-------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| **Creem**                   | 3,9% + USD 0,40, todo incluido                               | ~USD 9,21            | Sí (banco local)                          | Retiro: USD 7 o 1%, lo que sea mayor. El más barato.                                                        |
| **Polar**                   | 5% + USD 0,50; +1,5% tarjeta extranjera; +0,5% suscripciones | ~USD 8,80            | Sí (vía Stripe Connect Express)           | Cobra con infraestructura de Stripe. Retiro: USD 2/mes activo + 0,25% + USD 0,25, más conversión (0,25–1%). |
| **Lemon Squeezy**           | 5% + USD 0,50; +1,5% extranjero; +0,5% suscripciones         | ~USD 8,80            | Figura en su lista bancaria (doc antigua) | De Stripe; se está integrando a Stripe Managed Payments: confirmá el alta.                                  |
| **Paddle**                  | 5% + USD 0,50, todo incluido                                 | ~USD 9,00            | No lo confirmé                            | El más establecido para SaaS.                                                                               |
| **Stripe Managed Payments** | Tarifa de Stripe + 3,5%                                      | —                    | **No disponible**                         | Su lista de países no incluye Perú. Requeriría una entidad en un país soportado.                            |

\*Tarjeta no estadounidense, suscripción de USD 10, sin impuestos.
- **Ver "Stripe" en el cobro:** Polar es lo más cercano, porque cobra con infraestructura de Stripe. Stripe directo como vendedor no está disponible para tu caso sin una entidad en un país soportado, lo que agrega costos legales e impuestos.
- **Sugerencia:** Creem si priorizás costo; Polar si priorizás Stripe. Verificá el alta como persona natural o empresa.

### 8.2 Presupuesto de ejemplo

Escenario ilustrativo: 30 suscriptores Pro a USD 10 y 3 equipos a USD 49 = **USD 447 de facturación al mes**.

| **Proveedor**           | **Comisiones** | **Retiro mensual** | **Total aprox.** |
|-------------------------|----------------|--------------------|------------------|
| **Creem**               | ~USD 31 (7%)   | ~USD 7             | ~USD 38 (8%)     |
| **Polar (plan gratis)** | ~USD 48 (11%)  | ~USD 4–8           | ~USD 52–56 (12%) |
- **Presupuestá entre 8% y 13%** de la facturación entre comisiones y retiros.
- **No incluye:** impuesto a la renta en Perú (RUC y régimen: consultá a un contador), correo, dominio ni tu tiempo.
- **Uso comercial:** revisá que los créditos regalados (Google AI Pro, X) y los términos de X, Firecrawl y Jina lo permitan. La API de X exige un nivel de pago para uso comercial.

### 8.3 Pasos para llegar al cobro
1.  Todo gratis. Medí sin cuentas (tipos de consulta, repeticiones, costo) y publicá el changelog con RSS.
2.  Sumá una lista de espera de alertas (email opt-in) y hacé 10–15 entrevistas con devs de IA y periodistas tech: qué cambio de un proveedor les costó tiempo o plata.
3.  Señales para avanzar (sugeridas): 30 o más inscriptos, 5 que digan que pagarían y al menos un pago de prueba.
4.  Construí lo que quedó afuera del MVP: cuentas, términos, privacidad (Ley 29733) y el canal de envío (Telegram o correo con SPF, DKIM y DMARC).
5.  Elegí el MoR, hacé el alta y consultá a un contador y a un abogado.
6.  Lanzá Pro con un precio de prueba y mirá retención y uso durante un mes antes de ajustar.

## 9. Desarrollo con agentes y SDD

El código lo escriben agentes (MiniMax, Antigravity u otros) bajo desarrollo guiado por especificaciones (SDD): primero se escribe qué se construye y cómo se sabe que está bien; recién después se pide el código. La guía completa, con roles y prompts, está en el archivo **Lupa-SDD-guia.md**.
- **Constitución:** los principios no negociables del proyecto (libro cerrado, sin scraping de x.com, proveedores detrás de interfaces, solo biblioteca estándar, tests primero).
- **Una spec por funcionalidad** en specs/NNN-nombre, con spec, plan y tareas. Los contratos compartidos viven en specs/contracts.
- **Tareas atómicas:** una por rama, con criterios de aceptación medibles y la lista de rutas que el agente puede tocar.
- **Verificación automática:** CI con tests y evals de humo con tope de gasto. Los evals son los tests de aceptación del producto.
- **No se delega:** la spec, el gold set, la revisión de cada PR, los ADRs y los postmortems. Son las historias que se cuentan en una entrevista.

## 10. Seguridad y cumplimiento
- **Reglas de X:** solo API oficial, sin scraping; el texto de un tweet se guarda solo en caché temporal (se guardan IDs y el análisis); se borra su contenido en menos de 24 h si el tweet se elimina; se muestra con el embed oficial; sin perfilar usuarios ni inferir atributos sensibles; sin entrenar modelos con contenido de X.
- **Prompt injection:** todo texto externo es dato; delimitadores escapados; sin herramientas accesibles desde el contenido; salida validada contra un esquema.
- **Abuso y gasto:** Turnstile, límite por IP, tope de pasos y tokens por verificación y kill switch diario.
- **Privacidad:** sin cuentas en el MVP y logs mínimos. Aviso visible de "generado por IA, puede contener errores".
- **Derechos de autor:** se guardan extractos y enlaces, no páginas completas. Los snapshots en R2 son privados. Se respetan robots.txt y términos.
- **Modo demo y durabilidad:** 20–30 verificaciones precalculadas y el informe de evals público, que cuestan USD 0. Cuando se acaban los créditos, la app cae sola al modo demo.

## 11. Plan por hitos

| **Hito**                      | **Entregable**                                                                                                                                                         |
|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **0 · Fundación**             | Constitución, roles y repo. Migrar el HTTP de Go a la biblioteca estándar. Verificar cargos en Oracle y confirmar dominios y términos de las fuentes.                  |
| **1 · Streaming y corpus**    | SSE de punta a punta (ya hay un esqueleto con fakes). Ingesta de OpenAI y luego de los 4 proveedores, con embeddings y búsqueda híbrida; primera medición de recall@5. |
| **2 · Juez y Auditor reales** | Adaptadores de Luna y Gemini, gold set v1 (60 casos) y arnés de evals.                                                                                                 |
| **3 · Front y despliegue**    | Isla de Astro en Workers, modo demo, Turnstile, kill switch, Tunnel, backups a R2 y observabilidad.                                                                    |
| **4 · Evals y difusión**      | Gold set completo (120), informe público y primer artículo. Opcional: API de X y capturas con Gemini.                                                                  |
| **5 · Alertas**               | Detección de cambios, changelog público y RSS, con evals de alertas.                                                                                                   |
| **Después**                   | Lista de espera y entrevistas; economía con datos duros; cobro con MoR si la demanda se confirma.                                                                      |

## 12. Pendientes
- **Nombre del subdominio** de tu dominio propio; evitar la "X" en el nombre.
- **Embeddings:** confirmar Jina contra Gemini con recall@5.
- **Router:** decidir con evals entre Luna con razonamiento mínimo y Flash-Lite.
- **Gemini:** elegir la versión y confirmar que no esté por deprecarse.
- **Oracle:** revisar cargos en Cost Analysis, aunque la RAM esté confirmada.
- **Límites de cuenta nueva:** revisar rate limits de Luna y Gemini.
- **MoR:** confirmar el alta en Perú antes de elegir proveedor.
- **Tope diario** del kill switch y presupuesto de evals por corrida.
