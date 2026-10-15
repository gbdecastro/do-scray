# Phase 3 — Automated execution

The `Persistent crawler run` workflow executes every day at **19:00 in
Brasília** using `0 22 * * *` (22:00 UTC), and supports manual
`workflow_dispatch` from the Actions tab.

## Setup

1. Configure repository secrets `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID`.
   If the `production` environment exists, ensure the workflow can access
   those secrets there, and configure approvals as appropriate.
2. Ensure Actions has permission to write to the `data` branch. Repository
   rules or branch protection must permit the GitHub Actions bot to update it.
3. Manually run `Persistent crawler run` once on the default branch and
   verify that `data` contains `state/`, that a second run skips processed
   editions, and that failed Telegram sends remain pending for retry.
4. Inspect run logs for unexpected failures; never commit credentials or PDFs.

## Operational constraints

- The workflow is serialized by `do-scray-persistent-state` concurrency,
  with no cancellation of an in-progress run.
- The job times out after 45 minutes.
- State is persisted even when crawlers return nonzero; the run then reports
  failure through its final step.
- Secrets are required; missing values fail before crawling.
- Scheduled workflows run from GitHub's **default branch**. Merge the PR
  through the repository's release flow into `main` to activate scheduling.
- GitHub Actions cron is best effort; execution may be delayed or occasionally
  dropped. The crawler's persisted state makes the next successful run safe
  to resume.
- Brasília currently observes UTC-03:00 without daylight saving. If its
  legal timezone rules change, update the UTC cron expression.
