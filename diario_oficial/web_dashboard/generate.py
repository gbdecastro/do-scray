"""Publish only non-sensitive, aggregated crawler execution telemetry."""
from __future__ import annotations

import ipaddress
from urllib.parse import urlsplit
import json
import sys
from pathlib import Path

ALLOWED_STATUSES = {"success", "failed", "partial", "error", "skipped", "unknown"}
METRIC_KEYS = ("processed", "skipped", "match", "no_match", "errors")



STATE_FILES = {
    "boituva": "edicoes_lidas_boituva.json",
    "cismetro": "cismetro_convocacoes.json",
    "indaiatuba": "edicoes_lidas_indaiatuba.json",
    "sorocaba": "edicoes_lidas_sorocaba.json",
}
ALLOWED_HOSTS = {
    "boituva": {"www.boituva.sp.gov.br", "boituva.sp.gov.br"},
    "cismetro": {"www.cismetro.com.br", "cismetro.com.br", "drive.google.com"},
    "indaiatuba": {"www.indaiatuba.sp.gov.br", "indaiatuba.sp.gov.br"},
    "sorocaba": {"noticias.sorocaba.sp.gov.br"},
}


def official_url(source: str, raw: object) -> str | None:
    if not isinstance(raw, str) or len(raw) > 2048:
        return None
    try:
        parsed = urlsplit(raw)
        if parsed.scheme != "https" or parsed.username or parsed.password or parsed.port:
            return None
        if parsed.hostname not in ALLOWED_HOSTS[source]:
            return None
    except (ValueError, KeyError):
        return None
    return raw


def public_editions(state_dir: Path) -> list[dict]:
    """Export only edition metadata and official public document links."""
    result = []
    for source, filename in STATE_FILES.items():
        path = state_dir / filename
        if not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        editions = payload.get("editions") if isinstance(payload, dict) else None
        if not isinstance(editions, dict):
            continue
        for item in editions.values():
            if not isinstance(item, dict):
                continue
            url = official_url(source, item.get("url"))
            if not url:
                continue
            status = item.get("status")
            result.append({
                "crawler": source,
                "edition": str(item.get("number") or item.get("title") or "")[:100],
                "date": str(item.get("date") or "")[:40],
                "checked_at": str(item.get("checked_at") or "")[:40],
                "status": status if status in {"match", "no_match"} else "unknown",
                "url": url,
            })
    return sorted(result, key=lambda item: item["checked_at"], reverse=True)[:3000]


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


def render(source: Path, destination: Path, state_dir: Path | None = None) -> None:
    raw = json.loads(source.read_text(encoding="utf-8")) if source.is_file() else []
    payload = json.dumps(public_runs(raw), ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    editions = json.dumps(public_editions(state_dir) if state_dir else [], ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    template = (Path(__file__).parent / "template.html").read_text(encoding="utf-8")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(template.replace("__DASHBOARD_DATA__", payload).replace("__EDITION_DATA__", editions), encoding="utf-8")


def main() -> None:
    render(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]) if len(sys.argv) > 3 else None)


if __name__ == "__main__":
    main()
