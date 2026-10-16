# Implementation plan — 001 Ingestion

**Status:** DRAFT

## Baseline
Existing `diario_oficial/crawlers/` contains four source adapters; `runner.py` couples JsonStateStore and TelegramNotifier; `state_store.py` and `durable_notifier.py` persist JSON. Legacy workflows use develop/main/data branches. Preserve them during migration.

## Target
Docker Compose: `api` (NestJS), `crawler` (Python), `extractor` (Python), `postgres`, `minio`; Redis optional until asynchronous queue chosen. Terraform optional for external infra.

## Sequence
1. Define canonical publication schema and per-source mapping.
2. Define PostgreSQL migrations and source_run lifecycle.
3. Implement authenticated internal API for manifests and uploads.
4. Store original PDFs, verify SHA-256 and update document state.
5. Persist outbox and extract text in independent worker.
6. Implement checkpoint safety and reconciliation for partial failures.
7. Adapt one pilot crawler behind a feature flag or parallel runner.
8. Validate golden fixtures and end-to-end replays; then expand to remaining sources.

## Data
Source, SourceRun, SourceCheckpoint, Publication, DocumentVersion, IngestionAttempt, OutboxEvent. See `data-model.md`.

## Security
Service-to-service authentication, source allowlist, content validation, maximum file size, object key validation, no public internal endpoints. Respect official site access terms.

## Failure and rollback
DB and object store are not a single transaction; use explicit states and periodic reconciler. Keep old JSON-state path available until parity verified. Never delete old state as part of cutover.

## Verification
Docker Compose integration tests, duplicate/republication fixtures, fault injection around upload/commit, extraction, status metrics and checkpoint invariants.

## Refinement: edition / all / backfill
- Make `Edition` the publication aggregate, `EditionDocument` the logical file attachment, and `DocumentVersion` the immutable bytes/hash. Distinguish edition key from document key.
- Extend adapters with capabilities `supportsBackfill`, historical pagination/date-range discovery, stable edition IDs, and document roles (MAIN, SUPPLEMENT, ANNEX, OTHER).
- Scheduler issues LIVE and BACKFILL runs independently; prioritize LIVE to avoid historical load delaying current publications.
- Persist source-specific historical coverage intervals and gaps, plus independent LIVE cursor and BACKFILL cursor/range.
- Ensure deduplication across modes and concurrent workers with DB unique constraints.
- Implement bounded historical batches, rate limits, backoff and resumable checkpoints. Avoid fetching entire archives in one run.
- Track discovered editions, documents and successful storage separately; a historical interval is complete only when all eligible items are durably accounted for.
- Test multi-document edition, concurrent live/backfill overlap, changed attachment, inaccessible archive interval, and interruption/restart.
