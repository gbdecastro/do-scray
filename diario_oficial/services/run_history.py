from __future__ import annotations

import json
from pathlib import Path


def append_history(manifest_path: Path, history_path: Path, limit: int = 100) -> bool:
    """Keep bounded execution history, deduplicated by execution timestamp."""
    if not manifest_path.is_file():
        return False
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or not isinstance(manifest.get("crawlers"), list):
        raise ValueError("Invalid run manifest")
    existing = []
    if history_path.is_file():
        existing = json.loads(history_path.read_text(encoding="utf-8"))
        if not isinstance(existing, list):
            raise ValueError("Invalid history")
    existing = [row for row in existing if row.get("started_at") != manifest.get("started_at")]
    existing.append(manifest)
    history_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = history_path.with_suffix(".tmp")
    try:
        tmp.write_text(json.dumps(existing[-limit:], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(history_path)
    finally:
        tmp.unlink(missing_ok=True)
    return True


def read_history(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list):
            return []
        return [row for row in rows if isinstance(row, dict) and isinstance(row.get("crawlers"), list)]
    except (OSError, ValueError):
        return []


def main() -> None:
    append_history(Path("reports/run.json"), Path("state/history/runs.json"))


if __name__ == "__main__":
    main()
