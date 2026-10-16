from dataclasses import replace
import unittest

from diario_oficial.canonical import (
    CanonicalDocument, PublicationType, canonicalize_edition,
    canonicalize_cismetro, validate_manifest,
)
from diario_oficial.crawlers.boituva import BoituvaCrawler
from diario_oficial.crawlers.cismetro import DocumentParser

BOITUVA_HTML = '<article><small class="list-date">15/10/2026</small><a href="/files/1234.pdf">Diário Oficial - Edição 1234</a></article>'
CISMETRO_HTML = '<a href="https://drive.google.com/file/d/ABC123/view">Convocação para admissão</a>'

class CanonicalContractTests(unittest.TestCase):
    def test_boituva_fixture_through_real_parser(self):
        crawler = BoituvaCrawler(None, None, None, None)
        editions = crawler.extract_edition_links(BOITUVA_HTML, "https://www.boituva.sp.gov.br/diario-oficial")
        self.assertEqual(len(editions), 1)
        p = canonicalize_edition("boituva", editions[0].number, editions[0].text, editions[0].url)
        validate_manifest(p)
        self.assertEqual((p.type, p.key), (PublicationType.EDITION, "edition:1234"))

    def test_cismetro_fixture_through_real_parser(self):
        parser = DocumentParser()
        parser.feed(CISMETRO_HTML)
        self.assertEqual(len(parser.links), 1)
        title, url = parser.links[0]
        p = canonicalize_cismetro(url, title)
        validate_manifest(p)
        self.assertEqual((p.type, p.key), (PublicationType.CALL, "drive:ABC123"))

    def test_edition_key_survives_url_change(self):
        a = canonicalize_edition("boituva", "01234", "Diário", "https://example.org/a.pdf?utm_source=foo")
        b = canonicalize_edition("boituva", "1234", "Diário", "https://example.org/b.pdf")
        self.assertEqual(a.key, b.key)

    def test_multiple_documents(self):
        p = canonicalize_edition("boituva", "1234", "Diário", "https://example.org/main.pdf")
        p = replace(p, documents=p.documents + (CanonicalDocument("annex:1", "ANNEX", "https://example.org/annex.pdf"),))
        validate_manifest(p)
        self.assertEqual(len(p.documents), 2)

    def test_duplicate_document_key_is_rejected(self):
        p = canonicalize_edition("boituva", "1234", "Diário", "https://example.org/main.pdf")
        with self.assertRaises(ValueError):
            validate_manifest(replace(p, documents=p.documents + p.documents))

    def test_cismetro_url_fallback_is_not_stable_on_url_change(self):
        a = canonicalize_cismetro("https://example.org/a.pdf", "Convocação")
        b = canonicalize_cismetro("https://example.org/b.pdf", "Convocação")
        self.assertNotEqual(a.key, b.key)

    def test_cismetro_official_id_survives_url_change(self):
        a = canonicalize_cismetro("https://example.org/a.pdf", "Convocação", "2026-10")
        b = canonicalize_cismetro("https://example.org/b.pdf", "Convocação", "2026-10")
        self.assertEqual(a.key, b.key)

if __name__ == "__main__":
    unittest.main()
