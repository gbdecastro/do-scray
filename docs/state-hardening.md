# Phase 5 — State safety

Persistent GitHub Actions runs set `DO_SCRAY_STRICT_STATE=1`.

If an edition-state JSON file is corrupted or its `editions` payload is not
a mapping, the crawler fails instead of silently treating it as a fresh state.
This prevents reprocessing and repeated notifications caused by resetting a
corrupted state file. The existing permissive behavior remains available for
local executions without the strict flag.

The durable outbox now validates persisted notification state before creating
its Telegram sender, preventing a background worker from being started when
loading the outbox fails.

On state corruption, inspect and restore the relevant file from a known-good
commit on the `data` branch. Do not delete the file or force a reset without
reviewing the consequences for deduplication and notification delivery.

HTTP 403 failures from upstream portals remain an independent operational issue.
