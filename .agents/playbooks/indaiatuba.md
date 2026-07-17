# Indaiatuba Crawler Notes

1. Use the canonical listing URL `https://www.indaiatuba.sp.gov.br/comunicacao-social/imprensa-oficial/edicoes/`.
2. The edition links are direct download endpoints like `/download/72776/`, even when they do not end in `.pdf`.
3. Parse edition text from anchors using the pattern `Edição N.º #### - Publicada em dd/mm/aaaa`.
4. Key state by edition number, not by URL, so repeated downloads of the same edition stay idempotent.
5. Keep output under `DO/Indaiatuba/` and the state file under `state/edicoes_lidas_indaiatuba.json`.
