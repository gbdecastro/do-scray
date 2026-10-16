# 001 — Domain model

**Status:** DRAFT | Canonical aggregate: Publication.

## Contexts
Source Registry owns source, adapter capabilities and activation. Collection Operations owns SourceRun, SourceCheckpoint, observations and failures. Publication Catalog owns Publication, PublicationDocument and DocumentVersion. Document Processing owns extraction and durable events. Matching and notifications are outside Sprint 0.

## Glossary
- Publication: source-scoped official logical item; type EDITION, CALL, NOTICE, BULLETIN or OTHER.
- Edition: one Publication classification, optionally numbered.
- PublicationDocument: logical file with role MAIN, SUPPLEMENT, ANNEX or OTHER.
- DocumentVersion: immutable original bytes identified by SHA-256 within logical document.
- Adapter: source-specific discovery and normalization; never writes directly to domain database.
- Baseline: activation boundary; excludes existing historical items.
- Checkpoint: durable LIVE progress, committed only after safe ingestion.

All eligible accessible documents are collected regardless of keywords. No backfill.
