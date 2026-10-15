# Modelo de dados lógico

## Entidades
- User(id, email, passwordHash?, status, createdAt)
- Organization(id, name, type, status)
- Membership(userId, organizationId, role)
- Source(id, name, type, baseUrl, adapterKey, status)
- SourceRun(id, sourceId, startedAt, finishedAt, status, errorCode, correlationId)
- Publication(id, sourceId, externalId, title, publishedAt, canonicalUrl)
- DocumentVersion(id, publicationId, sha256, storageKey, extractedText, version, createdAt)
- Monitor(id, organizationId, name, operator[ANY|ALL], status, createdAt)
- MonitorTerm(id, monitorId, value, kind[INCLUDE|EXCLUDE])
- MonitorSource(monitorId, sourceId)
- Match(id, monitorId, documentVersionId, snippet, matchedTerms, detectedAt)
- Notification(id, matchId, channel, recipient, status, idempotencyKey)
- NotificationAttempt(id, notificationId, providerRef, status, attemptedAt)
- Subscription(id, organizationId, planId, providerRef, status)
- OutboxEvent(id, type, aggregateId, payload, occurredAt, publishedAt)

## Constraints
- UNIQUE(source_id, external_id) quando externalId conhecido; definir identidade determinística alternativa quando ausente.
- UNIQUE(publication_id, sha256)
- UNIQUE(monitor_id, source_id)
- UNIQUE(monitor_id, document_version_id)
- UNIQUE(notification.idempotency_key)
- UNIQUE(user_id, organization_id) em membership.

## Índices e armazenamento
- organization_id + created_at em dados privados; índices por source_id/published_at.
- PostgreSQL full-text search em português com GIN/tsvector; avaliar pg_trgm.
- PDF em object storage; metadados, versões e índices no PostgreSQL.
- Estratégia de retenção para documentos e dados pessoais sujeita a validação jurídica.

## Isolamento
Documentos públicos e fontes são globais. Monitors, Matches, Notifications e Subscriptions pertencem ao tenant via organization_id direto ou relacionamento. Toda leitura e escrita exige escopo de organização; testar IDOR e vazamento cruzado. RLS opcional como defesa adicional.

## Semântica
Mesmo externalId com hash novo gera versão; a identidade da publicação não deve depender somente de URL volátil. Um Match se refere a versão específica. Não enviar alerta histórico automaticamente ao criar regra.
