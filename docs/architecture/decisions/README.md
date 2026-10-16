> **Origem:** `docs/saas/ADRS.md`. **Status:** documento histórico de discovery; as especificações SDD vigentes prevalecem. Sprint 0: EDITION + ALL + START FROM ZERO; sem backfill.

# Architecture Decision Records — propostas para aprovação

| ADR | Decisão | Alternativa | Trade-off / revisão |
|---|---|---|---|
| 001 | Monólito modular | Microsserviços | Menor custo operacional; revisar com escala/equipes independentes |
| 002 | Ingestão global, dados privados por organização | Coleta por cliente | Economiza processamento; exige isolamento e dedupe |
| 003 | PostgreSQL + FTS | Elasticsearch/OpenSearch | Menor operação; revisar com volume e relevância |
| 004 | Workers Python separados | Reescrever em TS | Reaproveitamento; contratos entre linguagens |
| 005 | Documentos imutáveis/versionados | Sobrescrever PDFs | Auditoria; maior storage |
| 006 | Matching determinístico | LLM como avaliador | Auditabilidade; menor semântica |
| 007 | Outbox + idempotência | Publicação direta | Consistência; worker adicional |
| 008 | Multi-tenancy lógico | DB por tenant | Custo menor; isolamento exige testes rigorosos |
| 009 | REST/OpenAPI | GraphQL | Contratos simples; endpoints específicos |
| 010 | Object Storage | BLOB no PostgreSQL | Escala de documentos; dependência externa |

Todos os ADRs estão em estado **Proposed**. Cada aprovação futura deve registrar contexto, decisores, data, consequências e gatilhos de revisão.
