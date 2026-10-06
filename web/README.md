# web/

Sitio de Lupa en Astro 7 con una sola isla de streaming (Preact); casi todo HTML estático, desplegado en Cloudflare Workers. **Sin código todavía.**

## Estructura prevista (DESIGN.md, sección 4)

```text
web/
└── src/
    ├── pages/         páginas estáticas y /v/[id] (SSR para previews al compartir)
    ├── components/    la isla de verificación (único componente cliente)
    └── lib/           tipos que replican specs/contracts
```

## Reglas del paquete

- La isla de streaming es el único componente cliente.
- Los tipos replican `specs/contracts`; el contrato se cambia primero allí. El evento de error de negocio se llama `failed`.
- Sin secretos en el repo; configuración por variables de entorno.
- Aviso visible de "generado por IA, puede contener errores".

## Tareas del ROADMAP que lo implementan

- Spec 004: T004.1 a T004.5
- Spec 006: T006.5
