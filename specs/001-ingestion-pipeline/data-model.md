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
