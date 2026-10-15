# ADR-009 — Execution manifests and durable state

## Status
Proposed — Phase 1 of DO Scray v2.

## Context
The current orchestrator runs independent crawler subprocesses, but only writes human-readable logs. Crawlers maintain local JSON state, which does not survive an ephemeral GitHub Actions runner.

## Decision
- Emit one versioned `reports/run.json` manifest per orchestrator invocation, with per-crawler start/end timestamps, duration, exit status and exit code.
- A failed crawler must not prevent the remaining crawlers from running. The orchestrator returns nonzero if any crawler fails or the manifest cannot be written.
- Keep credentials out of the manifest. Do not persist command-line arguments, environment variables or Telegram configuration.
- Preserve existing CLI interfaces and crawler state semantics in this phase.
- In a separate PR, introduce durable state restoration/publishing with serialized GitHub Actions writes; do not treat an artifact or cache as the authoritative state.
- Follow with a dashboard generator reading versioned manifests and historical aggregates.

## Trade-offs
This first version captures process-level outcomes, not document-level counters. Adding structured document results will require an explicit crawler-to-orchestrator reporting contract, rather than parsing logs.

## Acceptance
- `run.json` is generated on success and partial failure.
- All configured crawlers are attempted.
- Unit tests cover serialization and failure isolation.
- Existing CI coverage gate remains at least 90%.
