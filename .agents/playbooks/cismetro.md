# CISMETRO admissions crawler

Source: https://www.cismetro.com.br/convocacao-de-candidatos-para-admissao/

- App: `python -m diario_oficial.apps.cismetro --term "TALINE MONTEIRO" --term "BOITUVA"`
- Run via `diario_oficial.jobs` in the existing orchestrator.
- Reuses PDF text extraction, JSON state and Telegram notifications.
- Discovers direct PDF links and Google Drive file links present in HTML anchors.
- Matches terms independently, case- and accent-insensitively. A match for BOITUVA does not by itself establish a Taline summons.
- Saves only matching PDFs; tracks processed document URLs to avoid duplicate notifications.
- If no links are discovered, raises an error rather than reporting no summons.
- If documents are published through iframe, JavaScript or another download host, update discovery with a tested HTML fixture.
- Verify actual CISMETRO page behavior before relying on this crawler for official monitoring.
