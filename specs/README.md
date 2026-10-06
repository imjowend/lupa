# specs/

Una carpeta por funcionalidad (`NNN-nombre/`). Es la fuente de verdad: si el código y la spec discrepan, se corrige uno de los dos de forma explícita.

## Cómo leer una spec

| Archivo | Responde |
|---|---|
| `spec.md` | Qué se construye y por qué, y cómo se sabe que está bien (sin tecnología) |
| `plan.md` | Cómo se construye: paquetes, contratos, decisiones, riesgos y pruebas |
| `tasks.md` | En qué pasos chicos y verificables; una tarea = una rama = un PR |
| `STATUS.md` | Estado para retomar sin contexto |

`contracts/` guarda lo que comparten los paquetes (eventos SSE, JSON Schemas). Contrato primero: se cambia ahí y luego en `api` y `web`. `ROADMAP.md` ordena y mide todas las tareas; `make progress` calcula el avance.

## Ciclo SDD

Constitución (una vez) → especificar → clarificar → planificar → tareas → analizar (GO / NO-GO) → implementar una tarea por vez → converger. Cada fase termina en una compuerta humana. Detalle y prompts en [`docs/SDD-GUIA.md`](../docs/SDD-GUIA.md).

## Convención de IDs

| ID | Qué es |
|---|---|
| `Tnnn.m` | Tarea `m` de la spec `nnn` (por ejemplo `T000.1`); se define en `ROADMAP.md` |
| `FR-nnn` | Requisito funcional, en formato EARS |
| `NFR-nnn` | Requisito no funcional, con números |
| `AC-nnn` | Criterio de aceptación, verificable con un test, un eval o un comando |

Un requisito sin prueba no existe.
