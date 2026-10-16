# Registro de consolidação documental — Fase 0

**Status:** CONSOLIDATED — structural migration completed on branch `docs/saas-product-discovery`.
**Scope:** documentation only; no application code or runtime tests changed.

## Resultado
- `docs/README.md` é o índice principal.
- `docs/product/`: visão, requisitos de discovery e modelo de negócio.
- `docs/architecture/`: visão, modelo conceitual, diretrizes de API e ADRs.
- `docs/delivery/`: plano de implementação, roadmap, backlog histórico e Sprint 0.
- `docs/operations/legacy/`: seis runbooks operacionais legados.
- `docs/archive/`: política de arquivamento.
- `specs/`: fonte de verdade para requisitos funcionais, contratos, tarefas e evidências.

## Migração de arquivos
Os 12 arquivos anteriores em `docs/saas/` foram substituídos por redirecionamentos Markdown de compatibilidade para caminhos canônicos. Os seis runbooks anteriores na raiz de `docs/` também redirecionam para `docs/operations/legacy/`. O conteúdo de discovery foi preservado nos novos destinos, identificado como histórico e subordinado às specs.

## Regras de precedência
1. `AGENTS.md` e `specs/constitution.md` (quando aprovados).
2. Specs de feature aprovadas, contratos e critérios de aceite.
3. ADRs aprovadas.
4. Plano de implementação e documentação de arquitetura.
5. Discovery histórico e runbooks legados (somente contexto).

**Sprint 0 atual:** EDITION + ALL + START FROM ZERO. Backfill não faz parte do escopo. Menções antigas a backfill nos documentos de discovery são históricas, não tarefas válidas.

## Validação realizada
- Criação e atualização de destinos confirmadas pelo GitHub.
- Links de navegação dos índices principais revisados e apontados para caminhos canônicos.
- Redirecionamentos de compatibilidade criados nos 18 caminhos antigos.

## Validação pendente
- Links Markdown relativos dos dez principais índices e entradas documentais foram verificados contra o inventário de destinos, sem referências não resolvidas. Ainda falta validação automática em todo o repositório.
- Não houve execução de build, lint, testes ou workflows.
- Links internos herdados dentro dos textos de discovery devem ser verificados pelo CI antes do merge.
- Constituição, regras e specs ainda dependem de revisão/aprovação humana.

## Gate da Fase 0
**Estrutura documental consolidada; revisão automatizada de links e aprovação humana pendentes.** Não afirmar que CI ou documentação completa foram validados sem evidência.
