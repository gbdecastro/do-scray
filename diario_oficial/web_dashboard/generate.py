"""Publish only non-sensitive, aggregated crawler execution telemetry."""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ALLOWED_STATUSES = {"success", "failed", "partial", "error", "skipped", "unknown"}
METRIC_KEYS = ("processed", "skipped", "match", "no_match", "errors")


def public_runs(raw: object) -> list[dict]:
    """Allowlist fields to avoid exposing source URLs, matched terms or PII."""
    if not isinstance(raw, list):
        return []
    cleaned = []
    for item in raw[-100:]:
        if not isinstance(item, dict) or not isinstance(item.get("crawlers"), list):
            continue
        crawlers = []
        for crawler in item["crawlers"]:
            if not isinstance(crawler, dict):
                continue
            name = str(crawler.get("name", "unknown"))[:40]
            if name not in {"cismetro", "boituva", "indaiatuba", "sorocaba"}:
                continue
            metrics = crawler.get("metrics") or {}
            if not isinstance(metrics, dict):
                metrics = {}
            crawlers.append({
                "name": name,
                "status": str(crawler.get("status", "unknown")) if crawler.get("status") in ALLOWED_STATUSES else "unknown",
                "duration_seconds": _number(crawler.get("duration_seconds")),
                "metrics": {key: _number(metrics.get(key)) for key in METRIC_KEYS},
            })
        cleaned.append({
            "started_at": str(item.get("started_at", ""))[:40],
            "finished_at": str(item.get("finished_at", ""))[:40],
            "status": str(item.get("status", "unknown")) if item.get("status") in ALLOWED_STATUSES else "unknown",
            "crawlers": crawlers,
        })
    return cleaned


def _number(value: object) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 0
    return max(0, min(value, 10_000_000))


def render(source: Path, destination: Path) -> None:
    raw = json.loads(source.read_text(encoding="utf-8")) if source.is_file() else []
    payload = json.dumps(public_runs(raw), ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    template = (Path(__file__).parent / "template.html").read_text(encoding="utf-8")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(template.replace("__DASHBOARD_DATA__", payload), encoding="utf-8")


def main() -> None:
    render(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
