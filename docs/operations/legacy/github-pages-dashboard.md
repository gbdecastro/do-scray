# Static operations dashboard (GitHub Pages)

The workflow `Publish operations dashboard` runs after each completed
`Persistent crawler run` (including crawler failures), or manually.

It reads `state/history/runs.json` from the `data` branch and publishes
a static responsive dashboard at
https://gbdecastro.github.io/do-scray/ after GitHub Pages is enabled.

**Repository settings:** Settings → Pages → Build and deployment → Source:
**GitHub Actions**. The `github-pages` environment must permit deployment.

Filters include date range, crawler, status and search. Charts and KPIs
are rendered client-side; no Streamlit server is required.

**Privacy:** the generator allowlists only crawler identifiers, statuses,
timestamps, durations and aggregate counters. It does not publish URLs,
PDFs, raw logs, matching terms, document text, or Telegram credentials.
The published metrics are PUBLIC even if the `data` branch is private.

If the persistent workflow fails before writing history, the page retains
previous history. The published page is not a live status monitor.
