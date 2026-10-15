from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from diario_oficial.services.run_history import append_history, read_history


class HistoryTests(unittest.TestCase):
    def test_missing_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(append_history(Path(d) / "missing.json", Path(d) / "history.json"))

    def test_append_deduplicate_and_limit(self):
        with tempfile.TemporaryDirectory() as d:
            manifest, history = Path(d) / "run.json", Path(d) / "state" / "history.json"
            for i in range(3):
                manifest.write_text(json.dumps({"started_at": str(i), "crawlers": []}), encoding="utf-8")
                self.assertTrue(append_history(manifest, history, limit=2))
            self.assertEqual([x["started_at"] for x in read_history(history)], ["1", "2"])
            append_history(manifest, history, limit=2)
            self.assertEqual(len(read_history(history)), 2)

    def test_invalid_manifest_and_corrupt_history(self):
        with tempfile.TemporaryDirectory() as d:
            manifest, history = Path(d) / "run.json", Path(d) / "history.json"
            manifest.write_text('{"bad":true}', encoding="utf-8")
            with self.assertRaises(ValueError):
                append_history(manifest, history)
            history.write_text("not-json", encoding="utf-8")
            self.assertEqual(read_history(history), [])
