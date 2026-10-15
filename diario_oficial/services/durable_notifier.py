"""Durable notification outbox; Telegram delivery is at-least-once."""
from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

from .telegram_service import TelegramNotifier
from ..models import EditionResult


class DurableNotifier:
    """Persist intent before sending; retry failed deliveries on later runs.

    A crash between a successful Telegram API call and saving its receipt can
    cause a duplicate. Exactly-once delivery cannot be guaranteed by Telegram.
    """

    def __init__(self, state_file: Path) -> None:
        self.path = state_file.parent / "notifications" / (state_file.stem + ".json")
        self.pending: dict[str, str] = {}
        self.delivered: set[str] = set()
        self._load()
        self.sender = TelegramNotifier()
        self._closed = False

    def _load(self) -> None:
        if not self.path.exists():
            return
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("pending"), dict) or not isinstance(data.get("delivered"), list):
            raise ValueError(f"Invalid notification state: {self.path}")
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in data["pending"].items()):
            raise ValueError(f"Invalid pending notifications: {self.path}")
        if not all(isinstance(key, str) for key in data["delivered"]):
            raise ValueError(f"Invalid delivered notifications: {self.path}")
        self.pending = data["pending"]
        self.delivered = set(data["delivered"])

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        try:
            tmp.write_text(
                json.dumps({"schema_version": 1, "pending": self.pending, "delivered": sorted(self.delivered)}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            tmp.replace(self.path)
        finally:
            tmp.unlink(missing_ok=True)

    @staticmethod
    def key(result: EditionResult) -> str:
        identity = json.dumps([result.source_name, result.url, result.number, result.status, sorted(result.matched_terms)], ensure_ascii=False)
        return hashlib.sha256(identity.encode("utf-8")).hexdigest()

    def notify(self, result: EditionResult) -> None:
        key = self.key(result)
        if key in self.delivered or key in self.pending:
            return
        self.pending[key] = TelegramNotifier._build_message(result)
        self._save()

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            for key, message in list(self.pending.items()):
                if not self.sender._send_message(message):
                    logging.warning("Telegram delivery pending for %s", key)
                    continue
                self.delivered.add(key)
                del self.pending[key]
                self._save()
        finally:
            self.sender.close()
