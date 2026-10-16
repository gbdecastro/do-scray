# 001 — Canonical ingestion business rules

**Status:** DRAFT | PUBLICATION + ALL + START FROM ZERO

- **BR-001:** Publication is universal; Edition is a publication type.
- **BR-002:** Canonical publication identity is unique per source, stable across URL changes.
- **BR-003:** Publication may have multiple logical documents and immutable versions.
- **BR-004:** Same document and hash are idempotent; changed bytes create a new version.
- **BR-005:** Store all eligible accessible documents from source activation, independent of subscriber terms.
- **BR-006:** Record failed/inaccessible documents explicitly; never claim false success.
- **BR-007:** Preserve original bytes and verify checksum before marking stored.
- **BR-008:** Each run records status, counts, errors and observations.
- **BR-009:** Partial failures prevent unsafe checkpoint advancement.
- **BR-010:** Snapshot and overlap must account for publication during activation.
- **BR-011:** Pre-activation history is excluded by default; no backfill.
- **BR-012:** URL is provenance, not universal identity.
- **BR-013:** Adapters emit canonical manifests and cannot write domain tables directly.
- **BR-014:** Every adapter passes common conformance tests.
- **BR-015:** Authenticated ingestion is source-authorized.
- **BR-016:** Original remains available if extraction fails.
- **BR-017:** No source-specific relational tables or API endpoints.
- **BR-018:** No historical completeness claim.
- **BR-019:** Multiple documents under one publication are independently tracked.
- **BR-020:** Recovery is durable and observable.

Supersedes earlier Edition-only and backfill business rules.
