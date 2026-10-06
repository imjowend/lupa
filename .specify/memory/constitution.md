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
7. Go: solo biblioteca estándar, más un único driver de base de datos (según el ADR 0001). Agregar otra dependencia exige un ADR aprobado.
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
