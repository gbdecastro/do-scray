from __future__ import annotations

import sys
import unittest
from unittest.mock import patch

from diario_oficial.apps import cismetro
from diario_oficial.helpers import DEFAULT_TARGET_TERMS


class CismetroAppTests(unittest.TestCase):
    def test_default_arguments(self):
        with patch.object(sys, "argv", ["cismetro"]):
            args = cismetro.parse_args()
        self.assertEqual(args.url, cismetro.BASE_URL)
        self.assertEqual(args.term, [])
        self.assertFalse(args.force)

    def test_custom_arguments(self):
        with patch.object(sys, "argv", [
            "cismetro", "--url", "https://example.org/docs",
            "--term", "BOITUVA", "--term", "TALINE", "--force",
        ]):
            args = cismetro.parse_args()
        self.assertEqual(args.url, "https://example.org/docs")
        self.assertEqual(args.term, ["BOITUVA", "TALINE"])
        self.assertTrue(args.force)

    @patch("diario_oficial.apps.cismetro.run_crawler", return_value=0)
    def test_main_uses_default_terms(self, run):
        with patch.object(sys, "argv", ["cismetro"]):
            self.assertEqual(cismetro.main(), 0)
        self.assertEqual(run.call_args.kwargs["crawler_kwargs"]["target_terms"], DEFAULT_TARGET_TERMS)
        self.assertIs(run.call_args.args[0], cismetro.CismetroCrawler)

    @patch("diario_oficial.apps.cismetro.run_crawler", return_value=0)
    def test_main_forwards_terms_and_force(self, run):
        with patch.object(sys, "argv", ["cismetro", "--term", "ENFERMEIRO", "--force"]):
            self.assertEqual(cismetro.main(), 0)
        self.assertEqual(run.call_args.kwargs["crawler_kwargs"]["target_terms"], ("ENFERMEIRO",))
        self.assertTrue(run.call_args.kwargs["force"])


if __name__ == "__main__":
    unittest.main()
