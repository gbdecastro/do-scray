# Maintain Crawlers

1. Identify whether the fix belongs in a shared helper or in a municipality crawler.
2. Update the package modules in `diario_oficial/` first.
3. Keep legacy wrappers aligned with the package entrypoints.
4. Verify the status flow (`match`, `no_match`) and `source_name`.
5. Run a syntax check before finishing.
