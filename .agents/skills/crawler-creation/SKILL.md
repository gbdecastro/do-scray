---
name: crawler-creation
description: Use when adding a new municipality crawler to this repository, including scaffolding app, crawler, job registration, and supporting playbook files.
---

# Crawler Creation

Use this skill when introducing a new municipality crawler.

## Scaffold

1. Add a crawler in `diario_oficial/crawlers/`.
2. Add an app entrypoint in `diario_oficial/apps/`.
3. Register the job in `diario_oficial/jobs.py`.
4. Define `BASE_URL`, output directory, log file, and state file.
5. Keep the legacy wrapper path working if the repository already exposes one.

## Implementation Notes

- Reuse `extract_pdf_text` and `JsonStateStore`.
- Keep the crawler-specific parsing logic isolated.
- Prefer config constants in the app module, not inline literals.
- Add a playbook entry when the crawler has non-obvious site quirks.
