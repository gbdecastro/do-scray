# Implementation plan — Radar Público / Sprint 0

**Status:** DRAFT — requires review before implementation.
**Approach:** Spec-Driven Development (SDD), AI-first with human review, Docker-first, incremental migration.
**Scope:** reliable ingestion of official editions and all eligible documents from activation onward; **no backfill**.

## Objective and measurable exit
One pilot source is collected end-to-end through Docker Compose; execution history, edition identity, all associated files, immutable versions, source checkpoint, original PDF and extraction state persist and can be inspected. A replay does not duplicate records. Failures are observable and recoverable. No claims of historical coverage.

## Phase 0 — Documentation governance (DOC)
| Task | Deliverable | Gate |
|---|---|---|
| DOC-001 | docs hub, ownership and precedence | One navigation entry point |
| DOC-002 | migration inventory and move/redirect strategy | No broken references |
| DOC-003 | reconcile SDD with latest EDITION/ALL/START FROM ZERO decisions | No active backfill requirements |
| DOC-004 | approve constitution and Sprint 0 business rules | Owner explicitly signs off |

## Phase 1 — Discovery and source contract (DISC)
| Task | Deliverable | Gate |
|---|---|---|
| DISC-001 | audit four source adapters and tests | Observed behavior, not guesses |
| DISC-002 | define canonical edition and attachment identities per source | Deterministic fixture examples |
| DISC-003 | design activation baseline and safe first checkpoint per source | No gap during activation |
| DISC-004 | choose pilot source and fixtures | Normal, duplicate, republished, partial failure |

## Phase 2 — Infrastructure foundation (INF)
| Task | Deliverable | Gate |
|---|---|---|
| INF-001 | Compose PostgreSQL and MinIO with volumes | Reproducible local start |
| INF-002 | safe env template, health checks, backups | No production secrets |
| INF-003 | containerized API and worker skeletons | Healthy services and logs |
| INF-004 | CI lint/tests/build | Regression evidence |

## Phase 3 — Data and ingestion contracts (DATA)
| Task | Deliverable | Gate |
|---|---|---|
| DATA-001 | PostgreSQL schema: Source, Run, Checkpoint, Edition, EditionDocument, Version, Observation, Attempt, Outbox | Migration and constraints tested |
| DATA-002 | OpenAPI LIVE-only ingestion and authentication | Contract tests |
| DATA-003 | object storage + SHA-256 + idempotent upsert | Replay and integrity tests |
| DATA-004 | extraction status + outbox + reconciliation | Crash/retry evidence |

## Phase 4 — Pilot adapter (PILOT)
| Task | Deliverable | Gate |
|---|---|---|
| PILOT-001 | adapt one crawler without keyword filtering | All eligible current documents persisted |
| PILOT-002 | source activation and checkpoint | Older editions excluded, no activation race |
| PILOT-003 | multi-file editions and version changes | Original and supplement preserved |
| PILOT-004 | parallel/feature-flag migration | Legacy workflow unaffected |

## Phase 5 — Acceptance and readiness (QA)
| Task | Deliverable | Gate |
|---|---|---|
| QA-001 | automated integration and fault-injection tests | Acceptance scenarios pass |
| QA-002 | operational dashboard/logs by run and source | Failures and freshness visible |
| QA-003 | recovery and backup/restore drill | Documented, repeatable |
| QA-004 | Sprint 0 review and sign-off | Evidence in specs/ acceptance files |

## Dependencies
DOC-003/004 → DISC-001/002/003 → DATA-001/002 → DATA-003/004 → PILOT-001/002/003 → QA.
INF-001/002 can run in parallel with DISC after DOC approval. INF-003 depends on contract decisions.

## Explicit non-goals
Historical backfill; subscriptions, billing, tenant-facing matching/alerts, Kubernetes and Terraform as mandatory runtime. Do not migrate all four sources until pilot passes.

## Roles in AI-first delivery
- **Product/Tech Lead (human):** approves scope, source boundaries, business invariants and release gates.
- **Specification agent:** drafts feature specs, contracts and acceptance scenarios.
- **Implementation agent:** implements one approved task at a time.
- **Reviewer/test agent:** challenges edge cases, runs checks and records evidence.
- **Human reviewer:** validates source-specific behavior, security and merge readiness.

## Definition of Ready
Approved feature spec and business rules; canonical identity/activation boundary known; tests and rollback defined; no unresolved blocking decisions.

## Definition of Done
Code + tests actually run + recorded evidence + Docker quickstart + migration/rollback notes + updated docs and ADRs.

## Active links
- [Platform foundation](../../specs/000-platform-foundation/spec.md)
- [Ingestion feature](../../specs/001-ingestion-pipeline/README.md)
- [Task backlog](../../specs/001-ingestion-pipeline/tasks.md)
- [Business acceptance](../../specs/001-ingestion-pipeline/business-acceptance.md)
- [Technical acceptance](../../specs/001-ingestion-pipeline/acceptance.md)
- [Documentation migration](documentation-migration.md)

## Open decisions before coding
Pilot source, precise activation baseline for each adapter, retention policy, operational limits, upload mechanism and whether document extraction is synchronous in first vertical slice.
