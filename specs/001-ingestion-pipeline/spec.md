# 001 — Canonical publication ingestion

**Status:** DRAFT | **Version:** 0.4 | **Priority:** P0 | **ADR:** [012](../../docs/architecture/decisions/ADR-012-canonical-publication.md)

## Objective
Collect all eligible official publications and their accessible documents from each source's activation baseline onward, independent of subscriber terms. **No historical backfill.** An edition is a Publication of type EDITION; standalone calls and notices are equally valid.

## Functional requirements
- **FR-001:** Each source run has unique ID, trigger, status, timestamps, counts and correlation ID.
- **FR-002:** Each adapter emits `canonicalPublicationKey` scoped to `sourceId`, `publicationType`, official URL and optional official ID, number, series, date and metadata.
- **FR-003:** Persist Publication/PublicationDocument/DocumentVersion in PostgreSQL and immutable PDF bytes in S3-compatible storage.
- **FR-004:** Repeated same publication/document/hash is idempotent; changed bytes create a new immutable version.
- **FR-005:** A publication can contain multiple logical documents, including main file, supplement and annex.
- **FR-006:** Extraction state and text are stored independent of matching.
- **FR-007:** Activate each source with a documented baseline and overlap window; checkpoint advances only after durable processing.
- **FR-008:** Authenticate/authorize internal requests per source.
- **FR-009:** Explicit PARTIAL/FAILED status and recoverable errors; no false success.
- **FR-010:** Only LIVE runs; no historical coverage or backfill endpoints.
- **FR-011:** Each adapter declares capabilities and passes a common contract test suite without requiring schema/API changes.
- **FR-012:** Store observations and original source metadata for provenance; URL is not universal identity.
- **FR-013:** Support two-step manifest registration and verified binary upload; server never blindly trusts client hash.

## Nonfunctional requirements
- **NFR-001:** Docker Compose local end-to-end.
- **NFR-002:** Source-agnostic ingestion API; Python adapter compatibility.
- **NFR-003:** Binary upload with size, MIME, signature and SHA-256 validation; no base64 PDF in JSON or arbitrary server-side URL fetch.
- **NFR-004:** Transactional outbox and reconciler for storage/DB inconsistencies.
- **NFR-005:** Trace run → publication → document → version → object.
- **NFR-006:** Source-specific rate limits, timeouts and explicit coverage limitations.

## Acceptance
- **AC-001:** New EDITION and standalone CALL both persist via same API.
- **AC-002:** Replay does not duplicate publication, document or identical version.
- **AC-003:** Changed bytes produce new version, previous version remains.
- **AC-004:** No matching terms still stores every eligible document.
- **AC-005:** Main and supplement are separate documents in one publication.
- **AC-006:** Crash between upload and DB completion is reconciled.
- **AC-007:** Failure prevents unsafe checkpoint advancement.
- **AC-008:** Unauthenticated or unauthorized requests rejected.
- **AC-009:** Pre-activation items excluded, item published during activation not lost.
- **AC-010:** A fifth adapter passes conformance tests without new tables or endpoints.

## Out of scope
Historical backfill, billing, matching, customer notifications, Kubernetes, Terraform as a mandatory runtime.

## Open decisions
Baseline validation per source, official identifier stability, object retention, maximum file size, pilot source and the exact source cursor semantics.
