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
- [Legacy audit](../../saas/SPRINT-0-AUDIT.md)
- [Initial ingestion proposal](../../saas/SPRINT-0-INGESTION.md) — early draft, **superseded where it conflicts** with LIVE-only current specs.
- [Docker-first ADR](../../saas/ADR-011-DOCKER-FIRST.md)

## Exit gate
One real pilot edition ingested with integrity, re-run idempotency, safe checkpoint and recovery evidence. No historical completeness claims.
