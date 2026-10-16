# Fase 1 — Auditoria estática dos quatro crawlers

**Status:** REVIEW REQUIRED | **Método:** leitura do código da branch `docs/saas-product-discovery`; nenhuma coleta HTTP real, teste ou execução foi realizada.

## Matriz de comportamento observado
| Fonte | Discovery | Chave atual do estado | Paginação | Persistência PDF | Risco |
|---|---|---|---|---|---|
| Boituva | HTML `article` e regex de edição | `edition.number` | Segue links numerados/próxima, varre todas as páginas | Somente se match | Custo histórico involuntário; dedupe por número |
| Indaiatuba | Links e regex `Edição Nº` | `edition.number` | Segue links numerados/próxima, varre todas as páginas | Somente se match | Custo histórico involuntário; dedupe por número |
| Sorocaba | Links PDF e regex de edição | `edition.url` | Apenas página inicial | Somente se match; sem termos registra sem download | URL mutável, falsa completude |
| CISMETRO | Links PDF e Google Drive em página de convocações | SHA-256 truncado da URL | Apenas página indicada | Somente se match | Não é diário por edição; sem agrupamento oficial |

## Evidências no código
- `diario_oficial/crawlers/boituva.py`: `crawl_all_edition_links` percorre paginação; `found[item.number]`; `run` usa `edition.number` no estado; `process_edition` copia PDF apenas se termos encontrados.
- `diario_oficial/crawlers/indaiatuba.py`: fluxo semelhante a Boituva; parser procura `Edição Nº`; persistência condicionada a termos.
- `diario_oficial/crawlers/sorocaba.py`: `crawl_all_edition_links` só lê URL inicial; estado por URL; ramo `if not self.target_terms` registra `no_match` sem PDF.
- `diario_oficial/crawlers/cismetro.py`: `discover` identifica PDFs e links Drive; `key=sha256(url)[:20]`; exige texto extraível antes de concluir; preserva PDF apenas com match.
- `diario_oficial/services/state_store.py`: JSON `editions`, gravação com `replace`; sem transação com objeto armazenado.
- `diario_oficial/runner.py`: integra `JsonStateStore`, notifier e termos; métricas `processed/skipped/match/no_match/errors`.
- `diario_oficial/models/edition.py`: `EditionLink(number,date,text,url)` e `EditionResult` não suportam múltiplos documentos por edição.

## Diagnóstico
1. **Acoplamento de domínio:** descoberta, download, extração, matching, armazenamento e notificação no mesmo crawler.
2. **Perda de original:** arquivos sem match não são retidos.
3. **Identidade heterogênea:** número, URL e hash truncado de URL são usados sem contrato comum.
4. **Sem checkpoint inicial:** varredura completa em Boituva/Indaiatuba contradiz START FROM ZERO.
5. **Sem integridade persistida:** não há checksum de conteúdo e versão imutável no modelo atual.
6. **Sem suporte multi-documento:** `EditionLink` representa um único link.
7. **Falha parcial ambígua:** erros por documento podem ser ignorados sem status PARTIAL confiável.

## Reuso recomendado
**Reutilizar:** parsers HTML, normalização de URLs, download HTTP com timeout, extração PDF, fixtures existentes.
**Refatorar:** `discover` para devolver metadados independentes de palavras-chave; adaptadores por fonte; run/metrics.
**Substituir no SaaS:** JSON como fonte de verdade, dedupe de URL, persistência condicional por match e notificação acoplada.
**Preservar no legado:** runners, notificadores e workflows atuais até piloto SaaS validado.

## Pendências de validação
- Estrutura HTML atual e mudanças de domínio das fontes.
- Se números de edição se repetem por ano/série.
- Se Sorocaba expõe suplementos/retificações com a mesma numeração.
- Se CISMETRO possui agrupamento oficial por edição ou somente documentos.
- Como identificar novas edições em relação ao instante de ativação sem lacunas.
- Quais fixtures/testes existentes cobrem as variações acima.
