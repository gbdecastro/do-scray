# Radar Público — Documentation hub

**Documentation architecture:** product / architecture / delivery / operations / archive.

> **Source of truth:** executable feature requirements, contracts, tasks and acceptance evidence live in [../specs/](../specs/). This directory holds product context, architecture, delivery planning and runbooks. Agents must also read [../AGENTS.md](../AGENTS.md).

## Start here
| Audience | Entry point | Purpose |
|---|---|---|
| Product owner | [Product](product/README.md) | Vision, requirements and business assumptions |
| Engineer/architect | [Architecture](architecture/README.md) | Technical context and decisions |
| Tech lead / delivery | [Implementation plan](delivery/implementation-plan.md) | Phases, gates, responsibilities and sequencing |
| Developer / AI agent | [Sprint 0](delivery/sprint-0/README.md) | Execution scope and specification links |
| Operator | [Operations](operations/README.md) | Current legacy runbooks |
| Reviewer | [Archive](archive/README.md) | Migration policy and historical documents |

## Status and conventions
- `APPROVED`: binding decision, subject to constitution.
- `DRAFT`: proposed; not authorization to implement.
- `LEGACY`: documents current existing system; not SaaS target requirements.
- `ARCHIVED`: retained for provenance; never use as current requirements.

## Documentation migration
The prior `docs/saas/` folder and root legacy runbooks now contain compatibility links to canonical destinations. [Migration plan](delivery/documentation-migration.md) records the source-to-destination mapping. Do not copy competing normative requirements into multiple locations.
