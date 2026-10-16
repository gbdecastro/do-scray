# Sprint 0 — Critérios de aceite de negócio

**Status:** DRAFT | **Validação:** pendente de aprovação do PO.

## Gates obrigatórios
- **BA-001 — Cobertura:** um run registra explicitamente fonte, início, término, escopo inspecionado, contagens e status.
- **BA-002 — Integridade:** todo documento disponível possui original recuperável e checksum verificado.
- **BA-003 — Idempotência:** reprocessamento de mesmo item e bytes não multiplica publicações/versões.
- **BA-004 — Versionamento:** republicação com novos bytes mantém histórico anterior.
- **BA-005 — Independência:** ausência de match não impede persistência.
- **BA-006 — Transparência:** falhas parciais e ausência de cobertura são distinguíveis de ausência de novidades.
- **BA-007 — Recuperação:** falhas no meio do pipeline não avançam checkpoint incorretamente.
- **BA-008 — Auditabilidade:** dado um documento, é possível encontrar fonte, execuções em que foi observado, versão e arquivo original.
- **BA-009 — Preservação:** pausa/reprocessamento não elimina evidências históricas.
- **BA-010 — Múltiplos arquivos:** publicação com anexo/suplemento não causa perda por pressuposto de PDF único.

## Evidências requeridas
Fixtures de pelo menos uma fonte piloto, execução Docker local, consultas PostgreSQL, objeto MinIO, logs com correlation ID e testes automatizados de cenários negativos. Nenhum gate foi executado até o momento.

## DoR de negócio
Glossário aprovado, escopo por fonte definido, regras BR-001..BR-024 revisadas, perguntas bloqueantes resolvidas, cenários BS-001..BS-016 priorizados e critérios BA-001..BA-010 aprovados.

## Gates adicionais — decisões aprovadas
- **BA-011 — Edition:** edição é a unidade principal; múltiplos documentos podem ser associados sem colisão.
- **BA-012 — All:** ingestão não depende de keywords e contempla todos os documentos elegíveis acessíveis do escopo.
- **BA-013 — Backfill:** ao menos uma fonte piloto ingere um intervalo histórico por paginação/arquivo oficial com execução auditada.
- **BA-014 — Overlap:** LIVE e BACKFILL simultâneos não duplicam edição, anexo ou versão.
- **BA-015 — Coverage:** intervalos históricos completos, parciais e indisponíveis são distinguíveis com motivo e evidência.
- **BA-016 — Resume:** backfill interrompido retoma sem avançar checkpoint indevidamente.
- **BA-017 — Priority:** backfill limitado não impede processamento atual dentro das metas operacionais definidas.
- **BA-018 — Multi-file:** PDF principal e suplemento persistidos separadamente sob a mesma edição.
**Status:** decisões de produto aprovadas; execução dos gates ainda PENDING.

## Scope correction — acceptance
**BA-013, BA-014, BA-015, BA-016, BA-017** (historical backfill, overlap, historical coverage, historical resume and priority) are **CANCELLED / OUT OF SCOPE**.
**BA-011, BA-012, BA-018** remain (edition, all eligible current documents, multiple files).
- **BA-019 — Activation baseline:** first collection records safe source-specific activation boundary.
- **BA-020 — No historical import:** pre-baseline editions are not imported by default.
- **BA-021 — Resume:** interrupted current collection resumes without losing post-activation editions.
- **BA-022 — Temporal transparency:** product makes no claim of pre-activation coverage.
All tests remain PENDING.
