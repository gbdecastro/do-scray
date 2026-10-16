# Fase 1 — Plano de execução do discovery

**Status:** IN PROGRESS — static code audit completed; external source validation and fixture-based tests pending.

## DISC-001 — Inventário de adaptadores
- [x] Ler os quatro crawlers, runner, modelo de edição e state store.
- [x] Registrar diferença entre edições numeradas e documentos CISMETRO.
- [ ] Inspecionar testes e fixtures existentes.
- [ ] Validar HTML/links atuais das quatro fontes com acessos permitidos.
**Evidência:** [source-audit.md](source-audit.md).

## DISC-002 — Identidade canônica
- [x] Propor chave source-scoped, documento e versão por hash.
- [ ] Testar estabilidade da numeração por ano/série.
- [ ] Confirmar suporte a anexos e retificações.
- [ ] Decidir exceção de domínio CISMETRO.
**Evidência:** [identity-and-baseline.md](identity-and-baseline.md).

## DISC-003 — Checkpoint inicial
- [x] Desenhar protocolo de ativação com snapshot e janela de sobreposição.
- [ ] Validar em fixtures corrida durante ativação e falha parcial.
- [ ] Aprovar estratégia por fonte.
**Evidência:** [identity-and-baseline.md](identity-and-baseline.md).

## DISC-004 — Piloto
- [ ] Selecionar fonte piloto após confirmar estabilidade de HTML e numeração.
- [ ] Criar fixtures com edição nova, duplicata, PDF alterado, múltiplos anexos e falha parcial.
- [ ] Aprovar escopo com o responsável de produto.

## Gate para Fase 2
Identidade e baseline de pelo menos uma fonte piloto aprovados, fixtures reproduzíveis, riscos de CISMETRO explicitados, sem necessidade de backfill. Nenhum gate de testes foi executado.
