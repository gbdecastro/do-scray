from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

from diario_oficial.crawlers import BoituvaCrawler, SorocabaCrawler
from diario_oficial.models import EditionLink, EditionResult
from tests.support import FakeResponse, FakeSession, MemoryNotifier, MemoryStateStore


class BoituvaCrawlerTest(unittest.TestCase):
    def test_parsers_and_helpers(self) -> None:
        from diario_oficial.crawlers.boituva import AnchorParser, EditionCardParser

        anchor_parser = AnchorParser()
        anchor_parser.feed('<a href="/link">Hello <b>World</b></a>')
        self.assertEqual(anchor_parser.anchors, [("Hello World", "/link")])

        card_parser = EditionCardParser()
        card_parser.feed(
            """
            <article>
              <small class="list-date"> 01/02/2024 </small>
              <a href="/pdf/123"> Diário Oficial - Edição 123 </a>
            </article>
            """
        )
        self.assertEqual(card_parser.anchors, [("01/02/2024", "Diário Oficial - Edição 123", "/pdf/123")])

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "out"
            response = FakeResponse(chunks=[b"a", b"b"])
            session = FakeSession({("https://example.com/file.pdf", True): response})
            crawler = BoituvaCrawler(
                session=session,
                output_dir=output_dir,
                state_store=MemoryStateStore(),
                notifier=MemoryNotifier(),
            )

            destination = Path(tmpdir) / "download.pdf"
            crawler.download_file("https://example.com/file.pdf", destination)
            self.assertEqual(destination.read_bytes(), b"ab")

        self.assertEqual(BoituvaCrawler.normalize_text("ÁBÇ"), "ábç")
        self.assertEqual(BoituvaCrawler.safe_filename("a/b c"), "a_b_c")
        self.assertEqual(BoituvaCrawler.safe_filename("???"), "arquivo")
        self.assertEqual(BoituvaCrawler.safe_filename("file.pdf"), "file.pdf")
        self.assertEqual(
            BoituvaCrawler(
                session=FakeSession(),
                output_dir=Path("."),
                state_store=MemoryStateStore(),
                notifier=MemoryNotifier(),
            ).guess_pdf_name("https://example.com/download", "12"),
            "edicao_12.pdf",
        )
        self.assertEqual(
            BoituvaCrawler(
                session=FakeSession(),
                output_dir=Path("."),
                state_store=MemoryStateStore(),
                notifier=MemoryNotifier(),
            ).guess_pdf_name("https://example.com/edicao_12.pdf", "12"),
            "edicao_12.pdf",
        )

    def test_extract_links_and_pagination(self) -> None:
        crawler = BoituvaCrawler(
            session=FakeSession(),
            output_dir=Path("."),
            state_store=MemoryStateStore(),
            notifier=MemoryNotifier(),
        )

        html = """
        <article>
          <small class="list-date"> 01/02/2024 </small>
          <a href="/pdf/123"> Diário Oficial - Edição 123 </a>
        </article>
        <article>
          <small class="list-date"> 01/02/2024 </small>
          <a href="/pdf/ignored.pdf"> Sem edição </a>
        </article>
        <a href="?page=2">Próxima</a>
        <a href="/page/3">3</a>
        <a href="/page?p=4">ignored text</a>
        """
        editions = crawler.extract_edition_links(html, "https://example.com/base/")
        self.assertEqual(editions[0].url, "https://example.com/pdf/123")
        self.assertEqual(editions[0].number, "123")

        links = crawler.extract_pagination_links(html, "https://example.com/base/")
        self.assertIn("https://example.com/base/?page=2", links)
        self.assertIn("https://example.com/page/3", links)
        self.assertIn("https://example.com/page?p=4", links)

    def test_crawl_all_edition_links(self) -> None:
        responses = {
            ("https://example.com/page1", False): FakeResponse(
                text="""
                <article>
                  <small class="list-date"> 01/02/2024 </small>
                  <a href="/pdf/123"> Diário Oficial - Edição 123 </a>
                </article>
                <a href="/page2">Próxima</a>
                """
            ),
            ("https://example.com/page2", False): FakeResponse(
                text="""
                <article>
                  <small class="list-date"> 02/02/2024 </small>
                  <a href="/pdf/124"> Diário Oficial - Edição 124 </a>
                </article>
                <a href="/page1">1</a>
                """
            ),
        }
        crawler = BoituvaCrawler(
            session=FakeSession(responses),
            output_dir=Path("."),
            state_store=MemoryStateStore(),
            notifier=MemoryNotifier(),
        )

        editions = crawler.crawl_all_edition_links("https://example.com/page1")
        self.assertEqual([item.number for item in editions], ["124", "123"])

    def test_process_and_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "out"
            state_store = MemoryStateStore(initial_state={"1": {"status": "match"}})
            notifier = MemoryNotifier()
            crawler = BoituvaCrawler(
                session=FakeSession(),
                output_dir=output_dir,
                state_store=state_store,
                notifier=notifier,
                target_terms=("term",),
            )

            def fake_download(url: str, destination: Path) -> None:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(b"pdf")

            edition = EditionLink(number="2", date="01/02/2024", text="edition 2", url="https://example.com/2.pdf")
            with patch.object(BoituvaCrawler, "download_file", side_effect=fake_download), patch(
                "diario_oficial.crawlers.boituva.extract_pdf_text", return_value="contains term"
            ):
                result = crawler.process_edition(edition)

            self.assertEqual(result.status, "match")
            self.assertTrue(result.saved_pdf and result.saved_pdf.exists())

            with patch.object(BoituvaCrawler, "download_file", side_effect=fake_download), patch(
                "diario_oficial.crawlers.boituva.extract_pdf_text", return_value="nothing"
            ):
                result = crawler.process_edition(
                    EditionLink(number="3", date="", text="edition 3", url="https://example.com/3.pdf")
                )

            self.assertEqual(result.status, "no_match")
            self.assertIsNone(result.saved_pdf)

            editions = [
                EditionLink(number="1", date="", text="skip", url="https://example.com/1.pdf"),
                EditionLink(number="2", date="", text="request", url="https://example.com/2.pdf"),
                EditionLink(number="3", date="", text="runtime", url="https://example.com/3.pdf"),
                EditionLink(number="4", date="", text="ok", url="https://example.com/4.pdf"),
            ]

            with patch.object(crawler, "crawl_all_edition_links", return_value=editions), patch.object(
                crawler,
                "process_edition",
                side_effect=[
                    requests.RequestException("boom"),
                    RuntimeError("boom"),
                    EditionResult(
                        number="4",
                        date="",
                        url="https://example.com/4.pdf",
                        source_name="Boituva",
                        status="no_match",
                        matched_terms=[],
                        saved_pdf=None,
                        checked_at="2024-02-03T10:00:00",
                    ),
                ],
            ):
                summary = crawler.run(force=False)

            self.assertEqual(summary, {"processed": 1, "skipped": 1, "match": 0, "no_match": 1})
            self.assertEqual(len(notifier.notifications), 1)
            self.assertEqual(len(state_store.saved_payloads), 1)
            self.assertIn("4", state_store.saved_payloads[0])


