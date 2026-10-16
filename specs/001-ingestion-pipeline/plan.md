# 001 — Technical implementation plan

**Status:** DRAFT | ADR-012 canonical Publication.

## Existing baseline
Four Python crawlers couple discovery, extraction, keyword matching, JSON state and notifications. Preserve legacy workflows during incremental migration.

## Target
- Python adapters: discovery, stable publication/document keys, capabilities and LIVE checkpoint semantics.
- NestJS API: authenticated runs, manifest registration, upload negotiation and verification.
- PostgreSQL: Source, SourceRun, SourceCheckpoint, Publication, PublicationDocument, DocumentVersion, PublicationObservation, IngestionAttempt, OutboxEvent.
- MinIO/S3: immutable original PDF bytes.
- Workers: extraction, retries, reconciliation and outbox.
- Docker Compose: reproducible local integration.

## Sequence
1. Validate source-specific identities and activation fixtures.
2. Approve canonical adapter contract and OpenAPI.
3. Implement database constraints and storage protocol.
4. Implement safe checkpoints, retries and extraction.
5. Adapt pilot source, then verify second publication type.
6. Execute integration tests and review acceptance evidence.

Guardrails: no Edition-only schema, no per-city branches in engine, no backfill, no keyword filtering at ingestion, no direct adapter DB writes.
