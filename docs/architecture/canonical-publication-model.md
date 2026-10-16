# Modelo canônico de publicações oficiais

**Status:** PROPOSED — decisão de direção arquitetural aprovada conceitualmente; contratos e migrações aguardam revisão.
**Objetivo:** escalar de quatro para centenas de adaptadores sem multiplicar entidades de negócio.

## Domínio independente da origem
- **Source:** órgão, portal ou feed configurado, com tipo, status e configuração do adaptador.
- **Publication:** unidade lógica oficial observada; tipo `EDITION | NOTICE | CALL | BULLETIN | OTHER`. Não pressupõe edição numerada.
- **PublicationDocument:** arquivo lógico associado à publicação, papel `MAIN | SUPPLEMENT | ANNEX | OTHER`.
- **DocumentVersion:** conteúdo imutável, SHA-256, metadados e localização no object storage.
- **SourceRun:** execução auditável de descoberta/ingestão.
- **SourceCheckpoint:** âncora LIVE de ativação e progresso, definida pelo adaptador e validada pelo motor.
- **PublicationObservation:** observação do item em uma execução, incluindo URL, timestamps e metadados de origem.
- **IngestionAttempt:** tentativa, erro e retry por item.
- **OutboxEvent:** evento persistido para processamento assíncrono.

## Identidade
- Publication: `UNIQUE(source_id, canonical_publication_key)`.
- PublicationDocument: `UNIQUE(publication_id, canonical_document_key)`.
- DocumentVersion: `UNIQUE(publication_document_id, sha256)`.
- A URL é localização/observação, não chave universal.
- `external_id`, número, série, data, título e metadados brutos são opcionais; um adaptador pode derivar uma chave estável documentada se a fonte não fornece ID.
- Alterações no arquivo criam nova versão sem alterar a identidade lógica.

## Contrato dos adaptadores
Cada adaptador implementa `discover(context) -> DiscoveredPublication[]`, `fetch(document) -> bytes/stream` e `checkpoint(context, observations) -> nextCheckpoint`. O retorno é tipado, validado e independente de palavras-chave.
O adaptador declara capacidades: `publicationTypes`, `supportsPagination`, `supportsStableExternalId`, `supportsAttachments`, `checkpointStrategy` e limites de requisição.
O core possui retries, dedupe, storage, observabilidade e regras de avanço de checkpoint; nenhum adaptador grava diretamente nas tabelas de domínio.

## Política de extensibilidade
Adicionar uma fonte deve exigir configuração, implementação do adaptador, fixtures e testes de conformidade, **não** migração de banco ou novos endpoints.
Não criar `BoituvaEdition`, `CismetroCall` ou campos de domínio específicos de município.
Se o esquema canônico não expressar uma necessidade recorrente, propor evolução versionada de contrato, não um `if sourceId` no core.

## Coleta e ativação
**START FROM ZERO:** registrar baseline por fonte e coletar apenas publicações elegíveis desde ativação. Não há backfill no MVP.
Uma janela de sobreposição de descoberta previne perda por corrida; checkpoint só avança após persistência durável.
As regras de snapshot e cursores são próprias de cada adaptador e devem ser testadas.

## Exemplos
| Fonte | Tipo de Publication | Identidade proposta |
|---|---|---|
| Boituva | EDITION | número + série/ano quando aplicável |
| Indaiatuba | EDITION | número + série/ano quando aplicável |
| Sorocaba | EDITION | número + série/ano quando aplicável |
| CISMETRO | CALL / NOTICE | ID oficial do documento, com fallback derivado estável |

**Observação:** tipos e estratégias são hipóteses até validação em fontes reais.

## Consequências
**Benefícios:** engine única, APIs estáveis, onboarding repetível, suporte a fontes heterogêneas.
**Trade-offs:** necessidade de contrato de conformidade, validação de chaves e tratamento de metadados específicos sem poluir o domínio.
**Não objetivos:** backfill, matching de usuários, billing e modelos específicos por município.
