# Persistent state (Phase 2)

Use the **Persistent crawler run** workflow (manual `workflow_dispatch`) to execute
the crawlers with persistent state. Daily scheduling is intentionally deferred
to Phase 3.

- The workflow restores `state/` from the dedicated `data` branch, or starts
  with an empty state on first execution.
- Crawler execution runs even if a previous run partially failed; its final
  exit status is propagated **after** state persistence.
- A single concurrency group serializes state writes for this workflow.
  Other workflows writing `data` must use the same group.
- The `data` branch is initialized on first run, and updated only when files
  have changed. A rejected non-fast-forward push fails the workflow rather than
  overwriting remote state.
- No PDFs, reports, logs, or Telegram credentials are committed to `data`.

## Notification delivery

When `DO_SCRAY_DURABLE_NOTIFICATIONS=1`, each crawler persists notifications
to `state/notifications/` before attempting Telegram delivery. Failed sends
remain pending and are retried in subsequent runs. Delivered IDs are tracked
separately from processed editions. Existing local execution without this
variable retains its current notifier behavior.

**Guarantee:** at-least-once delivery, not exactly-once. Telegram does not
offer an idempotency key for `sendMessage`; a process crash after the API
accepts a message but before the receipt is persisted can cause a duplicate.

Do not reset or force-push the `data` branch. Protect it from manual edits.
