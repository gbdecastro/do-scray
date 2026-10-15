# Edition library on GitHub Pages

The static dashboard reads edition metadata from the existing `data` branch
state files and shows up to 200 records at a time, searchable by edition,
crawler and result. Up to 3000 recent records are exported.

Links point to the official source URL stored by each crawler; the site
does **not** upload PDFs, serve copies or promise that an external link
remains reachable. Some official links may open a document viewer instead
of a PDF directly.

For privacy, the generator exports only crawler name, edition identifier,
date, checked timestamp, match/no-match flag and allowlisted HTTPS URL.
Matched terms, local PDF paths and document text are never published.
**Important:** edition-level match/no-match status is public on Pages.
Review whether this level of disclosure is acceptable before deployment.
