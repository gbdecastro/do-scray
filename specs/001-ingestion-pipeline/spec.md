# 001 — Ingestion pipeline and execution state

**Status:** DRAFT | **Version:** 0.1 | **Priority:** P0 | **Dependencies:** 000 Platform foundation
**Related:** `docs/saas/SPRINT-0-INGESTION.md`, `docs/saas/SPRINT-0-AUDIT.md`, ADR-011.

## Problem
Current collectors persist local JSON state and may process only keyword matches. SaaS must preserve all eligible editions with durable execution trace, irrespective of user terms.

## Functional requirements
- **FR-001:** Every scheduled/manual source execution has a unique `source_run` with timestamps, status, counts and correlation ID.
- **FR-002:** Every eligible discovered edition is identified by stable source-scoped canonical key, even without keyword match.
- **FR-003:** Persist metadata in PostgreSQL and original PDFs in S3-compatible object storage.
- **FR-004:** Repeated same document/hash does not create duplicate publication/version.
- **FR-005:** Same canonical publication with changed bytes creates a new immutable version.
- **FR-006:** Extracted text and processing status are stored independently of matching.
- **FR-007:** Partial failure is recoverable, and checkpoints advance only after durable persistence.
- **FR-008:** Internal ingestion endpoints require service authentication and source authorization.
- **FR-009:** Record errors and per-source freshness; never mask partial failure as success.

## Nonfunctional requirements
- **NFR-001:** Local end-to-end operation through Docker Compose.
- **NFR-002:** Source-agnostic ingestion contract, Python adapter compatibility.
- **NFR-003:** PDF upload with size/type/hash validation, no arbitrary URL fetch or base64-in-JSON.
- **NFR-004:** Transactional outbox for post-storage processing, reconciliation for DB/object-storage inconsistency.
- **NFR-005:** Logs trace run ID → publication ID → version ID → object key.

## Acceptance scenarios
- **AC-001:** Given an eligible new edition, when crawler ingests it, then run/publication/version and original PDF are durably stored.
- **AC-002:** Given an identical rerun, when ingestion repeats, then no duplicate publication or version exists.
- **AC-003:** Given same canonical key and changed PDF hash, when ingested, then new version is created and prior one remains.
- **AC-004:** Given a PDF without user keyword match, when collected, then it is still persisted and extractable.
- **AC-005:** Given crash after upload but before DB completion, when reconciler runs, then state recovers or becomes explicit error.
- **AC-006:** Given a source failure, when run closes, then status is PARTIAL/FAILED and checkpoint is not advanced incorrectly.
- **AC-007:** Given unauthenticated ingest request, when submitted, then it is rejected.
- **AC-008:** Given successful extraction, when queried, then text and status are available.

## Out of scope
B2C auth, billing, tenant monitoring, matching, notification delivery and SaaS dashboard.

## Open questions
Canonical identifiers by source; upload strategy (multipart vs signed URL); document retention; source access conditions; OCR resource limits.
