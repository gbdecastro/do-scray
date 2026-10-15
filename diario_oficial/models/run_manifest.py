from __future__ import annotations

import dataclasses
import datetime as dt
import json
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class CrawlerRunResult:
    name: str
    status: str
    exit_code: int
    started_at: str
    finished_at: str
    duration_seconds: float


@dataclasses.dataclass(frozen=True)
class RunManifest:
    schema_version: int
    started_at: str
    finished_at: str
    status: str
    crawlers: list[CrawlerRunResult]


def write_manifest(manifest: RunManifest, destination: Path) -> None:
    """Write an atomic, machine-readable execution report."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    try:
        temporary.write_text(
            json.dumps(dataclasses.asdict(manifest), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
