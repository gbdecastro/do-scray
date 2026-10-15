# Arquitetura técnica proposta

## Contexto
Evoluir o crawler Python do do-scray para SaaS de monitoramento, sem quebrar a operação atual.

## Decisão
Monólito modular NestJS + PostgreSQL/Prisma, frontend Next.js responsivo, workers Python independentes, Redis/BullMQ, object storage compatível com S3, OpenAPI, OIDC, OpenTelemetry e GitHub Actions.

## Fluxo
1. Scheduler dispara coleta por fonte; workers Python aplicam adaptadores e registram SourceRun.
2. Documento original armazenado em object storage, com hash e identidade canônica.
3. API interna ingere metadados, versiona e registra evento na outbox em transação.
4. Worker de matching normaliza e avalia regras candidatas (ANY/ALL + EXCLUDE).
5. Match persistido de modo idempotente; outbox solicita notificação.
6. Worker envia e-mail e registra tentativas; UI exibe fonte, trecho e documento.

## Módulos
Identity, Sources, Publications, Monitoring, Notifications, Billing e Operations. API e workers podem ser deployados separadamente sem fragmentar os domínios em microsserviços.

## Eventos
`source.run.completed.v1`, `publication.discovered.v1`, `document.version.created.v1`, `document.extracted.v1`, `monitor.match.created.v1`, `notification.requested.v1`, `notification.delivered.v1`.
Envelope: eventId, schemaVersion, occurredAt, correlationId, aggregateId, payload.

## Matching
Normalizar Unicode, caixa, acentuação e espaços, preservando texto original. ANY/ALL aplicado ao texto completo; EXCLUDE prevalece. Texto muito extenso pode gerar falso positivo; futura evolução por seção/página. Matching determinístico na RC1, sem LLM como fonte de verdade.

## Segurança
Isolamento por organização; validação de ownership; TLS; secrets manager; autorização em ingestão interna; limites de tamanho de PDF e URL; mitigar SSRF; auditoria; retenção e LGPD. URLs de fontes externas não podem ser buscadas arbitrariamente a pedido do usuário.

## Confiabilidade
Retry exponencial, DLQ, deduplicação, idempotência, outbox, backpressure, monitoramento de freshness por fonte, backup/restore testados. Não afirmar cobertura completa quando fonte falhar.

## Testes
Fixtures HTML/PDF, golden dataset, testes unitários de matching, contratos API, concorrência/idempotência, isolamento de tenants, E2E cadastro→regra→documento→match→e-mail, carga e recuperação de falhas.

## Estrutura-alvo (novo monorepo, não criada nesta branch)
```
radar-publico/
  apps/web/
  apps/api/
  apps/matching-worker/
  apps/notification-worker/
  collectors/core/
  collectors/adapters/
  packages/contracts/
  packages/observability/
  infrastructure/docker/
  infrastructure/terraform/
  docs/adr/
```

## Migração
Auditar código atual; extrair adaptadores reutilizáveis; definir contrato de ingestão; manter GitHub Actions/Pages existentes até novo pipeline validado; fazer rollout gradual e rollback documentado.
