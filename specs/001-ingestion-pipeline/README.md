# Feature 001 — Ingestão e governança de dados

**Status:** DRAFT. Esta é a primeira feature SDD da Sprint 0.

## Leia nesta ordem
1. [Regras de negócio](business-rules.md)
2. [Modelo de domínio e glossário](domain-model.md)
3. [Cenários de negócio](business-scenarios.md)
4. [Aceite de negócio](business-acceptance.md)
5. [Especificação funcional](spec.md)
6. [Plano técnico](plan.md)
7. [Modelo lógico de persistência](data-model.md)
8. [Contrato de API](contracts/ingestion.openapi.yaml)
9. [Backlog técnico](tasks.md)
10. [Evidências de execução](acceptance.md)

## Separação de responsabilidades
- Documentos de negócio definem o comportamento esperado, independentemente da stack.
- Documentos técnicos definem como atender o comportamento com Docker, PostgreSQL, MinIO e serviços.
- Nenhum documento DRAFT autoriza implementação automática; aprovar primeiro regras, cenários e contratos.

## Fonte de contexto
`docs/saas/SPRINT-0-AUDIT.md` e `docs/saas/SPRINT-0-INGESTION.md`.
