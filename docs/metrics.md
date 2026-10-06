# Métricas de Ingeniería (DORA)

## Lead Time for Changes

| Sprint | Módulo | Lead Time |
|---|---|---:|
| Sprint 1 | Computación | 4.2 días |
| Sprint 2 | Ajedrez | 3.1 días |
| Sprint 3 | Robótica | 2.5 días |
| Sprint 4 | Lenguaje | 2.3 días |

El Lead Time se redujo un 45% entre el primer y último sprint.

## Change Failure Rate (CFR)

- Despliegues exitosos: 92%
- CFR: 8%

La baja tasa de fallos se atribuye a TDD con pytest, revisiones de código
y validación en entorno real.

## Nota metodológica

Las métricas se calcularon a partir del historial de PRs cerrados y hotfixes
registrados en el repositorio durante los 4 sprints.
