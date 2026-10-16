> **Origem:** `docs/saas/ADR-011-DOCKER-FIRST.md`. Documento de discovery; specs vigentes prevalecem. Sprint 0 sem backfill.

# ADR-011 — Docker-first, Terraform-ready

**Status:** Proposed (diretriz solicitada para refinamento na Sprint 0)

## Contexto
O projeto atual já possui Dockerfile Python 3.12-slim e docker-compose.yml com serviços crawler e dashboard Streamlit. O SaaS deverá ser reproduzível localmente, em homologação e produção, com custo e complexidade operacional mínimos.

## Decisão
1. **Docker como padrão obrigatório** de empacotamento de todos os componentes executáveis (API NestJS, web Next.js, crawlers Python, workers).
2. **Docker Compose como padrão inicial** de orquestração local e de ambientes pequenos; configurações por ambiente e profiles quando necessário.
3. **Terraform como opção secundária e complementar** para provisionar recursos externos (VM, rede, DNS, banco gerenciado, object storage, segredos e outros serviços de nuvem). Terraform não substitui Docker nem Compose.
4. **Não adotar Kubernetes na RC1** sem evidência de necessidade operacional.
5. Desenvolvimento local deve funcionar sem conta em provedor de nuvem: PostgreSQL, Redis e MinIO em contêineres.
6. Imagens imutáveis com tags de commit e, em produção, digest; build multi-stage, usuário não-root, healthchecks, limites de recursos e política de restart.
7. Configuração por variáveis e secrets; nunca commitar credenciais. Diferenciar `.env.example` de arquivos secretos.
8. Persistência com volumes e backups/restore testados; PostgreSQL em contêiner na produção apenas mediante avaliação explícita de operação e recuperação.
9. CI/CD executa lint, testes, scan de dependências/imagens, build e publicação; promoção controlada entre ambientes.
10. Observabilidade de logs, métricas, healthchecks e freshness dos coletores desde o MVP.

## Alternativas
- Kubernetes desde o início: rejeitado por custo e operação.
- Infra cloud exclusivamente Terraform: rejeitado por dependência desnecessária de provedor.
- Execução sem contêineres: rejeitada por menor reprodutibilidade.

## Consequências
Mais simplicidade de onboarding e portabilidade; Compose requer procedimentos operacionais para deploy, backups, scaling e alta disponibilidade. Terraform agrega valor quando infraestrutura externa for necessária.

## Critérios de revisão
Escala multi-host, disponibilidade requerida, crescimento operacional, exigências de compliance ou adoção de serviços gerenciados.

## Sprint 0 — tarefas
- INF-001 Inventariar Dockerfile e Compose atuais; identificar gaps de healthcheck, secrets, persistência e imagens.
- INF-002 Definir topologia local API/web/collector/matching/notification/PostgreSQL/Redis/MinIO.
- INF-003 Definir convenção Dockerfile multi-stage e política de tags.
- INF-004 Definir arquivos Compose base e overlays de desenvolvimento/homologação.
- INF-005 Especificar volumes, backups, restore e disaster recovery.
- INF-006 Definir CI de build/test/scan de imagens.
- INF-007 Registrar gatilhos e escopo mínimo de módulos Terraform futuros.
- INF-008 Definir métricas, alertas e healthchecks operacionais.

## Não objetivos desta ADR
Não cria automaticamente infraestrutura nem substitui os arquivos Docker existentes; implementação ocorre nas sprints seguintes.
