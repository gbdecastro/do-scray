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
