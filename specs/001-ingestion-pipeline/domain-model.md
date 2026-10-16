# Sprint 0 — Modelo de domínio e linguagem ubíqua

**Status:** DRAFT. Modelo de negócio; não confundir com schema físico PostgreSQL.

## Bounded contexts
1. **Source Registry:** cadastro, habilitação, frequência e capacidade das fontes.
2. **Collection Operations:** execução, observações, checkpoint, falhas e cobertura.
3. **Publication Catalog:** identidade de publicação, edição, anexos e relações.
4. **Document Archive:** versões imutáveis, integridade, retenção e original.
5. **Content Processing:** extração, qualidade e indexabilidade.
6. **Monitoring (futuro):** regras de usuários, correspondências e notificações; não participa da decisão de ingestão.

## Glossário
| Termo | Significado | Não confundir com |
|---|---|---|
| Fonte | Órgão/portal/canal oficial monitorado | Um PDF |
| Adaptador | Implementação técnica que entende uma fonte | Fonte como entidade |
| Execução (SourceRun) | Tentativa delimitada de varredura de uma fonte | Publicação |
| Observação | Evidência de que uma execução encontrou determinado item | Nova versão |
| Publicação | Unidade oficial com identidade estável na fonte | Arquivo binário |
| Edição | Número/data de uma publicação periódica, quando existente | Run |
| Documento | Arquivo associado a publicação | Texto extraído |
| Versão | Conteúdo binário específico de um documento em dado momento | Nova execução |
| Republicação | Nova versão ou nova publicação conforme semântica oficial | Duplicata de download |
| Checkpoint | Posição segura para retomada | Última URL visitada |
| Original | Bytes obtidos da fonte e preservados com hash | Texto normalizado |
| Extração | Transformação de PDF para texto e metadados | Matching |
| Cobertura | Escopo de páginas/edições efetivamente inspecionado | Sucesso HTTP |
| Integridade | Correspondência entre bytes, hash e metadados | Disponibilidade da fonte |

## Agregados candidatos
- **Source**: configurações e regras de elegibilidade.
- **SourceRun**: ciclo de execução, contadores, observações e falhas.
- **Publication**: identidade oficial e associação a documentos.
- **Document**: arquivo lógico e coleção de versões.
- **DocumentVersion**: objeto imutável, hash, extração e disponibilidade.

## Invariantes
- `SourceRun.sourceId` não muda.
- Uma `Publication` pertence a uma `Source`.
- Versões não sobrescrevem bytes anteriores.
- Uma execução pode observar uma publicação existente.
- Uma publicação pode ter zero, um ou vários documentos; documentos podem ter várias versões.
- Uma falha de extração não destrói evidência original.
- Um consumidor de matching não controla quais publicações são arquivadas.

## Eventos de domínio candidatos
`source.run.started.v1`, `source.run.finished.v1`, `publication.observed.v1`, `publication.created.v1`, `document.version.stored.v1`, `document.extraction.completed.v1`, `document.extraction.failed.v1`, `source.coverage.degraded.v1`.

## Context map
Collection Operations → Publication Catalog → Document Archive → Content Processing → Monitoring (futuro).
Integração por contratos explícitos; eventos devem ser idempotentes, versionados e rastreáveis.

## Approved domain refinement
- **Edition** is the principal aggregate, source-scoped and identified by canonical edition key.
- **EditionDocument** is a logical attachment of an edition (MAIN, SUPPLEMENT, ANNEX, OTHER); each can have multiple **DocumentVersion** records.
- **SourceRun.mode** is LIVE or BACKFILL. **SourceCoverage** describes verified historical interval coverage and gaps. **EditionObservation** associates editions with runs without duplication.
- **Backfill** means bounded, resumable historical discovery; not a guarantee that official archives exist.
- The old generic `Publication` term in technical drafts maps to `Edition` for this feature; future act-level modeling remains out of scope.
- **Invariants:** edition identity shared across live/backfill; separate checkpoints; all eligible documents collected regardless of keywords; no destructive replacement of historical versions.

## Current domain decision — no historical backfill
- **Edition** remains the publication aggregate, with EditionDocument and immutable DocumentVersion.
- Only current `SourceRun` and one safe `SourceCheckpoint` per source are needed in Sprint 0.
- `SourceCoverage`, BACKFILL mode and historical coverage intervals are out of scope.
- Add source activation baseline as an explicit domain concept; do not promise data prior to activation.
- The prior backfill refinement is superseded by this section.
