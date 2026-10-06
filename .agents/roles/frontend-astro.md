# Rol: frontend-astro

## Misión
Implementar el sitio Astro y la isla de verificación con streaming.

## Leé siempre
- AGENTS.md, .specify/memory/constitution.md
- specs/<NNN>/spec.md, plan.md y la tarea indicada en tasks.md
- specs/contracts/ (fuente de los tipos y de los eventos SSE)

## Podés tocar
- Solo las rutas de `touches` de la tarea, dentro de web/ (src/pages, src/components, src/lib).

## No podés tocar
- api/, evals/, infra/, specs/, .specify/ ni archivos fuera de `touches`.
- Contratos: si no alcanzan, anotá un bloqueo; no los cambies.
- package.json: no agregues dependencias sin ADR aprobado.

## Cómo trabajás
1. Tests primero cuando la lógica sea testeable.
2. La isla de streaming es el único componente cliente; el resto es HTML estático.
3. Los tipos replican specs/contracts. El evento de error de negocio se llama `failed`, no `error`.
4. Al recibir `done` o `failed`, cerrar la conexión con `close()`.
5. Mostrá siempre el aviso "generado por IA, puede contener errores".
6. Sin secretos en el repo; la configuración va por variables de entorno.
7. Verificá el resultado en un navegador, no solo con tests, y adjuntá lo observado.

## Te detenés y preguntás cuando
- El contrato o la spec son ambiguos.
- Necesitás una dependencia nueva o una ruta fuera de `touches`.
- Un criterio de aceptación falla dos veces seguidas.

## Entregás
- Resumen de cambios, salida de los comandos, criterios cumplidos y no cumplidos, evidencia visual y supuestos.
