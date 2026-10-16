> **Origem:** `docs/saas/BACKLOG.md`. Documento de discovery; specs vigentes prevalecem. Sprint 0 sem backfill.

# Backlog inicial — sujeito a refinement

Story points preliminares; não equivalem a dias. P0 = MVP, P1 = beta comercial, P2 = expansão.

| ID | Épico | História | Prioridade | SP | Dependências |
|---|---|---|---|---:|---|
| US-001 | Identity | Como usuário, criar conta e autenticar | P0 | 5 | Fundação |
| US-002 | Sources | Como usuário, listar fontes e última atualização | P0 | 3 | Catálogo |
| US-003 | Monitoring | Como usuário, criar regra por fontes e palavras-chave | P0 | 8 | US-001, US-002 |
| US-004 | Monitoring | Como usuário, editar/pausar/excluir regra | P0 | 5 | US-003 |
| US-005 | Ingestion | Como sistema, coletar e versionar sem duplicar | P0 | 8 | Source adapters |
| US-006 | Matching | Como sistema, normalizar texto e detectar correspondências | P0 | 8 | US-003, US-005 |
| US-007 | Evidence | Como usuário, ver trecho e documento original | P0 | 5 | US-006 |
| US-008 | Notification | Como usuário, receber alertas por e-mail | P0 | 8 | US-006, outbox |
| US-009 | Operations | Como operador, acompanhar falhas e atrasos | P0 | 5 | US-005 |
| US-010 | Billing | Como assinante, gerenciar plano | P1 | 8 | US-001 |

## Aceite detalhado
### US-003
- Pelo menos um termo INCLUDE e uma fonte.
- Nome obrigatório; operador ANY ou ALL.
- Termos EXCLUDE prevalecem sobre INCLUDE.
- Validação de limites de plano e de organização.
- Criação não dispara histórico automaticamente.
- Uma regra só pode ser acessada por membros autorizados.

### US-005
- Novo documento persiste publicação, arquivo original e versão.
- Mesma identidade canônica e hash não duplica versão.
- Mesmo documento alterado cria nova versão.
- Falhas transitórias têm backoff; falhas permanentes são registradas para reprocessamento.
- Execução mantém métricas e correlation ID.

### US-006
- Normalização Unicode, acentos, caixa e espaços.
- ANY/ALL avaliado no texto inteiro da versão.
- Exclusão tem precedência.
- Match único por monitor e versão; snippet e termos preservados.
- Reprocessamento não duplica correspondência.

### US-008
- Notificação lógica idempotente por match, canal e destinatário.
- Status PENDING/SENT/FAILED/SUPPRESSED e trilha de tentativas.
- Entrega externa pode ser at-least-once; idempotência local não garante exactly-once no provedor.
- E-mail contém origem, trecho e link verificável.

## Backlog de engenharia para Sprint 0
- ENG-001: inventariar crawlers, testes, workflows e dashboard atual.
- ENG-002: mapear acoplamentos com GitHub Actions e Pages.
- ENG-003: estabelecer fixtures de PDFs/HTML e golden datasets.
- ENG-004: selecionar 2–3 fontes piloto com condições de acesso adequadas.
- ENG-005: decidir provedor de autenticação e pagamentos após spike.
- ENG-006: criar threat model de multi-tenancy, ingestão e links externos.
- ENG-007: detalhar contratos de ingestão e esquema de eventos.
- ENG-008: definir baseline de métricas e SLOs realistas.
