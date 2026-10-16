"""Source-agnostic adapter contract, version 1.

Adapters discover *all* eligible publications; matching and persistence belong to
other services. This module deliberately has no source-specific imports.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable

from .canonical import CanonicalPublication, validate_manifest


CONTRACT_VERSION = "1.0"


class CheckpointStrategy(str, Enum):
    MONOTONIC = "MONOTONIC"
    SNAPSHOT = "SNAPSHOT"
    OPAQUE_CURSOR = "OPAQUE_CURSOR"


@dataclass(frozen=True)
class AdapterCapabilities:
    publication_types: tuple[str, ...]
    checkpoint_strategy: CheckpointStrategy
    supports_pagination: bool = False
    supports_attachments: bool = False
    supports_stable_external_id: bool = False
    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class DiscoveryContext:
    source_id: str
    baseline: str | None
    cursor: str | None
    is_activation: bool = False


@dataclass(frozen=True)
class DiscoveryBatch:
    publications: tuple[CanonicalPublication, ...]
    next_cursor: str | None
    complete: bool
    errors: tuple[str, ...] = ()


@runtime_checkable
class SourceAdapter(Protocol):
    @property
    def capabilities(self) -> AdapterCapabilities: ...

    def discover(self, context: DiscoveryContext) -> DiscoveryBatch: ...

    def fetch(self, document_url: str) -> bytes: ...


def validate_batch(context: DiscoveryContext, capabilities: AdapterCapabilities, batch: DiscoveryBatch) -> None:
    """Reject malformed output before it reaches the ingestion engine."""
    if capabilities.contract_version != CONTRACT_VERSION:
        raise ValueError("unsupported adapter contract version")
    if not capabilities.publication_types:
        raise ValueError("adapter must declare publication types")
    if not batch.complete and not batch.errors:
        raise ValueError("incomplete discovery must explain why")
    seen: set[str] = set()
    for publication in batch.publications:
        validate_manifest(publication)
        if publication.source_id != context.source_id:
            raise ValueError("source mismatch")
        if publication.type.value not in capabilities.publication_types:
            raise ValueError("undeclared publication type")
        if publication.key in seen:
            raise ValueError("duplicate publication in discovery batch")
        seen.add(publication.key)
    if not batch.complete and batch.next_cursor != context.cursor:
        raise ValueError("partial discovery must not advance checkpoint")
