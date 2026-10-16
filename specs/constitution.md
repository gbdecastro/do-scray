# Radar Público — Engineering Constitution v1.0

**Status:** Proposed; approval required before implementation.

## Principles
1. **Spec before code:** no new product feature without testable requirements and acceptance scenarios.
2. **Evidence over assumptions:** document observed behavior, tool outputs and executed tests; distinguish proposal from implementation.
3. **Docker-first:** all runnable services packaged in Docker, local stack via Compose; Terraform complementary/optional for external provisioning.
4. **Ingestion before matching:** persist eligible official publications regardless of current subscribers or keywords.
5. **Auditability:** preserve source identity, timestamps, content hash, original document and processing trace.
6. **Idempotency:** repeated crawls and retries must not create duplicate logical publications, versions or alerts.
7. **Failure transparency:** never report complete coverage when collection/extraction failed; expose source health.
8. **Security and privacy:** service authentication, tenant isolation, least privilege, SSRF prevention, secrets hygiene, LGPD and retention controls.
9. **Incremental migration:** preserve legacy operations while proving replacement behavior via fixtures and parallel runs.
10. **Sustainable simplicity:** modular monolith, explicit contracts, automated tests and observability before microservice proliferation.
11. **Responsible collection:** comply with source access policies; prefer official APIs; no bypassing blocks or access controls.
12. **AI accountability:** agents must not fabricate implementation status, benchmark data or test results.

## Governance
Constitution changes require explicit review and version increment. Exceptions must be recorded in a feature spec with rationale, risk and expiry. ADRs document major technical trade-offs.
