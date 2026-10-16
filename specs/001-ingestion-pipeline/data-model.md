# 001 — Canonical logical data model

**Status:** DRAFT | **ADR-012:** Publication is the aggregate; no historical backfill.

| Entity | Fields | Constraint |
|---|---|---|
| Source | id, code, adapterKey, status, activatedAt, baselineStrategy, baselineReference | UNIQUE(code) |
| SourceRun | id, sourceId, trigger, status, timestamps, counters, correlationId | FK(sourceId) |
| SourceCheckpoint | sourceId, baseline, cursor, lastRunId, updatedAt | UNIQUE(sourceId) |
| Publication | id, sourceId, canonicalPublicationKey, publicationType, officialId?, editionNumber?, series?, publishedAt?, title, officialUrl, rawMetadata? | UNIQUE(sourceId, canonicalPublicationKey) |
| PublicationDocument | id, publicationId, canonicalDocumentKey, role, officialUrl, title? | UNIQUE(publicationId, canonicalDocumentKey) |
| DocumentVersion | id, publicationDocumentId, sha256, sizeBytes, mimeType, objectKey, storageStatus, extractionStatus, extractedText? | UNIQUE(publicationDocumentId, sha256) |
| PublicationObservation | runId, publicationId, observedAt, observedUrl | UNIQUE(runId, publicationId) |
| IngestionAttempt | id, runId, publicationDocumentId?, status, errorCode, attemptedAt | FK(runId) |
| OutboxEvent | id, eventType, aggregateId, payload, occurredAt, publishedAt? | UNIQUE(id) |

## Invariants
- Publication type is EDITION, CALL, NOTICE, BULLETIN or OTHER. Edition is not a separate aggregate.
- One Publication has many PublicationDocuments; one document has immutable versions.
- URL is observation metadata, not universal identity.
- Content hash is computed/verified server-side.
- SourceRun: QUEUED → RUNNING → SUCCEEDED/PARTIAL/FAILED/CANCELLED.
- DocumentVersion: PENDING_UPLOAD → UPLOADED → VERIFIED/ERROR; extraction is tracked separately.
- Advance LIVE checkpoint only after safe durable processing.
- PostgreSQL transaction covers metadata and outbox; storage inconsistencies require reconciliation.
- No SourceCoverage, BACKFILL or historical interval fields.
