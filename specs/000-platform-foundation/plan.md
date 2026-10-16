# Plan — 000 Platform foundation

**Status:** DRAFT

- Reuse existing Python Dockerfile and Compose for legacy; avoid breaking crawler/dashboard.
- Add isolated Compose profile or file for future SaaS local stack.
- Local PostgreSQL with volume and readiness probe; MinIO with volume and readiness probe.
- Later add NestJS API, extractor and crawler worker images; Redis only when queue requirements are proven.
- Terraform modules remain optional for external provisioning; no Terraform dependency in local quickstart.
- Validate security posture, backups, restore, resource limits and Docker build reproducibility before production.
- **Rollout:** new services side-by-side, no replacement of legacy workflows.
