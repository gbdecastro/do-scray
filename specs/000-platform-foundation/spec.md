# 000 — Platform foundation

**Status:** DRAFT | **Version:** 0.1 | **Priority:** P0 | **Dependencies:** none

## Outcome
Establish reproducible local infrastructure and implementation conventions without disturbing current do-scray execution.

## Scope
- **FR-001:** Local Docker Compose starts PostgreSQL and S3-compatible object storage with persistent volumes.
- **FR-002:** Configuration is documented via safe `.env.example`; no secrets committed.
- **FR-003:** Container images and services expose appropriate health/readiness checks.
- **FR-004:** Developer quickstart and reset/backup guidance exist.
- **NFR-001:** No paid cloud account required for local stack.
- **NFR-002:** Existing crawler workflows and GitHub Pages remain unchanged until replacement is verified.
- **NFR-003:** Terraform optional for future cloud provisioning, not a local dependency.

## Acceptance
- **AC-001:** Given a clean environment, when following documented Compose commands, then local services become healthy.
- **AC-002:** Given a container restart, when volumes persist, then existing test data remains.
- **AC-003:** Given a fresh checkout, when configuring local environment, then no production secret is required.

## Out of scope
Kubernetes, production HA, paid cloud provisioning, commercial frontend and billing.

## Open questions
Production hosting model; database backup strategy; secret provider; image registry.
