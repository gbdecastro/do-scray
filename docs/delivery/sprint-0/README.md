# Sprint 0 — Data ingestion foundation

**Status:** DRAFT | **Business decisions:** EDITION + ALL + START FROM ZERO.

## Objective
An auditable source run produces persistent editions, logical attachments, immutable document versions, original PDFs and extraction outcomes. A source begins at an explicit activation baseline. No backfill.

## Read in order
1. [Implementation plan](../implementation-plan.md)
2. [Business rules](../../../specs/001-ingestion-pipeline/business-rules.md)
3. [Domain model](../../../specs/001-ingestion-pipeline/domain-model.md)
4. [Business scenarios](../../../specs/001-ingestion-pipeline/business-scenarios.md)
5. [Business acceptance](../../../specs/001-ingestion-pipeline/business-acceptance.md)
6. [Technical spec](../../../specs/001-ingestion-pipeline/spec.md)
7. [OpenAPI](../../../specs/001-ingestion-pipeline/contracts/ingestion.openapi.yaml)
8. [Tasks](../../../specs/001-ingestion-pipeline/tasks.md)
9. [Acceptance evidence](../../../specs/001-ingestion-pipeline/acceptance.md)

## Existing research
- [Legacy audit](legacy-audit.md)
- [Initial ingestion proposal](ingestion-design.md) — early draft, **superseded where it conflicts** with LIVE-only current specs.
- [Docker-first ADR](../../architecture/decisions/ADR-011-docker-first.md)

## Exit gate
One real pilot edition ingested with integrity, re-run idempotency, safe checkpoint and recovery evidence. No historical completeness claims.

## Fase 1 — Discovery técnico
- [Plano e checklist](discovery-plan.md)
- [Auditoria estática dos quatro crawlers](source-audit.md)
- [Identidade e baseline de ativação](identity-and-baseline.md)

**Estado:** auditoria estática realizada; validação externa e fixtures pendentes. CISMETRO pode exigir exceção ao agregado Edition.

## Escalabilidade dos adaptadores
- [Contrato de conformidade para novos crawlers](adapter-conformance.md)
- [Modelo canônico de publicação](../../architecture/canonical-publication-model.md)

**Revisão necessária:** documentos SDD anteriores usam `Edition` como agregado. A ADR-012 propõe substituí-lo por `Publication`; não implementar o contrato antigo antes da reconciliação.
