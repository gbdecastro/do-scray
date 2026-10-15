# Phase 4 — Execution history and dashboard

The persistent workflow appends `reports/run.json` to `state/history/runs.json`
after crawler execution, even when some crawlers fail. The history is capped
at 100 runs and deduplicated by start timestamp. It is committed to the `data`
branch alongside crawler state.

The existing Streamlit dashboard now includes an **Execuções** tab with latest
run, per-crawler metrics and aggregated historical counts.

For local viewing of GitHub Actions history, first restore the `state/`
directory from the `data` branch, then run `docker compose up dashboard`.
The dashboard does not fetch private GitHub data or host a public endpoint.
