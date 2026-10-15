from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from diario_oficial.web_dashboard.generate import official_url, public_editions, render


class EditionDashboardTests(unittest.TestCase):
    def test_only_official_https_urls(self):
        self.assertEqual(official_url("boituva", "https://www.boituva.sp.gov.br/edicao.pdf"), "https://www.boituva.sp.gov.br/edicao.pdf")
        for url in ("http://www.boituva.sp.gov.br/x", "https://evil.example/x", "javascript:alert(1)", "https://www.boituva.sp.gov.br.evil.example/x", "https://user@www.boituva.sp.gov.br/x"):
            self.assertIsNone(official_url("boituva", url))

    def test_export_does_not_leak_matched_terms_or_saved_files(self):
        with tempfile.TemporaryDirectory() as d:
            state=Path(d)
            (state/"edicoes_lidas_boituva.json").write_text(json.dumps({"editions":{"42":{"number":"42","date":"2026-10-15","url":"https://www.boituva.sp.gov.br/42.pdf","status":"match","checked_at":"2026-10-15T01:00:00","matched_terms":["PRIVATE_PERSON"],"saved_pdf":"/secret/private.pdf"}}}),encoding="utf-8")
            data=public_editions(state)
            self.assertEqual(len(data),1)
            self.assertNotIn("PRIVATE_PERSON",json.dumps(data))
            self.assertNotIn("/secret/private.pdf",json.dumps(data))
            output=state/"index.html"
            render(state/"missing.json",output,state)
            html=output.read_text(encoding="utf-8")
            self.assertIn("Biblioteca de edições",html)
            self.assertNotIn("PRIVATE_PERSON",html)

    def test_invalid_and_non_official_state_ignored(self):
        with tempfile.TemporaryDirectory() as d:
            state=Path(d)
            (state/"edicoes_lidas_sorocaba.json").write_text(json.dumps({"editions":{"a":{"url":"https://example.org/x"}}}))
            (state/"cismetro_convocacoes.json").write_text("{bad")
            self.assertEqual(public_editions(state),[])
