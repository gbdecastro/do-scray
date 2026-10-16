# Logical data model — 001

| Entity | Key fields | Constraint |
|---|---|---|
| Source | id, code, adapterKey, status, lastSuccessAt | UNIQUE(code) |
| SourceRun | id, sourceId, trigger, status, startedAt, finishedAt, counts, correlationId | FK(sourceId) |
| SourceCheckpoint | sourceId, cursor, lastRunId, updatedAt | UNIQUE(sourceId) |
| Publication | id, sourceId, canonicalKey, externalId?, edition?, publishedAt, canonicalUrl | UNIQUE(sourceId, canonicalKey) |
| DocumentVersion | id, publicationId, sha256, versionNumber, objectKey, storageStatus, extractionStatus, extractedText? | UNIQUE(publicationId, sha256) |
| IngestionAttempt | id, runId, canonicalKey, status, errorCode, attemptedAt | FK(runId) |
| OutboxEvent | id, eventType, aggregateId, payload, occurredAt, publishedAt? | UNIQUE(id) |

## State transitions
- SourceRun: QUEUED → RUNNING → SUCCEEDED | PARTIAL | FAILED.
- DocumentVersion: RECEIVED → UPLOADING → STORED → EXTRACTED, with RETRY_PENDING/ERROR.
- Advance checkpoint only after durable persistence of eligible documents.

## Atomicity
PostgreSQL transactions protect relational writes/outbox; object storage requires state transitions and reconciler. A PDF hash change creates a version; same hash is idempotent.

## Refined relational model — approved business choices
The initial `Publication` concept is now **Edition**. Do not implement the old one-publication/one-version shortcut.

| Entity | Key fields | Constraint |
|---|---|---|
| Edition | id, sourceId, canonicalEditionKey, editionNumber?, publishedAt?, officialUrl, title | UNIQUE(sourceId, canonicalEditionKey) |
| EditionDocument | id, editionId, canonicalDocumentKey, role, officialUrl, title? | UNIQUE(editionId, canonicalDocumentKey) |
| DocumentVersion | id, editionDocumentId, sha256, versionNumber, objectKey, storageStatus, extractionStatus | UNIQUE(editionDocumentId, sha256) |
| SourceRun | id, sourceId, mode[LIVE/BACKFILL], requestedFrom?, requestedTo?, status, counters, timestamps | FK(sourceId) |
| SourceCheckpoint | id, sourceId, mode, cursor, rangeFrom?, rangeTo?, updatedAt | UNIQUE(sourceId, mode, rangeFrom, rangeTo) with NULL-safe strategy |
| SourceCoverage | id, sourceId, fromDate, toDate, status[COMPLETE/PARTIAL/UNAVAILABLE], lastRunId, reason? | Index(sourceId, fromDate, toDate) |
| EditionObservation | runId, editionId, observedAt | UNIQUE(runId, editionId) |
| IngestionAttempt | id, runId, editionDocumentId?, errorCode, status | FK(runId) |

**Invariant:** one edition can have many documents; one document can have many immutable versions. LIVE and BACKFILL must share identity constraints but not overwrite each other's progress. Design exclusion/overlap rules for coverage intervals during physical migration.
