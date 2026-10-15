from __future__ import annotations

import unittest
from pathlib import Path


class DashboardMobileLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (Path(__file__).resolve().parents[1] / "diario_oficial/web_dashboard/template.html").read_text(encoding="utf-8")

    def test_viewport_and_mobile_breakpoints(self):
        self.assertIn('name="viewport" content="width=device-width,initial-scale=1"', self.html)
        self.assertIn("@media(max-width:767px)", self.html)
        self.assertIn("@media(max-width:359px)", self.html)

    def test_mobile_filters_and_tables(self):
        self.assertIn(".controls{display:grid", self.html)
        self.assertIn("grid-template-columns:repeat(2,minmax(0,1fr))", self.html)
        self.assertIn("-webkit-overflow-scrolling:touch", self.html)
        self.assertIn("min-height:44px", self.html)
        self.assertIn("overflow-x:auto", self.html)

    def test_mobile_accessibility(self):
        self.assertIn(":focus-visible", self.html)
        self.assertIn("prefers-reduced-motion:reduce", self.html)
