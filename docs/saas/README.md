# Radar Público — SaaS de monitoramento de publicações oficiais

**Estado:** Discovery / proposta de RC1. **Estratégia:** B2C concursos primeiro; expansão B2B mediante validação. **Origem:** evolução do projeto do-scray.

## Índice
- [PRD](PRD.md)
- [Histórias e critérios de aceite](BACKLOG.md)
- [Modelo de dados](DATA-MODEL.md)
- [Contratos de API](API-CONTRACTS.md)
- [Arquitetura](ARCHITECTURE.md)
- [Roadmap](ROADMAP.md)
- [ADRs](ADRS.md)
- [Modelo de negócio](BUSINESS.md)

## Princípios
1. Uma fonte é coletada globalmente, não por assinante.
2. Documentos originais e versões são rastreáveis.
3. Monitoramentos e alertas pertencem a organizações isoladas.
4. Matching determinístico antes de classificação por IA.
5. Alertas sempre incluem evidência e transparência de cobertura.
6. Código atual continua operacional até migração incremental.

## Próximo refinamento
Auditar adaptadores e workflows atuais; validar 20 entrevistas; selecionar fontes-piloto; decompor épicos em issues pequenas com dependências, estimativas e critérios de teste.

**Este diretório documenta propostas, não funcionalidades já implementadas.**
