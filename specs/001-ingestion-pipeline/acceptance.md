# Acceptance — 001 Ingestion

**Status:** NOT RUN. No implementation has been executed.

| ID | Scenario | Expected | Evidence | Status |
|---|---|---|---|---|
| AC-001 | New edition | Run/publication/version + PDF persisted | Pending integration test | PENDING |
| AC-002 | Identical replay | No duplicates | Pending idempotency test | PENDING |
| AC-003 | Modified PDF | New version, old retained | Pending versioning test | PENDING |
| AC-004 | No keyword match | Document still persisted | Pending fixture | PENDING |
| AC-005 | Crash after upload | Reconciled or explicit error | Pending fault injection | PENDING |
| AC-006 | Source failure | Correct run status and checkpoint | Pending failure test | PENDING |
| AC-007 | Unauthenticated request | Rejected | Pending API security test | PENDING |
| AC-008 | Successful extraction | Text/status queryable | Pending worker test | PENDING |

Record commit, Docker versions, commands, output, and defects before changing status to VERIFIED.
