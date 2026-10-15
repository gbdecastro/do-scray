from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from diario_oficial.services.state_store import JsonStateStore
from diario_oficial.services.durable_notifier import DurableNotifier


class HardeningTests(unittest.TestCase):
    def test_strict_state_rejects_corruption_without_overwriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            original = "{bad json"
            path.write_text(original, encoding="utf-8")
            with patch.dict("os.environ", {"DO_SCRAY_STRICT_STATE": "1"}):
                with self.assertRaises(ValueError):
                    JsonStateStore(path).load()
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_strict_state_rejects_invalid_editions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            path.write_text(json.dumps({"editions": []}), encoding="utf-8")
            with patch.dict("os.environ", {"DO_SCRAY_STRICT_STATE": "1"}):
                with self.assertRaises(ValueError):
                    JsonStateStore(path).load()

    def test_legacy_state_mode_keeps_existing_behavior(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            path.write_text("{broken", encoding="utf-8")
            with patch.dict("os.environ", {"DO_SCRAY_STRICT_STATE": "0"}):
                self.assertEqual(JsonStateStore(path).load(), {})

    def test_corrupt_outbox_does_not_construct_sender(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "notifications" / "edicoes.json"
            path.parent.mkdir()
            path.write_text("not json", encoding="utf-8")
            with patch("diario_oficial.services.durable_notifier.TelegramNotifier") as sender:
                with self.assertRaises(json.JSONDecodeError):
                    DurableNotifier(Path(tmp) / "edicoes.json")
                sender.assert_not_called()
