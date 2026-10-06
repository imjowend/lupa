# ADR 0001 · Base de datos
Estado: **propuesta** · Fecha: 2026-10-05 · Decide: humano

## Contexto
Lupa necesita persistencia para documentos y versiones del corpus, verificaciones y su historial de eventos, costos por llamada (`llm_calls`), evals y, más adelante, eventos de cambio y suscripciones. Los vectores van en Qdrant, aparte.

`docs/DESIGN.md` asume PostgreSQL en Docker en la misma VM, y la constitución (principio 7) permite **un único driver de base de datos**, según este ADR. La decisión **no está tomada**: este documento solo ordena las opciones.

Restricciones conocidas: VPS Oracle Always Free con 24 GB de RAM compartidos con API, worker, Qdrant y cloudflared; solo biblioteca estándar de Go más un driver; la cola de trabajos vive en la base de datos; hay backups a R2 y prueba de restauración (T007.3); varios procesos (API y worker) acceden a los datos.

## Opciones

### A · SQLite
- A favor: sin servidor ni contenedor extra; menos memoria y operación; backup simple (copia de archivo).
- A considerar: concurrencia de escritura entre API y worker; qué driver usar (hay opciones con y sin CGO) y su impacto en el build ARM64; cola de trabajos sobre una base embebida; migración futura a Postgres si el producto crece.

### B · PostgreSQL
- A favor: concurrencia y transacciones robustas entre procesos; es lo que asume DESIGN.md; driver `pgx`; camino natural si se agregan cuentas y alertas de pago.
- A considerar: un servicio más que operar y respaldar en la VM; consumo de memoria; configuración de backups y restauración.

## Decisión
**Pendiente.** Decide el humano. Este ADR sigue en estado *propuesta* hasta que lo haga.

## Alternativas descartadas
Ninguna todavía.

## Consecuencias
Mientras el ADR no esté aceptado, ninguna tarea que dependa de la base puede avanzar: T000.5, T001.3, T002.1, T003.5, T006.1 y T007.3 dependen de T000.2 (directa o indirectamente). Al decidir, hay que actualizar `.env.example` (`DATABASE_URL`), los roles afectados y los planes de esas specs.

## Preguntas para quien decide
- ¿Cuántas escrituras concurrentes esperás entre API y worker?
- ¿Querés operar un servicio de base de datos en la VM o preferís un archivo?
- ¿Cuándo esperás agregar cuentas y pagos (Pro)?
