# Roadmap de engenharia — estimativa inicial

Cadência proposta: seis sprints de duas semanas, após Sprint 0. Estimativas dependem de disponibilidade e refinamento.

| Sprint | Tema | Entregáveis | Critério de saída |
|---|---|---|---|
| 0 | Auditoria | Inventário do do-scray, spikes, fontes piloto, golden dataset | Plano de migração validado |
| 1 | Fundação | Monorepo, CI/CD, migrations, identidade, OpenAPI, observabilidade | API e login em homologação |
| 2 | Ingestão | Adaptadores, catálogo, versões, object storage, dedupe | Documento real rastreável |
| 3 | Matching | CRUD, ANY/ALL/EXCLUDE, índices, outbox | Match idempotente |
| 4 | Experiência | Dashboard responsivo, histórico, filtros, alertas e-mail | Jornada E2E |
| 5 | Comercial | Billing, limites, operação, segurança | Beta pago controlado |
| 6 | RC1 | Regressão, carga, runbooks, backup/restore, rollout | Gates aprovados |

## Gates RC1
- Cadastro → regra → detecção → alerta validado.
- Sem vazamento entre organizações.
- Sem duplicação lógica em reprocessamento.
- Precisão e recall medidos em corpus auditado.
- Atraso e falha de fonte visíveis.
- Backup e restauração testados.
- Billing e limites verificados.
- Mobile responsivo.

## Critérios de DoD
Testes pertinentes, contratos versionados, observabilidade, revisão de segurança, documentação e evidências de aceite.

## Marcos de produto (90 dias)
Dias 1–15: entrevistas e landing page; 16–45: MVP técnico; 46–65: beta pago; 66–90: métricas e entrevistas B2B. Executar descoberta em paralelo à engenharia.
