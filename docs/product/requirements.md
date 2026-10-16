> Histórico de discovery. Para requisitos executáveis consulte [specs](../../specs/). Sprint 0 não inclui backfill.

# PRD v1.0 — Radar Público

## Problema e público
Informações oficiais estão fragmentadas entre diários, sites e PDFs. Pessoas acompanhando concursos precisam descobrir convocações, nomeações, homologações e prorrogações. Futuramente empresas e associações poderão monitorar licitações e atos administrativos.

## Proposta
Usuário seleciona fontes públicas e define regras por palavras-chave positivas/negativas. O sistema coleta, versiona, extrai texto, encontra correspondências e envia alertas com documento original e trecho.

## Jornada
Criar conta → selecionar fontes → cadastrar regra → receber correspondência → verificar documento → gerenciar alerta.

## Funcionalidades
| ID | Requisito | Prioridade |
|---|---|---|
| RF-01 | Identidade e recuperação de acesso | P0 |
| RF-02 | Catálogo e estado das fontes | P0 |
| RF-03 | Criar monitoramentos com fontes e termos | P0 |
| RF-04 | ANY/ALL e termos de exclusão | P0 |
| RF-05 | Coleta agendada, retry e deduplicação | P0 |
| RF-06 | Extração, normalização e indexação | P0 |
| RF-07 | Matching rastreável | P0 |
| RF-08 | Notificações por e-mail | P0 |
| RF-09 | Histórico e evidências | P0 |
| RF-10 | Editar, pausar e excluir regras | P0 |
| RF-11 | Assinaturas e limites | P1 |
| RF-12 | Saúde dos coletores e auditoria | P0 |
| RF-13 | Compartilhamento em equipes | P2 |
| RF-14 | API pública/webhooks B2B | P2 |

## Requisitos não funcionais — metas, não garantias
- API: disponibilidade mensal 99,5%; p95 de leitura comum <500ms (exclui processamento).
- Matching: até 15 min após ingestão bem-sucedida; notificação até 5 min após match em condições normais.
- Observabilidade por fonte: última execução, último sucesso, atraso, falha e cobertura conhecida.
- Autorização por organização; TLS; dados mínimos; LGPD; idempotência e auditoria.
- Não prometer detecção dentro de prazo fixo contado da publicação original: fontes externas são variáveis.

## Fora da RC1
App nativo, WhatsApp, marketplace de crawlers, API B2B pública, relatórios avançados, IA generativa no matching, backfill automático e monitoramento por ciclo de vida de concurso.

## Métricas experimentais
20 entrevistas; 50 usuários beta; 10–20 pagantes; precisão >=95% e recall >=98% no conjunto manualmente auditado; 3 organizações interessadas em piloto. Não são benchmarks comprovados.

## Riscos
Bloqueios de acesso, alteração de layouts, falsos negativos, churn B2C, CAC, direitos e dados pessoais em publicações. Preferir APIs oficiais e respeitar condições de acesso.
