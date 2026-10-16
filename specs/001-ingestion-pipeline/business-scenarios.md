# Sprint 0 — Cenários de negócio e decisões esperadas

**Status:** DRAFT. Cada cenário deve virar teste automatizado quando aprovado.

| ID | Dado | Quando | Então |
|---|---|---|---|
| BS-001 | Fonte ativa com 10 edições novas | Coleta termina e arquivos íntegros são persistidos | Run SUCCEEDED, 10 observações e documentos disponíveis |
| BS-002 | Fonte ativa sem novidades | Coleta completa sem novos documentos | Run SUCCEEDED, zero novos, checkpoint coerente |
| BS-003 | Edição já arquivada | Crawler encontra mesmo conteúdo | Nova observação, sem nova versão |
| BS-004 | Edição conhecida com PDF alterado | Novo hash é obtido | Nova versão preservando anterior |
| BS-005 | Documento não contém termo de usuário | Coleta descobre documento | Original e metadados persistidos normalmente |
| BS-006 | Três PDFs encontrados e um falha | Run finaliza | PARTIAL, erro visível e retomada segura |
| BS-007 | Portal indisponível | Crawler não consegue inspecionar escopo | FAILED, não declarar ausência de novidades |
| BS-008 | Upload conclui e processo cai antes do commit | Reconciliador atua | Conclui estado ou registra pendência recuperável |
| BS-009 | PDF íntegro sem texto extraível | Extração é tentada | Original STORED; extração com diagnóstico próprio |
| BS-010 | Fonte é pausada | Scheduler consulta cadastro | Não inicia novas execuções agendadas; histórico permanece |
| BS-011 | Operador força reprocessamento | Mesmas edições são encontradas | Sem duplicatas, com nova execução auditada |
| BS-012 | Fonte remove edição anteriormente publicada | Nova varredura não a encontra | Histórico preservado; ausência não apaga original |
| BS-013 | Fonte retorna paginação incompleta | Run tenta concluir | PARTIAL/FAILED conforme política de cobertura |
| BS-014 | Duas execuções concorrem pela mesma edição | Ambas tentam persistir | Uma identidade lógica e uma versão por hash |
| BS-015 | Publicação possui PDF principal e suplemento | Ambos são descobertos | Dois documentos lógicos associados à publicação |
| BS-016 | Data de publicação difere da coleta | Ingestão registra item | Preserva publishedAt e discoveredAt separadamente |

## Perguntas para o PO / responsável técnico
1. O que significa uma publicação para cada fonte: edição, ato, PDF ou item de uma página?
2. O SaaS arquivará todos os PDFs elegíveis ou haverá limites por tipo/recência?
3. Como classificar retificações e suplementos oficiais?
4. Qual período de histórico será oferecido ao cliente?
5. Qual retenção do PDF e do texto, considerando custos e LGPD?
6. Quando uma fonte é considerada degradada e quem recebe o alerta operacional?
7. Quais são as fontes-piloto e os critérios de sucesso mensuráveis?
8. Precisamos guardar observações individuais ou somente agregados por execução?
9. Qual semântica de cancelamento e reexecução manual?
10. Qual regra de elegibilidade para links HTML sem PDF?

## Additional approved-decision scenarios
| ID | Dado | Quando | Então |
|---|---|---|---|
| BS-017 | Edição histórica não vista na página atual | Backfill percorre arquivo oficial acessível | Edição e documentos são registrados |
| BS-018 | LIVE e BACKFILL encontram mesma edição | Ambos ingerem o mesmo hash | Uma edição, um documento e uma versão; duas observações |
| BS-019 | Edição tem PDF principal e suplemento | Ambos são descobertos | Dois EditionDocument vinculados à mesma Edition |
| BS-020 | Histórico tem lacuna inacessível | Backfill encontra erro de acesso | Intervalo PARTIAL/UNAVAILABLE e motivo, sem falsa completude |
| BS-021 | Backfill é interrompido | Execução é retomada | Retoma do checkpoint seguro, sem perda nem duplicata |
| BS-022 | Backfill extenso está ativo | Surge nova edição atual | LIVE recebe prioridade operacional |
| BS-023 | Suplemento é republicado | Novo hash do mesmo anexo é ingerido | Nova versão do suplemento; PDF principal não muda |
| BS-024 | Fonte não oferece arquivo retroativo | Fonte é avaliada | Capacidade/limitação registrada; nenhuma promessa de cobertura total |

## Scope correction — scenarios
**BS-017, BS-018, BS-020, BS-021, BS-022, BS-024** from the backfill amendment are **OUT OF SCOPE**.
**BS-019 and BS-023** remain applicable to current collection (supplements and new versions).
| ID | Dado | Quando | Então |
|---|---|---|---|
| BS-025 | Fonte é ativada hoje e portal lista edições antigas | Primeiro ciclo começa | Baseline é registrado e edições anteriores são ignoradas sem falso erro |
| BS-026 | Edição é publicada durante ativação | Baseline é estabelecido | Não há lacuna entre ativação e primeira coleta |
| BS-027 | Crawler falha após armazenar parte das edições atuais | Nova execução ocorre | Retoma do checkpoint seguro, sem duplicação |
| BS-028 | Fonte é ativada sem histórico importado | Cliente consulta acervo | Escopo temporal começa na ativação, sem alegar completude retroativa |
