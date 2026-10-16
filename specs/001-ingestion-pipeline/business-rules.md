# Sprint 0 — Regras de negócio da ingestão

**Status:** DRAFT | **Versão:** 0.1 | **Escopo:** descoberta, execução, publicação, documento, versão, integridade e disponibilidade.

## Objetivo de negócio
Construir um acervo confiável de publicações oficiais que possa ser consultado e monitorado no futuro, independentemente de assinantes, termos de busca ou canais de notificação.

## Atores
- **Operador da plataforma:** cadastra fontes, acompanha execução, intervém em falhas e reprocessa.
- **Coletor automatizado:** descobre publicações em fontes permitidas e entrega metadados/documentos.
- **Serviço de ingestão:** valida, persiste, deduplica, versiona e registra trilha de auditoria.
- **Processador de conteúdo:** extrai texto e sinaliza capacidade de pesquisa.
- **Consumidor futuro (matching):** consulta documentos aptos, sem interferir na coleta.

## Regras normativas propostas
| ID | Regra | Justificativa |
|---|---|---|
| BR-001 | Toda fonte possui identidade estável, tipo, endereço oficial, adaptador e estado operacional | Governança |
| BR-002 | Toda execução possui identidade própria e vínculo com uma fonte, inclusive quando nenhum documento é encontrado | Auditoria |
| BR-003 | Uma execução registra início, fim, origem do disparo, resultados e falhas | Rastreabilidade |
| BR-004 | A ingestão de publicações elegíveis independe de palavras-chave e assinantes | Acervo reutilizável |
| BR-005 | Uma publicação tem chave canônica única no contexto da fonte | Deduplicação |
| BR-006 | Identidade da publicação não é equivalente ao hash de seus bytes; versões diferentes podem representar a mesma publicação | Republicação |
| BR-007 | Um mesmo hash para a mesma publicação não gera nova versão | Idempotência |
| BR-008 | Um hash diferente para a mesma publicação gera versão imutável, preservando a anterior | Evidência histórica |
| BR-009 | Documento original é preservado e vinculado a checksum, tipo, tamanho e localização de armazenamento | Integridade |
| BR-010 | Registro de metadados sem objeto íntegro não é documento disponível | Consistência |
| BR-011 | Extração de texto tem estado independente do armazenamento do PDF | Diagnóstico |
| BR-012 | Falha na extração não apaga o original e não equivale a falha de coleta | Recuperação |
| BR-013 | Uma publicação pode ser encontrada em múltiplas execuções sem gerar duplicação lógica | Histórico |
| BR-014 | Checkpoint só avança quando todos os itens abrangidos por ele têm persistência durável ou política explícita de exceção | Evitar perdas |
| BR-015 | Falhas parciais não podem ser reportadas como cobertura completa | Transparência |
| BR-016 | Reprocessar não pode apagar versões nem evidências anteriores | Auditoria |
| BR-017 | Publicação retirada da fonte não deve ser automaticamente apagada do acervo; retenção depende de política aprovada | Histórico e conformidade |
| BR-018 | Cada documento deve ter origem verificável e link oficial quando disponível | Confiança |
| BR-019 | Datas da fonte, da descoberta e da ingestão são conceitos distintos | Precisão temporal |
| BR-020 | Nenhum resultado futuro de matching pode ser usado como critério para descartar uma publicação | Independência de domínios |
| BR-021 | A fonte pode ser suspensa operacionalmente sem apagar publicações anteriores | Governança |
| BR-022 | Execução manual e agendada obedecem às mesmas regras de integridade e idempotência | Previsibilidade |
| BR-023 | A coleta respeita condições de acesso, frequência e limites legítimos das fontes | Sustentabilidade |
| BR-024 | Toda exceção operacional relevante deve registrar causa, momento e identificador de correlação | Diagnóstico |

## Estados de negócio
### Fonte
ACTIVE: elegível para execução; PAUSED: não agendar; DEGRADED: execução com problemas; DISABLED: desabilitada por decisão operacional. DEGRADED pode ser estado derivado de saúde, e não de configuração — decidir na modelagem.

### Execução
QUEUED → RUNNING → SUCCEEDED | PARTIAL | FAILED | CANCELLED.
- SUCCEEDED: varredura concluída e todos os itens elegíveis conhecidos duravelmente registrados; pode ter zero itens.
- PARTIAL: varredura produziu algum resultado, mas deixou itens/etapas pendentes ou falhou em parte da cobertura.
- FAILED: não houve conclusão confiável da coleta; dados já persistidos não são revertidos.
- CANCELLED: interrompida deliberadamente, sem assumir cobertura completa.

### Documento
DISCOVERED → RECEIVED → STORED → EXTRACTED, com estados de falha/retry por etapa.
- STORED: original íntegro e recuperável.
- EXTRACTED: texto processado; texto vazio pode ser resultado válido somente com diagnóstico explícito.
- SEARCHABLE: capacidade derivada da qualidade/indexação do texto, não sinônimo automático de EXTRACTED.

## Políticas de deduplicação
- Identidade de publicação: `(source_id, canonical_key)`; definir regra canônica por adaptador.
- Identidade de versão: `(publication_id, sha256)`.
- Múltiplas observações da mesma publicação são registradas como evidência de execução, sem criar versões duplicadas.
- Uma edição com vários anexos/documentos exige modelagem explícita de `publication_documents`; não pressupor sempre um PDF por publicação.

## Limites e decisões abertas
- Retenção do original, do texto extraído e dos logs; tratamento de dados pessoais.
- Fonte com edição removida, PDF ilegível ou sem documento.
- Política de histórico e backfill.
- Qualidade mínima para considerar conteúdo pesquisável.
- Critério de conclusão quando fonte apresenta paginação incompleta.
- Política de alertas operacionais e frequência de coleta.
- Regras para publicações com múltiplos anexos, suplementos e retificações.

## Ratified decisions — edition / all / backfill
- **DEC-001 — EDITION:** The edition is the principal business publication. Attachments/supplements belong to the edition; acts within PDFs are not independent publications in Sprint 0.
- **DEC-002 — ALL:** Collect every eligible official edition and its available documents for configured sources, without keyword filtering. Explicitly record inaccessible/missing documents and do not misrepresent coverage.
- **DEC-003 — BACKFILL:** Historical ingestion is part of Sprint 0. Per-source supported date ranges and archive capabilities must be inventoried before declaring historical coverage complete.
- **BR-025:** LIVE and BACKFILL are separate execution modes with independently recoverable progress.
- **BR-026:** An edition may contain multiple logical documents; each has its own immutable version history.
- **BR-027:** Repeated discovery across LIVE and BACKFILL produces observations, not duplicate editions/documents/versions.
- **BR-028:** Historical coverage must track date intervals as COMPLETE, PARTIAL or UNAVAILABLE with reason and last attempt.
- **BR-029:** LIVE ingestion must not be starved by historical backfill; backfill is bounded, resumable and respectful of source limits.
- **BR-030:** "All" means all eligible accessible items within approved source scope, not unlimited bypass or a guarantee of complete archives.
- **BR-031:** Historical coverage is only COMPLETE when every discovered eligible edition/document in that interval has a durable outcome or an explicitly accepted exception.
**Supersession:** any earlier text implying a single PDF per publication or backfill as a future-only enhancement is superseded by these decisions.
