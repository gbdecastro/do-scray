# Documentation reorganization plan

**Status:** DRAFT. **This document records the target and prevents premature destructive moves.** Current links remain valid until reviewed and replaced.

## Target taxonomy
- `docs/product/`: vision, business model and product-level requirements.
- `docs/architecture/`: system overview, data model, API guidelines and ADRs.
- `docs/delivery/`: implementation plan, roadmap, sprint entry points and audit.
- `docs/operations/`: production/local operations and legacy runbooks.
- `docs/archive/`: superseded snapshots only; not active requirements.
- `specs/`: authoritative feature specifications, contracts, tasks and evidence.

## Inventory and proposed moves
| Current file | Target path | Action |
|---|---|---|
| docs/saas/README.md | docs/product/vision.md (extract principles) | Review/merge |
| docs/saas/PRD.md | docs/product/requirements.md | Review, avoid duplicating specs |
| docs/saas/BUSINESS.md | docs/product/business-model.md | Review assumptions |
| docs/saas/ARCHITECTURE.md | docs/architecture/overview.md | Review |
| docs/saas/DATA-MODEL.md | docs/architecture/data-model.md | Mark conceptual; specs authoritative |
| docs/saas/API-CONTRACTS.md | docs/architecture/api-guidelines.md | Avoid competing endpoint definitions |
| docs/saas/ADRS.md | docs/architecture/decisions/README.md | Reconcile ADR index |
| docs/saas/ADR-011-DOCKER-FIRST.md | docs/architecture/decisions/ADR-011-docker-first.md | Move unchanged after links updated |
| docs/saas/BACKLOG.md | docs/delivery/legacy-backlog.md | Historical discovery; specs tasks current |
| docs/saas/ROADMAP.md | docs/delivery/roadmap.md | Reconcile no-backfill scope |
| docs/saas/SPRINT-0-AUDIT.md | docs/delivery/sprint-0/legacy-audit.md | Preserve audit observations |
| docs/saas/SPRINT-0-INGESTION.md | docs/delivery/sprint-0/ingestion-design.md | Supersede backfill assumptions |
| docs/automated-execution.md | docs/operations/legacy/automated-execution.md | Move with reference update |
| docs/edition-library.md | docs/operations/legacy/edition-library.md | Move with reference update |
| docs/execution-history.md | docs/operations/legacy/execution-history.md | Move with reference update |
| docs/github-pages-dashboard.md | docs/operations/legacy/github-pages-dashboard.md | Move with reference update |
| docs/persistent-state.md | docs/operations/legacy/persistent-state.md | Move with reference update |
| docs/state-hardening.md | docs/operations/legacy/state-hardening.md | Move with reference update |

## Safe migration steps
1. Inventory inbound links in README, AGENTS, workflows, specs and Markdown files.
2. Reconcile obsolete backfill references and identify normative conflicts.
3. Create destination files and update internal links in the **same reviewed change set**.
4. Keep lightweight compatibility stubs at old paths where GitHub links may exist; do not duplicate full content.
5. Validate Markdown relative links, index navigation and any docs build.
6. Only then remove obsolete duplicates; retain history in Git.

## Documentation ownership
Product: product lead. Architecture/ADRs: tech lead. Delivery: tech lead/engineering. Operations: runtime owner. Specs: feature owner and reviewer.

## Acceptance
No broken internal links; one canonical owner per requirement/contract; all original docs accounted for; historical assumptions visibly labeled; no legacy behavior changed.
