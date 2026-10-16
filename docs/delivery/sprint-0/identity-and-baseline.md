# Fase 1 — Contrato de identidade e ativação

**Status:** PROPOSED. Não implementar antes de validar fixtures por fonte.

## Identidade canônica
A chave lógica de edição é `(source_id, canonical_edition_key)`; a de documento é `(edition_id, canonical_document_key)`; a versão é `(edition_document_id, sha256(bytes))`. URL de download é localização mutável, não identidade garantida.

| Fonte | Edição proposta | Documento proposto | Validação bloqueante |
|---|---|---|---|
| Boituva | `edition:<numero>` (acrescentar série/ano se necessário) | `main` e anexos por papel/ID oficial | Número globalmente único? |
| Indaiatuba | `edition:<numero>` (série/ano se necessário) | `main` e anexos | Número globalmente único? |
| Sorocaba | `edition:<numero>` + série/ano quando necessário | `main` / suplemento por identificador oficial | URLs/numeração mudam? |
| CISMETRO | **Exceção de domínio:** `document:<official-id>` ou URL canônica como fallback provisório | `main` | Há conceito oficial de edição? Decidir se é fonte DOCUMENT_STREAM, não EDITION |

Não inventar uma edição diária para CISMETRO sem evidência oficial. O agregado comum poderá ser `Publication` com subtipo `EDITION`/`DOCUMENT`, ou CISMETRO poderá ser explicitamente adiado até a revisão de negócio.

## START FROM ZERO — ativação segura
1. Operador ativa a fonte em `activatedAt`; o sistema registra snapshot/âncora de itens já publicados, preferencialmente IDs/edições, não apenas timestamp textual.
2. Enquanto snapshot é capturado, novas edições podem aparecer. A primeira execução deve comparar snapshot e descoberta posterior, mantendo janela de sobreposição para não perder novas edições.
3. Edições anteriores ao baseline ficam fora do escopo; alterações/republicações de edições antigas exigem decisão explícita.
4. Checkpoint só avança após registro durável de todas as edições elegíveis descobertas.
5. Em erro de coleta ou paginação, marcar execução PARTIAL/FAILED, preservar cursor anterior e permitir retry idempotente.
6. Em fontes com listagem apenas da página inicial, estabelecer frequência que minimize perda por rotação de itens; não alegar cobertura garantida sem API/feed ou paginação.

## Baseline por fonte — hipóteses a testar
- **Boituva:** âncora no maior número de edição visível ao ativar, com sobreposição de edições recentes; não executar histórico integral por padrão.
- **Indaiatuba:** mesmo princípio, validar sequência e paginação.
- **Sorocaba:** snapshot do conjunto de identificadores de edições na página atual; não usar somente URL como identidade.
- **CISMETRO:** snapshot do conjunto de links/IDs oficiais; risco de mudança de URL e substituição de conteúdo; exige regra de fonte específica.

## Invariantes de aceite
- Primeira execução não importa automaticamente histórico anterior à ativação.
- Edição publicada durante ativação não se perde.
- Mesmo item observado novamente não duplica registro.
- Documento alterado gera nova versão preservando bytes anteriores.
- Sem termos de busca, documento é igualmente armazenado.
- Não declarar SUCCEEDED se houver falha relevante de cobertura.

## Perguntas bloqueantes
1. CISMETRO permanece no MVP mesmo sem edição numerada?
2. Baseline inicial: snapshot dos itens presentes ou edição mais recente, por fonte?
3. Republicações de edições anteriores à ativação entram ou não?
4. Fontes que publicam várias edições por dia: qual frequência mínima?
