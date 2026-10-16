# 001 — Implementation tasks

**Status:** DRAFT; no implementation performed.

- [ ] T001 [FR-002] Validate canonical identity for all four sources with fixtures.
- [ ] T002 [FR-011] Define typed adapter manifest and conformance suite.
- [ ] T003 [FR-007] Test activation baseline, overlap and partial failure.
- [ ] T004 [FR-003] Migrate PostgreSQL schema for Publication, PublicationDocument, DocumentVersion and operational entities.
- [ ] T005 [FR-013] Finalize OpenAPI manifest/upload negotiation and source authorization.
- [ ] T006 [FR-004] Implement idempotent publication/document/version registration.
- [ ] T007 [FR-013] Verify binary upload, MIME, size, SHA-256 and immutable storage.
- [ ] T008 [FR-007] Implement safe checkpoints and run state transitions.
- [ ] T009 [FR-006] Add extraction, outbox and reconciliation.
- [ ] T010 [FR-011] Implement pilot adapter and second publication type fixture.
- [ ] T011 [NFR-001] Docker Compose integration.
- [ ] T012 [AC-001..AC-010] Execute integration/fault tests and record evidence.

Dependencies: T001–T003 before T004–T005; T004–T005 before T006–T009; T010–T012 last.
No backfill, Edition-only schema or keyword-dependent persistence.
