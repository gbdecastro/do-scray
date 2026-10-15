from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from diario_oficial.web_dashboard.generate import public_runs, render


class PublicDashboardTests(unittest.TestCase):
    def test_allowlist_excludes_sensitive_data(self):
        payload = [{"started_at":"2026-10-15T01:00:00Z","status":"partial","secret":"DO_NOT_PUBLISH","crawlers":[{"name":"boituva","status":"failed","url":"https://private.example","matched_terms":["PRIVATE_NAME"],"metrics":{"processed":3,"match":1,"private":42}},{"name":"unapproved","status":"success"}]}]
        result = public_runs(payload)
        data = json.dumps(result)
        self.assertNotIn("DO_NOT_PUBLISH", data)
        self.assertNotIn("PRIVATE_NAME", data)
        self.assertNotIn("private.example", data)
        self.assertNotIn("unapproved", data)
        self.assertEqual(result[0]["crawlers"][0]["metrics"]["processed"], 3)

    def test_render_escapes_html_payload(self):
        with tempfile.TemporaryDirectory() as d:
            source, dest = Path(d)/"history.json", Path(d)/"site"/"index.html"
            source.write_text(json.dumps([{"started_at":"</script><script>alert(1)</script>","status":"success","crawlers":[]}]))
            render(source, dest)
            content=dest.read_text()
            self.assertNotIn("</script><script>alert(1)", content)
            self.assertIn("Visão geral", content)

    def test_empty_history(self):
        with tempfile.TemporaryDirectory() as d:
            dest=Path(d)/"index.html"
            render(Path(d)/"missing.json",dest)
            self.assertIn("[]",dest.read_text())

    def test_invalid_records_and_metrics(self):
        data=public_runs([None,{"crawlers":[{"name":"cismetro","status":"weird","metrics":{"processed":-1,"match":"abc"}}]}])
        self.assertEqual(data[0]["crawlers"][0]["status"],"unknown")
        self.assertEqual(data[0]["crawlers"][0]["metrics"]["processed"],0)
