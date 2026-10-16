"""Offline conformance checks for adapters implementing the canonical v1 contract."""
import unittest

from diario_oficial.adapter_contract import (
    AdapterCapabilities, CheckpointStrategy, DiscoveryBatch,
    DiscoveryContext, SourceAdapter, validate_batch,
)
from diario_oficial.canonical import canonicalize_edition, canonicalize_cismetro


class StaticAdapter:
    def __init__(self, publications, types, source_id, *, complete=True, errors=()):
        self._publications = publications
        self._source_id = source_id
        self._complete = complete
        self._errors = errors
        self.capabilities = AdapterCapabilities(
            publication_types=types,
            checkpoint_strategy=CheckpointStrategy.SNAPSHOT,
        )

    def discover(self, context):
        return DiscoveryBatch(
            publications=self._publications,
            next_cursor="next" if self._complete else context.cursor,
            complete=self._complete,
            errors=self._errors,
        )

    def fetch(self, document_url):
        return b"%PDF-1.7\n%%EOF"


class AdapterConformanceTests(unittest.TestCase):
    def setUp(self):
        self.edition = canonicalize_edition(
            "boituva", "1234", "Diário Oficial", "https://example.org/1234.pdf"
        )
        self.call = canonicalize_cismetro(
            "https://drive.google.com/file/d/ABC123/view", "Convocação"
        )

    def check_adapter(self, adapter, source):
        self.assertIsInstance(adapter, SourceAdapter)
        context = DiscoveryContext(source_id=source, baseline="initial", cursor="current")
        batch = adapter.discover(context)
        validate_batch(context, adapter.capabilities, batch)
        for publication in batch.publications:
            for document in publication.documents:
                self.assertTrue(adapter.fetch(document.url).startswith(b"%PDF"))

    def test_edition_adapter(self):
        self.check_adapter(
            StaticAdapter((self.edition,), ("EDITION",), "boituva"), "boituva"
        )

    def test_call_adapter(self):
        self.check_adapter(
            StaticAdapter((self.call,), ("CALL",), "cismetro"), "cismetro"
        )

    def test_wrong_source_rejected(self):
        adapter = StaticAdapter((self.edition,), ("EDITION",), "boituva")
        with self.assertRaisesRegex(ValueError, "source mismatch"):
            validate_batch(
                DiscoveryContext("cismetro", None, None),
                adapter.capabilities,
                adapter.discover(DiscoveryContext("boituva", None, None)),
            )

    def test_duplicate_publication_rejected(self):
        adapter = StaticAdapter((self.edition, self.edition), ("EDITION",), "boituva")
        context = DiscoveryContext("boituva", None, None)
        with self.assertRaisesRegex(ValueError, "duplicate publication"):
            validate_batch(context, adapter.capabilities, adapter.discover(context))

    def test_incomplete_batch_cannot_advance(self):
        context = DiscoveryContext("boituva", None, "cursor-1")
        adapter = StaticAdapter((self.edition,), ("EDITION",), "boituva", complete=False, errors=("timeout",))
        validate_batch(context, adapter.capabilities, adapter.discover(context))
        bad = DiscoveryBatch((self.edition,), "cursor-2", False, ("timeout",))
        with self.assertRaisesRegex(ValueError, "checkpoint"):
            validate_batch(context, adapter.capabilities, bad)

    def test_undeclared_publication_type_rejected(self):
        adapter = StaticAdapter((self.call,), ("EDITION",), "cismetro")
        context = DiscoveryContext("cismetro", None, None)
        with self.assertRaisesRegex(ValueError, "undeclared"):
            validate_batch(context, adapter.capabilities, adapter.discover(context))


if __name__ == "__main__":
    unittest.main()
