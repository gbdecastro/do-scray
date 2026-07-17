from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class CrawlerJob:
    name: str
    script: Path
    args: list[str] = field(default_factory=list)


CRAWLER_JOBS: list[CrawlerJob] = [
    CrawlerJob(name="boituva", script=Path("diario_oficial/apps/boituva.py")),
    CrawlerJob(name="indaiatuba", script=Path("diario_oficial/apps/indaiatuba.py")),
    CrawlerJob(name="sorocaba", script=Path("diario_oficial/apps/sorocaba.py")),
]
