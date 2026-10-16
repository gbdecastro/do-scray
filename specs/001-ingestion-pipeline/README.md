# Feature 001 — Canonical publication ingestion

**Status:** DRAFT | **Version:** 0.4 | **ADR:** [012](../../docs/architecture/decisions/ADR-012-canonical-publication.md)

## Current business decisions
- **PUBLICATION:** universal aggregate; EDITION, CALL, NOTICE, BULLETIN and OTHER are types.
- **ALL:** ingest every eligible accessible publication and document independent of keywords.
- **START FROM ZERO:** collect from per-source activation baseline forward; no historical backfill.

## Read in order
1. [Business rules](business-rules.md)
2. [Domain model](domain-model.md)
3. [Business scenarios](business-scenarios.md)
4. [Business acceptance](business-acceptance.md)
5. [Functional spec](spec.md)
6. [Technical plan](plan.md)
7. [Logical data model](data-model.md)
8. [OpenAPI 0.4.0](contracts/ingestion.openapi.yaml)
9. [Tasks](tasks.md)
10. [Test evidence](acceptance.md)

## Architecture and discovery
- [Canonical model](../../docs/architecture/canonical-publication-model.md)
- [Adapter conformance](../../docs/delivery/sprint-0/adapter-conformance.md)
- [Static crawler audit](../../docs/delivery/sprint-0/source-audit.md)

No feature document is approved for implementation until reviewed. Existing crawlers remain unchanged.
