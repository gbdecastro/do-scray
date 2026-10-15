import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from diario_oficial.crawlers.cismetro import CismetroCrawler, normalize


class CismetroTests(unittest.TestCase):
    def make_crawler(self, session=None, output_dir=Path("out"), **kwargs):
        return CismetroCrawler(session or Mock(), output_dir, Mock(), Mock(), **kwargs)

    def test_normalization(self):
        self.assertEqual(normalize("BOITUVA  CONVOCAÇÃO"), "boituva convocacao")

    def test_discovery(self):
        session = Mock()
        session.get.return_value.text = '<a href="/docs/convocacao.pdf"><b>Edital</b> de convocação</a>'
        crawler = self.make_crawler(session)
        self.assertEqual(crawler.discover(), [
            ("https://www.cismetro.com.br/docs/convocacao.pdf", "Edital de convocação")
        ])

    def test_discovery_ignores_non_documents(self):
        session = Mock()
        session.get.return_value.text = '<a href="javascript:alert(1)">Bad</a><a href="/sobre">Sobre</a>'
        self.assertEqual(self.make_crawler(session).discover(), [])

    def test_empty_discovery_fails(self):
        session = Mock()
        session.get.return_value.text = '<a href="/">Home</a>'
        with self.assertRaisesRegex(RuntimeError, "Nenhum PDF"):
            self.make_crawler(session).run()

    def test_matching_pdf(self):
        with TemporaryDirectory() as tmp:
            session = Mock()
            session.get.return_value.content = b"%PDF-fake"
            crawler = self.make_crawler(session, Path(tmp), target_terms=("BOITUVA", "TALINE MONTEIRO"))
            with patch("diario_oficial.crawlers.cismetro.extract_pdf_text", return_value="Convocação: Boituva - Taline Monteiro"):
                result = crawler.process_document("abc", "https://example.com/x.pdf", "Edital")
            self.assertEqual(result.status, "match")
            self.assertEqual(result.matched_terms, ["BOITUVA", "TALINE MONTEIRO"])
            self.assertTrue(result.saved_pdf.exists())

    def test_no_match(self):
        with TemporaryDirectory() as tmp:
            session = Mock()
            session.get.return_value.content = b"%PDF-fake"
            crawler = self.make_crawler(session, Path(tmp), target_terms=("TALINE",))
            with patch("diario_oficial.crawlers.cismetro.extract_pdf_text", return_value="Outra cidade"):
                result = crawler.process_document("abc", "https://example.com/x.pdf", "Edital")
            self.assertEqual(result.status, "no_match")
            self.assertIsNone(result.saved_pdf)

    def test_invalid_pdf_is_not_processed(self):
        session = Mock()
        session.get.return_value.content = b"<html>not pdf</html>"
        with self.assertRaisesRegex(ValueError, "nao retornou PDF"):
            self.make_crawler(session).process_document("abc", "https://example.com/x.pdf", "Edital")

    def test_drive_link(self):
        session = Mock()
        session.get.return_value.content = b"%PDF-fake"
        crawler = self.make_crawler(session)
        with patch("diario_oficial.crawlers.cismetro.extract_pdf_text", return_value="Documento"):
            result = crawler.process_document("abc", "https://drive.google.com/file/d/ABC123/view", "Edital")
        self.assertEqual(result.status, "no_match")
        self.assertIn("id=ABC123", session.get.call_args.args[0])

    def test_run_notifies_only_matches(self):
        with TemporaryDirectory() as tmp:
            state = Mock()
            state.load.return_value = {}
            crawler = CismetroCrawler(Mock(), Path(tmp), state, Mock())
            crawler.discover = Mock(return_value=[("https://example.com/x.pdf", "Edital")])
            with patch.object(crawler, "process_document") as process:
                from diario_oficial.models import EditionResult
                process.return_value = EditionResult(
                    number="1", date="", url="https://example.com/x.pdf",
                    source_name="CISMETRO", status="match",
                    matched_terms=["BOITUVA"], saved_pdf=None, checked_at="2026-10-14"
                )
                summary = crawler.run()
            self.assertEqual(summary["match"], 1)
            crawler.notifier.notify.assert_called_once()
            state.save.assert_called_once()


if __name__ == "__main__":
    unittest.main()
