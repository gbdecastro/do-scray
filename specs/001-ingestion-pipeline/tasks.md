# Tasks — 001 Ingestion pipeline

**Status:** DRAFT; no implementation completed.

- [ ] **T001 [FR-002, AC-001]** Inventory identity/edition semantics for Boituva, Sorocaba, Indaiatuba, Cismetro; deliver mapping table and fixtures.
- [ ] **T002 [FR-001, FR-003, AC-001]** Define schema and PostgreSQL migrations; dependency T001.
- [ ] **T003 [FR-002, FR-008, AC-007]** Define versioned internal ingestion OpenAPI and service auth; dependency T001.
- [ ] **T004 [FR-003, FR-004, AC-001, AC-002]** Implement publication/version upsert and unique constraints; dependencies T002/T003.
- [ ] **T005 [FR-003, NFR-003, AC-001]** Implement safe PDF transfer, storage and SHA-256 verification; dependencies T003/T004.
- [ ] **T006 [FR-006, AC-008]** Implement extraction worker and state updates; dependency T005.
- [ ] **T007 [FR-007, AC-005, AC-006]** Implement reconciler, retries, source_run finalization and checkpoint safety; dependencies T004/T005.
- [ ] **T008 [FR-005, AC-003]** Implement immutable document versioning; dependencies T004/T005.
- [ ] **T009 [FR-002, AC-004]** Adapt one source to ingest without keyword filtering; dependencies T001/T003/T005.
- [ ] **T010 [NFR-001, AC-001]** Docker Compose integration and quickstart; dependency 000 foundation.
- [ ] **T011 [FR-009, NFR-005]** Instrument run-to-object traceability and source health; dependencies T002/T007.
- [ ] **T012 [AC-001..AC-008]** Golden dataset and fault-injection integration tests; dependencies T004–T011.

## Business refinement additions — edition / all / backfill
- [ ] **T013 [FR-011, AC-010]** Model Edition → EditionDocument → DocumentVersion with stable per-source edition and per-edition attachment identities; dependency T001.
- [ ] **T014 [FR-010, AC-012]** Inventory archive depth, pagination, access conditions and earliest accessible date for each of four source adapters; dependency T001.
- [ ] **T015 [FR-010, AC-011]** Design independent LIVE/BACKFILL cursors and historical coverage interval/gap persistence; dependency T002/T014.
- [ ] **T016 [FR-010, AC-009]** Implement bounded, resumable BACKFILL scheduling with live priority and source rate limits; dependency T015.
- [ ] **T017 [FR-011, AC-010]** Implement multi-document manifest ingestion and versioning; dependency T013/T003.
- [ ] **T018 [FR-012, AC-011]** Add historical coverage reporting and gap retry tests; dependency T015/T016.
- [ ] **T019 [AC-009, AC-010, AC-012]** Add golden fixtures for overlapping LIVE/BACKFILL runs and main PDF + supplement; dependency T014/T017.
**Refinement note:** T002/T004/T008 must adopt the revised edition-document-version model; old single-document assumptions are superseded.

## Scope correction — no backfill
- **T014, T015, T016, T018, T019** from the backfill amendment are **CANCELLED / OUT OF SCOPE** (historical archive inventory, historical cursors, backfill scheduler, historical coverage, overlapping-mode tests).
- **T013 and T017 remain** (edition/document/version model).
- [ ] **T020 [FR-010, AC-011]** Define and implement per-source LIVE activation baseline and safe initial checkpoint.
- [ ] **T021 [FR-012, AC-012]** Add tests for first-run boundary, older items visible on source pages and activation-time race conditions.
- [ ] **T022 [AC-009]** Verify repeat LIVE runs are idempotent.
- **T001/T002/T003/T004** must align with LIVE-only API and edition/document model.
