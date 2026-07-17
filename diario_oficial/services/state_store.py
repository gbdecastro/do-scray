from __future__ import annotations

import datetime as dt
import json
import logging
from pathlib import Path


class JsonStateStore:
    def __init__(self, state_file: Path) -> None:
        self.state_file = state_file

    def load(self) -> dict[str, dict[str, object]]:
        if not self.state_file.exists():
            return {}

        try:
            with self.state_file.open("r", encoding="utf-8") as handle:
                raw = json.load(handle)
        except json.JSONDecodeError:
            logging.warning(
                "Arquivo de estado corrompido, iniciando um novo: %s",
                self.state_file,
            )
            return {}

        editions = raw.get("editions", {}) if isinstance(raw, dict) else {}
        if not isinstance(editions, dict):
            return {}
        return editions

    def save(self, editions: dict[str, dict[str, object]]) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "updated_at": dt.datetime.now().isoformat(timespec="seconds"),
            "editions": editions,
        }
        temp_file = self.state_file.with_suffix(".tmp")
        with temp_file.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        temp_file.replace(self.state_file)
