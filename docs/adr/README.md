# Decisiones de arquitectura (ADR)

Cada decisión de arquitectura vive en un archivo `NNNN-titulo.md`, con la plantilla [`0000-template.md`](0000-template.md).

- **Estados:** `propuesta` · `aceptada` · `reemplazada`.
- Los redacta el rol `architect`; **las decide el humano**. Un agente nunca pasa un ADR a `aceptada`.
- Toda dependencia nueva exige un ADR aprobado (constitución, principio 7).

| ADR | Tema | Estado |
|---|---|---|
| [0001](0001-base-de-datos.md) | Base de datos (SQLite o Postgres) | propuesta |
