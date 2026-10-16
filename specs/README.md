# Spec-Driven Development — Radar Público

## Goal
Make specs the implementation contract for humans and AI agents. This folder contains **proposals**, not proof of implemented behavior.

## Lifecycle
`DRAFT → REVIEW → APPROVED → IN_PROGRESS → VERIFIED → RELEASED`. Only approved specs may drive implementation. Record owner, status, version, date, dependencies, and links in each feature spec. Do not mark VERIFIED without executed acceptance evidence.

## Folder convention
`NNN-kebab-case/` per feature. Required: `spec.md` (why/what), `plan.md` (how), `tasks.md` (ordered units), `acceptance.md` (proof). Optional: `data-model.md`, `contracts/`, `research.md`, `quickstart.md`, `migration.md`.

## Traceability
Requirements `FR-###`, nonfunctional `NFR-###`, scenarios `AC-###`, tasks `T###`. Each task references requirements and tests. Record decisions as ADRs; spec references relevant ADRs.

## Source-of-truth hierarchy
1. `specs/constitution.md` for invariant engineering principles.
2. Approved feature `spec.md` and `acceptance.md` for behavior.
3. Approved `plan.md` and contracts for implementation.
4. `tasks.md` for execution status.
5. `docs/saas/` for broader discovery, historical assumptions and strategy.
When documents disagree, **do not silently choose**: raise a conflict and amend the affected spec.

## AI execution prompt
> Read AGENTS.md, specs/constitution.md, and the target feature directory. Identify open questions, impacted legacy code, risks and tests. Do not implement while the feature status is DRAFT/REVIEW. For an approved task, implement only its scope, run checks, record evidence and report deviations.

## Features
| ID | Feature | Status | Priority |
|---|---|---|---|
| 000 | Platform foundation | DRAFT | P0 |
| 001 | Ingestion pipeline and persistent execution state | DRAFT | P0 |

## Legacy documentation
`docs/saas/` remains intact during transition. A future documentation migration should use redirects/index updates and avoid duplicating conflicting normative requirements.