class SorocabaCrawlerTest(unittest.TestCase):
    def test_parsers_and_helpers(self) -> None:
        from diario_oficial.crawlers.sorocaba import AnchorParser

        anchor_parser = AnchorParser()
        anchor_parser.feed('<a href="/link">Hello <b>World</b></a>')
        self.assertEqual(anchor_parser.anchors, [("Hello World", "/link")])

        self.assertEqual(SorocabaCrawler.normalize_text("ÁBÇ"), "ábç")
        self.assertEqual(SorocabaCrawler.safe_filename("a/b c"), "a_b_c")
        self.assertEqual(SorocabaCrawler.safe_filename("???"), "arquivo")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "out"
            response = FakeResponse(chunks=[b"a", b"b"])
            session = FakeSession({("https://example.com/file.pdf", True): response})
            crawler = SorocabaCrawler(
                session=session,
                output_dir=output_dir,
                state_store=MemoryStateStore(),
                notifier=MemoryNotifier(),
            )

            destination = Path(tmpdir) / "download.pdf"
            crawler.download_file("https://example.com/file.pdf", destination)
            self.assertEqual(destination.read_bytes(), b"ab")

    def test_extract_links_and_crawl(self) -> None:
        crawler = SorocabaCrawler(
            session=FakeSession(
                {
                    ("https://example.com/start", False): FakeResponse(
                        text="""
                        <a href="/d1.pdf">Jornal da Cidade - Edição n 123 de 01 DE FEVEREIRO DE 2024</a>
                        <a href="/d2.pdf">Jornal da Cidade - Edição n 124 de 02 DE FEVEREIRO DE 2024</a>
                        <a href="/d3.pdf">Sem edição</a>
                        <a href="/not-pdf">Ignore</a>
                        """
                    )
                }
            ),
            output_dir=Path("."),
            state_store=MemoryStateStore(),
            notifier=MemoryNotifier(),
        )

        html = """
        <a href="/d1.pdf">Jornal da Cidade - Edição n 123 de 01 DE FEVEREIRO DE 2024</a>
        <a href="/d2.pdf">Jornal da Cidade - Edição n 124 de 02 DE FEVEREIRO DE 2024</a>
        <a href="/d3.pdf">Sem edição</a>
        <a href="/not-pdf">Ignore</a>
        """
        editions = crawler.extract_edition_links(html, "https://example.com/base/")
        self.assertEqual([item.number for item in editions], ["123", "124"])
        self.assertEqual(editions[0].url, "https://example.com/d1.pdf")

        links = crawler.crawl_all_edition_links("https://example.com/start")
        self.assertEqual([item.number for item in links], ["124", "123"])

    def test_process_and_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "out"
            state_store = MemoryStateStore(initial_state={"https://example.com/1.pdf": {"status": "match"}})
            notifier = MemoryNotifier()
            crawler = SorocabaCrawler(
                session=FakeSession(),
                output_dir=output_dir,
                state_store=state_store,
                notifier=notifier,
                target_terms=("term",),
            )

            def fake_download(url: str, destination: Path) -> None:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(b"pdf")

            edition = EditionLink(number="2", date="01/02/2024", text="edition 2", url="https://example.com/2.pdf")
            with patch.object(SorocabaCrawler, "download_file", side_effect=fake_download), patch(
                "diario_oficial.crawlers.sorocaba.extract_pdf_text", return_value="contains term"
            ):
                result = crawler.process_edition(edition)

            self.assertEqual(result.status, "match")
            self.assertTrue(result.saved_pdf and result.saved_pdf.exists())

            with patch.object(SorocabaCrawler, "download_file", side_effect=fake_download), patch(
                "diario_oficial.crawlers.sorocaba.extract_pdf_text", return_value="nothing"
            ):
                result = crawler.process_edition(
                    EditionLink(number="3", date="", text="edition 3", url="https://example.com/3.pdf")
                )

            self.assertEqual(result.status, "no_match")
            self.assertIsNone(result.saved_pdf)

            editions = [
                EditionLink(number="1", date="", text="skip", url="https://example.com/1.pdf"),
                EditionLink(number="2", date="", text="request", url="https://example.com/2.pdf"),
                EditionLink(number="3", date="", text="runtime", url="https://example.com/3.pdf"),
                EditionLink(number="4", date="", text="ok", url="https://example.com/4.pdf"),
            ]

            with patch.object(crawler, "crawl_all_edition_links", return_value=editions), patch.object(
                crawler,
                "process_edition",
                side_effect=[
                    requests.RequestException("boom"),
                    RuntimeError("boom"),
                    EditionResult(
                        number="4",
                        date="",
                        url="https://example.com/4.pdf",
                        source_name="Sorocaba",
                        status="match",
                        matched_terms=["term"],
                        saved_pdf=Path("out.pdf"),
                        checked_at="2024-02-03T10:00:00",
                    ),
                ],
            ):
                summary = crawler.run(force=False)

            self.assertEqual(summary, {"processed": 1, "skipped": 1, "match": 1, "no_match": 0})
            self.assertEqual(len(notifier.notifications), 1)
            self.assertEqual(len(state_store.saved_payloads), 1)
            self.assertIn("https://example.com/4.pdf", state_store.saved_payloads[0])

    def test_run_without_terms_records_no_match(self) -> None:
        state_store = MemoryStateStore()
        notifier = MemoryNotifier()
        crawler = SorocabaCrawler(
            session=FakeSession(),
            output_dir=Path("."),
            state_store=state_store,
            notifier=notifier,
            target_terms=(),
        )

        with patch.object(
            crawler,
            "crawl_all_edition_links",
            return_value=[EditionLink(number="1", date="", text="one", url="https://example.com/1.pdf")],
        ):
            summary = crawler.run(force=False)

        self.assertEqual(summary, {"processed": 1, "skipped": 0, "match": 0, "no_match": 1})
        self.assertEqual(len(notifier.notifications), 0)
        self.assertEqual(state_store.saved_payloads[0]["https://example.com/1.pdf"]["status"], "no_match")
