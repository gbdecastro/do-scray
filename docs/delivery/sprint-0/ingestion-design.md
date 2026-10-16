> **Origem:** `docs/saas/SPRINT-0-INGESTION.md`. Documento de discovery; specs vigentes prevalecem. Sprint 0 sem backfill.

# Sprint 0 — Contrato e gerenciamento de ingestão de dados

**Status:** Proposed. Objetivo: comprovar pipeline Docker local com PostgreSQL e MinIO, sem matching, billing ou interface comercial.

## Princípio
Crawler descobre e baixa; serviço de ingestão valida e controla persistência; banco guarda metadados/estado; object storage guarda originais. **Ingerir todas as edições elegíveis, não apenas documentos com match.**

## Fluxo de execução
1. Scheduler cria `source_run` (RUNNING), com `run_id`, `source_id`, `started_at`, `trigger` e `correlation_id`.
2. Worker Python coleta edições e envia manifesto de cada publicação ao serviço interno autenticado.
3. API valida origem permitida, metadados e chave de idempotência; registra publicação e versão pendente.
4. Arquivo original é transferido ao storage por fluxo controlado, com limites de tamanho, MIME verificado e hash SHA-256. Nunca confiar em URL arbitrária fornecida por cliente.
5. Após confirmação de existência do objeto e hash, transação no PostgreSQL marca versão `STORED` e registra evento de extração na outbox.
6. Worker de extração lê o objeto, produz texto/diagnóstico e atualiza `extraction_status`; falhas são retentáveis.
7. Worker reporta contagens; scheduler finaliza `source_run` como SUCCEEDED/PARTIAL/FAILED e registra checkpoint/cursor.
8. Reprocessar mesmo documento/hash é no-op; mesmo documento com hash novo cria nova versão.

## Modelo mínimo
- `sources`: id, code, name, adapter_key, status, last_success_at, expected_frequency.
- `source_runs`: id, source_id, trigger, status, started_at, finished_at, discovered_count, stored_count, skipped_count, failed_count, error_code, correlation_id.
- `publications`: id, source_id, external_id_nullable, canonical_key, title, edition, published_at, canonical_url, created_at; UNIQUE(source_id, canonical_key).
- `document_versions`: id, publication_id, sha256, version_number, object_key, bytes, mime_type, storage_status, extraction_status, extracted_text_nullable, created_at; UNIQUE(publication_id, sha256).
- `source_checkpoints`: source_id, cursor, updated_at, last_run_id.
- `ingestion_attempts`: id, run_id, publication_key, status, error_code, attempted_at.
- `outbox_events`: id, event_type, aggregate_id, payload, occurred_at, published_at.

## Estados
- SourceRun: QUEUED → RUNNING → SUCCEEDED | PARTIAL | FAILED.
- DocumentVersion: RECEIVED → UPLOADING → STORED → EXTRACTED; ERROR e RETRY_PENDING para falhas.
- Nunca declarar sucesso se PDF ou metadados estiverem ausentes; publicar saúde por fonte.

## Idempotência e consistência
- Chave canônica por fonte: preferir identificador oficial/edição; fallback determinístico por URL normalizada e metadados.
- Hash SHA-256 dos bytes para detectar versões.
- Constraints UNIQUE e UPSERT transacional evitam duplicatas sob concorrência.
- PostgreSQL e object storage não participam da mesma transação: usar máquina de estados, objeto temporário, promoção/verificação e reconciliador de pendências/órfãos.
- Checkpoint só avança depois de persistência durável dos itens elegíveis; garantir retomada em falhas.
- Não enviar PDF em JSON/base64; streaming multipart interno ou upload com URL assinada curta e validação de checksum.
- Outbox somente após versão pronta, com consumer idempotente.

## API interna proposta
- `POST /internal/v1/source-runs`: abre execução.
- `POST /internal/v1/source-runs/{runId}/publications`: upsert de manifesto; retorna publicationId, versionId, instrução de upload se necessário.
- `POST /internal/v1/document-versions/{versionId}/complete`: confirma upload e hash.
- `POST /internal/v1/source-runs/{runId}/finish`: fecha execução com contagens e erros.
- `GET /internal/v1/source-runs/{runId}`: status e reconciliação.
A autenticação é de serviço para serviço, com autorização por source_id. Não expor endpoints internos à internet pública.

## Payload de manifesto — exemplo
```json
{
  "sourceId": "src_boituva",
  "externalId": "2026-154",
  "canonicalKey": "edicao-2026-154",
  "title": "Diário Oficial - Edição 154",
  "edition": "154",
  "publishedAt": "2026-10-15T10:00:00Z",
  "canonicalUrl": "https://example.org/edicao.pdf",
  "document": {
    "sha256": "sha256-hex-real-calculated-by-worker",
    "sizeBytes": 123456,
    "mimeType": "application/pdf"
  }
}
```
Exemplo ilustrativo; o hash real será hexadecimal de 64 caracteres e validado no backend.

## Topologia Docker local
- `api`: NestJS ingestão.
- `crawler`: worker Python.
- `postgres`: metadados e estado (volume).
- `minio`: documentos (volume).
- `extractor`: worker Python de extração.
- `redis`: opcional nesta prova; adicionar se scheduler/filas demandarem.
Terraform não é necessário no fluxo local; opcional no provisionamento cloud.

## Critérios de aceite Sprint 0
1. `docker compose up --build` sobe componentes sem conta cloud.
2. Uma edição real de fonte piloto gera source_run, publication e document_version.
3. PDF original recuperável do MinIO, hash verificado.
4. Texto extraído e status persistidos independentemente de palavras-chave.
5. Reexecução sem alterações não duplica registros.
6. Documento republicado com bytes novos cria nova versão.
7. Interrupção após upload/antes do commit é recuperável por reconciliação.
8. Falha de fonte não marca execução como sucesso e não perde checkpoint.
9. Logs e métricas permitem rastrear run_id → publication → version → objeto.
10. Testes de integração cobrem idempotência, falhas e isolamento de endpoints internos.

## Perguntas para refinamento
- Identidade de edição e URL canônica em cada crawler.
- Política de retenção e limites de PDF.
- Volume esperado por fonte e periodicidade.
- Preferência entre multipart e URL assinada.
- Banco gerenciado ou Docker com backup para produção.

## Não objetivos
Não implementar billing, usuários finais, notificações ou matching nesta etapa.
