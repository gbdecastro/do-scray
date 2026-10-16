> **Origem:** `docs/saas/SPRINT-0-AUDIT.md`. Documento de discovery; specs vigentes prevalecem. Sprint 0 sem backfill.

# Sprint 0 — Auditoria técnica inicial do do-scray

**Estado:** análise estática inicial (não foram executados crawlers, testes nem infraestrutura). **Branch:** docs/saas-product-discovery.

## Inventário verificado
- Crawlers: `diario_oficial/crawlers/{cismetro,boituva,indaiatuba,sorocaba}.py`.
- Orquestração: `diario_oficial/jobs.py`, `runner.py`, `apps/run_crawlers.py`.
- PDF: `helpers/pdf_text_extractor.py` com PyMuPDF, tentativa de OCR e fallback pdftotext.
- Estado: `services/state_store.py` usa JSON por fonte e substituição de arquivo temporário.
- Notificação: `services/durable_notifier.py` mantém pending/delivered em JSON e entrega Telegram at-least-once.
- Histórico: `services/run_history.py` mantém histórico limitado em JSON.
- Dashboard: `dashboard.py` Streamlit e `web_dashboard/` gerador estático.
- Docker: Dockerfile python:3.12-slim e Compose crawler + dashboard; bind mounts logs/state/DO.
- Testes: suíte Python cobrindo crawlers, runner, dashboards, modelos, estado e notificações.
- Workflows: persistent-run.yml executa checkout de `develop`, restaura/persiste estado na branch `data`; publish-dashboard.yml usa `main` e publica GitHub Pages com dados da `data`.

## Matriz de decisão
| Item | Ação | Motivo |
|---|---|---|
| Parsers/adaptadores de fontes | REUTILIZAR/REFATORAR | Lógica específica de cada portal já existe |
| Extrator PDF | REUTILIZAR/ENDURECER | Necessita métricas, limites de recursos e fixtures |
| runner.py | REFATORAR | Acopla estado e notificação à coleta |
| JsonStateStore | SUBSTITUIR NO SAAS | JSON local não suporta concorrência e versionamento global adequados |
| DurableNotifier | APROVEITAR CONCEITO | Migrar intenção de envio para outbox transacional e múltiplos destinatários |
| Jobs estáticos | REFATORAR | Fontes devem ser configuráveis e ter scheduler observável |
| Streamlit | MANTER LEGADO | Não serve como interface comercial principal |
| GitHub Pages | MANTER TEMPORARIAMENTE | Não é persistência nem interface privada do SaaS |
| Dockerfile/Compose | EVOLUIR | Incluir imagens multi-stage, healthchecks e serviços locais |
| Testes | PRESERVAR/AMPLIAR | Golden dataset, matching, integração, segurança e E2E |

## Achados arquiteturais
1. Termos globais no crawler: o SaaS deve ingerir documentos independentemente dos termos de qualquer usuário; matching ocorre depois.
2. Estado em Git/JSON: substituir por PostgreSQL e object storage; não depender da branch `data` em produção SaaS.
3. Branches distintas nos workflows (`develop`, `main`, `data`): documentar o fluxo e manter legado estável durante migração.
4. Notificações Telegram: desacoplar coleta de envio, usando evento/outbox e destinatários por organização.
5. OCR: avaliar CPU/memória, timeout, idioma e PDFs problemáticos antes de definir SLO.

## Backlog priorizado Sprint 0
| ID | Prioridade | Atividade | Entregável | Aceite |
|---|---|---|---|---|
| S0-01 | P0 | Auditar fluxos de cada crawler e schemas de saída | Mapa por fonte | Entradas, identificadores, paginação, retries e falhas documentados |
| S0-02 | P0 | Definir contrato de documento normalizado | JSON Schema/OpenAPI interno | Independente de matching/Telegram |
| S0-03 | P0 | Montar golden dataset por fonte | Fixtures + resultados esperados | Testes reproduzíveis offline |
| S0-04 | P0 | Prototipar ingestão independente de termos | Spike isolado | Documento sem match é persistido |
| S0-05 | P0 | Auditar Docker e definir Compose-alvo | Topologia e matriz de ambientes | Local sem serviços cloud obrigatórios |
| S0-06 | P0 | Avaliar persistência e migração de estado | Plano incremental | Reprocessamento sem duplicações |
| S0-07 | P1 | Auditar workflows e estratégia de deploy | Diagrama CI/CD | Legado preservado e rollback descrito |
| S0-08 | P1 | Definir observabilidade por fonte | Contrato de métricas | Último sucesso, latência, erros e atraso |
| S0-09 | P1 | Threat model e LGPD | Checklist de riscos | Isolamento, SSRF, dados pessoais e credenciais |
| S0-10 | P1 | Spike de infraestrutura Terraform | Escopo e gatilhos | Não bloquear execução local com Docker |

## Questões abertas
- Fontes prioritárias do piloto e condições de acesso.
- Política de histórico/backfill e retenção de PDFs.
- Identidade canônica por fonte, especialmente edições republicadas.
- Se os crawlers atuais descartam documentos sem match em todos os caminhos.
- Como autenticar o canal interno de ingestão e limitar arquivos externos.
- Infra de produção: VPS Docker Compose ou serviços gerenciados.
- Testes de falhas 403 e mecanismos legítimos de obtenção de dados.

## Próximos passos
1. Inspecionar profundamente implementações dos quatro crawlers e testes.
2. Produzir contrato de ingestão e fixtures.
3. Fazer spike Docker Compose para pipeline ponta a ponta.
4. Refinar histórias da Sprint 1 com base nas evidências.

Nenhuma mudança de código executável foi feita nesta auditoria.
