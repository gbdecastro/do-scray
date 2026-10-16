# AI Engineering Contract — do-scray / Radar Público

This repository uses **Spec-Driven Development (SDD)**. Read `specs/README.md`, `specs/constitution.md`, and the target feature directory **before** editing code.

## Mandatory workflow
1. **Discover:** inspect existing implementation, tests, and active specs; do not infer missing behavior.
2. **Specify:** create/update `spec.md` with functional requirements, scenarios, constraints, exclusions, and open questions.
3. **Plan:** create/update `plan.md` with architecture, contracts, data migration, risk, tests, rollback, and Docker strategy.
4. **Decompose:** write `tasks.md` with IDs, dependencies, acceptance evidence, and checkboxes.
5. **Implement:** change only approved scope, maintain backward compatibility with legacy crawlers and workflows.
6. **Verify:** run relevant tests and capture actual commands/results in `acceptance.md`; never claim unexecuted tests passed.
7. **Document:** update ADRs for material architectural changes, specs for changed behavior, and operational runbooks.

## Engineering guardrails
- Docker-first; Docker Compose for local reproducibility; Terraform optional for cloud provisioning. See `docs/saas/ADR-011-DOCKER-FIRST.md`.
- Ingestion is independent of customer keywords; persist every eligible discovered publication.
- PostgreSQL for metadata/state, S3-compatible storage for originals; idempotent versions and explicit failure states.
- Do not rewrite working crawlers without an adapter/migration plan and regression fixtures.
- Do not edit production secrets, branch `data`, or workflows outside approved scope.
- Never bypass source access controls; use official APIs/authorized collection and respectful rate limits.
- Tenant boundaries, input validation, observability, testability and LGPD are first-class requirements.
- Do not invent evidence, test results, metrics, or completed tasks.
- No changes to `main` without explicit merge/review.

## Definition of Ready
A task is ready when its spec and acceptance are testable, dependencies known, contracts clear, and unresolved blocking questions identified.

## Definition of Done
Implementation + tests + evidence + documentation + operational impact/rollback, with links to task and spec IDs.

## Navigation
- `specs/README.md` — SDD lifecycle and conventions
- `specs/constitution.md` — product and engineering invariants
- `specs/001-ingestion-pipeline/` — first implementation feature
- `docs/saas/` — discovery and existing planning artifacts
