---
name: crawler-maintenance
description: Use when updating or debugging existing diary crawlers, shared helpers, Telegram delivery, state handling, or package layout in this repository.
---

# Crawler Maintenance

Use this skill for fixes in `diario_oficial/`, legacy wrappers, and municipality-specific crawlers.

## Workflow

1. Inspect the package source first: `diario_oficial/`.
2. Keep the canonical status values as `match` and `no_match`.
3. Preserve compatibility wrappers at legacy paths unless the user asks to remove them.
4. Reuse shared helpers for PDF text extraction, state, and Telegram delivery.
5. Validate with `py_compile` or the smallest equivalent check.

## Edit Rules

- Prefer changes in `diario_oficial/` over legacy files.
- Keep `source_name` explicit in every `EditionResult`.
- Do not reintroduce duplicate terms, job lists, or notifier logic.
