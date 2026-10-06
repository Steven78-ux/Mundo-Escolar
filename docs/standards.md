# Estándares y Metodología

## Sección 1: Tabla de estándares

| Estándar | Evidencia |
|---|---|
| ISO/IEC 25000 (SQuaRE) | Adecuación funcional, portabilidad (.deb, Linux), mantenibilidad |
| ISO 12207 | Ciclo de vida documentado: diagnóstico, diseño, desarrollo, pruebas, despliegue |
| SOLID | OCP (Factory Method), SRP (capas separadas), DIP (Repository) |
| PEP 8 | Nombrado consistente, estructura modular |
| DORA | Lead Time 2.3 días, CFR 8% |

## Sección 2: Metodología

Enfoque híbrido Waterfall + Scrum:

- Waterfall para análisis, diseño arquitectónico y documento de requisitos
- Scrum para construcción y pruebas (4 sprints de 2 semanas)
- Kanban con WIP ≤ 2
- TDD con pytest

## Sección 3: Herramientas

| Categoría | Tecnología |
|---|---|
| Lenguaje | Python 3.x |
| GUI | CustomTkinter + Pillow + tkExtraFont |
| Persistencia | JSON + Repository |
| Motor ajedrez | Stockfish |
| Control versiones | Git + GitHub |
| Empaquetado | Scripts Debian (.deb) |
