from __future__ import annotations

import unittest
from pathlib import Path

import diario_oficial
from diario_oficial.helpers import DEFAULT_TARGET_TERMS
from diario_oficial.jobs import CRAWLER_JOBS, CrawlerJob
from diario_oficial.models import EditionLink, EditionResult


class ModelsAndJobsTest(unittest.TestCase):
    def test_package_and_dataclasses(self) -> None:
        self.assertTrue(hasattr(diario_oficial, "__file__"))
        self.assertEqual(DEFAULT_TARGET_TERMS[0], "TALINE MONTEIRO")

        job = CrawlerJob(name="demo", script=Path("demo.py"))
        self.assertEqual(job.args, [])
        self.assertEqual(job.name, "demo")
        self.assertEqual(job.script, Path("demo.py"))

        self.assertEqual([item.name for item in CRAWLER_JOBS], ["boituva", "indaiatuba", "sorocaba"])

        link = EditionLink(number="1", date="2024-01-01", text="title", url="https://example.com")
        result = EditionResult(
            number="1",
            date="2024-01-01",
            url="https://example.com",
            source_name="Boituva",
            status="match",
            matched_terms=["term"],
            saved_pdf=Path("output.pdf"),
            checked_at="2024-01-01T00:00:00",
        )

        self.assertEqual(link.text, "title")
        self.assertEqual(result.source_name, "Boituva")
