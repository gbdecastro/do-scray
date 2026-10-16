# ADR-012 — Publication como agregado canônico

**Status:** PROPOSED
**Contexto:** o produto pretende escalar a centenas de crawlers; fontes heterogêneas publicam edições numeradas, convocações e arquivos avulsos. `Edition` como entidade universal força modelos artificiais.
**Decisão:** adotar `Publication → PublicationDocument → DocumentVersion` como modelo central. `EDITION` é um tipo de publicação, não o agregado. Adaptadores normalizam as fontes para um contrato único; o motor não contém lógica específica de órgãos.
**Alternativas:** (a) Edition universal — rejeitada por acoplamento; (b) tabela por fonte — rejeitada por custo de manutenção; (c) Publication canônica — selecionada.
**Trade-offs:** maior abstração e governança de contrato, em troca de onboarding previsível e esquema estável.
**Consequências:** revisar Feature 001, data model, OpenAPI, regras e aceites antes de implementar; adicionar testes de conformidade de adaptadores.
**Revisar se:** novos tipos recorrentes não forem representáveis, identidade não for estável ou o contrato gerar acoplamento específico.
**Referência:** [modelo canônico](../canonical-publication-model.md).
