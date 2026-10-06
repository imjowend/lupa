# infra/

Infraestructura de Lupa: Cloudflare Tunnel, backups a R2 y scripts de operación. **Sin código todavía.**

## Estructura prevista (DESIGN.md, secciones 3 y 4)

Tunnel y DNS, backups a R2 con prueba de restauración, Dockerfile ARM64 y compose para la VPS Oracle (también en la raíz según el diseño), y el runbook. La estructura exacta la define el plan de la spec 007.

## Reglas del paquete

- Sin secretos en el repo: todo por variables de entorno; `.env.example` lleva solo nombres.
- Sin puertos abiertos hacia afuera: el acceso es por Cloudflare Tunnel.
- Los backups incluyen una prueba de restauración. La base de datos concreta depende del ADR 0001.

## Tareas del ROADMAP que lo implementan

- Spec 000: T000.3, T000.4
- Spec 004: T004.5
- Spec 007: T007.1 a T007.5
