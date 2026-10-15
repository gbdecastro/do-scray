# API REST v1 — proposta de contrato

Prefixo `/api/v1`; OpenAPI 3.1 será fonte de verdade na implementação. Autenticação OIDC/JWT; escopo de organização derivado de autorização, nunca confiado apenas no corpo.

| Método | Rota | Finalidade |
|---|---|---|
| GET | /sources | Catálogo |
| GET | /sources/:id | Saúde da fonte |
| POST | /monitors | Criar regra |
| GET | /monitors | Listar regras |
| GET | /monitors/:id | Detalhar |
| PATCH | /monitors/:id | Editar/pausar |
| DELETE | /monitors/:id | Excluir |
| GET | /monitors/:id/matches | Correspondências |
| GET | /publications | Pesquisar |
| GET | /publications/:id | Evidências |
| GET | /publications/:id/versions | Versões |
| GET | /notifications | Alertas |
| PATCH | /notifications/:id | Marcar como lido |
| GET | /billing/subscription | Plano |
| POST | /billing/checkout | Checkout |

## POST /monitors — exemplo
```json
{
  "name": "Convocações de enfermagem",
  "operator": "ANY",
  "terms": [
    {"value":"convocação","kind":"INCLUDE"},
    {"value":"nomeação","kind":"INCLUDE"},
    {"value":"processo seletivo simplificado","kind":"EXCLUDE"}
  ],
  "sourceIds":["src_01","src_02"],
  "notification":{"email":true,"frequency":"IMMEDIATE"}
}
```

201: `{"id":"mon_01","name":"Convocações de enfermagem","status":"ACTIVE","operator":"ANY","sourceIds":["src_01","src_02"],"createdAt":"2026-10-15T20:30:00Z"}`

## GET /monitors/:id/matches — exemplo
```json
{
  "data":[{
    "id":"match_01","monitorId":"mon_01",
    "publication":{"id":"pub_01","title":"Edição 154","publishedAt":"2026-10-15T10:00:00Z","sourceName":"Diário Municipal","originalUrl":"https://example.org/edicao.pdf"},
    "matchedTerms":["convocação"],
    "snippet":"Convocação dos candidatos aprovados...",
    "detectedAt":"2026-10-15T10:15:00Z"
  }],
  "nextCursor":null
}
```

## Padrões
- Paginação cursor-based; UTC ISO 8601; IDs opacos.
- `Idempotency-Key` em checkout e operações sensíveis.
- RFC 9457 problem+json para erros.
- 403 sem permissão; 404 para recursos cuja existência não pode ser exposta; 409 conflito; 422 validação; 429 limite.
- Rate limits por conta/organização; versionamento explícito.
- Exemplos não representam endpoints implementados.

## Contrato interno de ingestão — pendente de spike
Envelope com sourceId, externalId?, canonicalUrl, publishedAt, title, contentHash, storageKey e correlationId; validar assinatura/autorização e tamanho máximo. Persistência e outbox na mesma transação.
