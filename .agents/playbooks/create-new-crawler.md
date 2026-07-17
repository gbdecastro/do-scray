# Create New Crawler

1. Add the municipality-specific crawler under `diario_oficial/crawlers/`.
2. Add the CLI/app entrypoint under `diario_oficial/apps/`.
3. Register the job in `diario_oficial/jobs.py`.
4. Define `BASE_URL`, output directory, log file, and state file.
5. Confirm the crawler emits `EditionResult` with a unique `source_name`.
6. Keep the legacy path, if present, as a wrapper.
