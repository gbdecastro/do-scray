# 001 — Business scenarios

**Status:** DRAFT; fixtures and automated evidence pending.

| ID | Given | When | Then |
|---|---|---|---|
| BS-001 | EDITION found | Ingest | Canonical Publication stored |
| BS-002 | CALL found | Ingest | Same API stores CALL |
| BS-003 | Same key, new URL | Rediscover | No duplicate Publication |
| BS-004 | Same document/hash | Replay | No duplicate DocumentVersion |
| BS-005 | Same document, changed bytes | Rediscover | New immutable version |
| BS-006 | Main and supplement | Ingest | Two logical documents |
| BS-007 | No keywords | Collect | All eligible originals retained |
| BS-008 | Crash after upload | Reconcile | Recovery or explicit error |
| BS-009 | Partial failure | Finish run | PARTIAL/FAILED; safe checkpoint |
| BS-010 | Item before activation | Discover | Excluded |
| BS-011 | Item published during activation | First run | Not lost |
| BS-012 | Invalid service credential | Ingest | Rejected |
| BS-013 | New adapter | Conformance | No new schema or endpoint |
| BS-014 | Extraction failure | Process | Original remains available |
