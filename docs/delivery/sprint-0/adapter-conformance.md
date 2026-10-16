# Contrato de conformidade para adaptadores

**Status:** DRAFT — casos de teste propostos, não executados.

## Para cada novo crawler
1. Descrever a fonte e a publicação lógica que representa.
2. Fornecer `canonicalPublicationKey` determinística e isolada por `sourceId`.
3. Devolver todos os documentos elegíveis, sem filtrar por termos de usuário.
4. Fornecer `canonicalDocumentKey` estável e classificar o papel do arquivo.
5. Manter URLs e metadados originais como observações, não identidade primária.
6. Declarar capacidade de paginação, anexos, ID oficial e checkpoint.
7. Capturar baseline inicial e garantir janela de sobreposição sem importar histórico.
8. Demonstrar dedupe, republicação (novo SHA-256), retry e falha parcial em fixtures.
9. Não persistir diretamente no banco nem enviar notificações de usuário.
10. Reportar limitações de cobertura e acesso, sem alegar completude indevida.

## Matriz de aceitação
| Caso | Esperado |
|---|---|
| Mesma publicação, URL diferente | Uma Publication |
| Mesmo documento, bytes iguais | Uma DocumentVersion |
| Mesmo documento, bytes alterados | Nova DocumentVersion |
| Publicação com PDF e suplemento | Dois PublicationDocuments |
| Sem palavras-chave | Todos os documentos persistidos |
| Ativação com itens anteriores | Itens anteriores excluídos |
| Publicação durante ativação | Não perdida |
| Falha parcial | Checkpoint não avança além de itens pendentes |
| Documento sem ID oficial | Chave derivada estável com fixture |
| Nova fonte | Sem alteração de schema ou endpoints |

## Resultado do discovery
Boituva, Indaiatuba, Sorocaba e CISMETRO devem implementar o mesmo contrato, com estratégias próprias de descoberta/identidade. Ainda falta validar HTML real e fixtures.
