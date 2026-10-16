# Modelo de dados — visão arquitetural

**Status:** DRAFT. [Discovery original](../saas/DATA-MODEL.md).

A modelagem implementável é a da [Feature 001](../../specs/001-ingestion-pipeline/data-model.md): Source, SourceRun, SourceCheckpoint, Edition, EditionDocument, DocumentVersion, EditionObservation, IngestionAttempt e OutboxEvent.

Edição é a unidade principal; pode conter múltiplos documentos, cada qual com versões imutáveis. Coleta somente desde a ativação da fonte; sem backfill.
