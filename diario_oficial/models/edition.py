from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EditionLink:
    number: str
    date: str
    text: str
    url: str


@dataclass(frozen=True)
class EditionResult:
    number: str
    date: str
    url: str
    source_name: str
    status: str
    matched_terms: list[str]
    saved_pdf: Path | None
    checked_at: str
