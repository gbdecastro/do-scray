from __future__ import annotations

import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from diario_oficial.helpers import pdf_text_extractor as extractor


class PdfTextExtractorTest(unittest.TestCase):
    def test_extract_pdf_text_prefers_primary_and_fallback_paths(self) -> None:
        with patch.object(extractor, "_extract_with_pymupdf", return_value="primary") as primary, patch.object(
            extractor, "_extract_with_pdftotext", return_value="fallback"
        ) as fallback:
            self.assertEqual(extractor.extract_pdf_text(Path("file.pdf")), "primary")
            primary.assert_called_once()
            fallback.assert_not_called()

        with patch.object(extractor, "_extract_with_pymupdf", return_value="") as primary, patch.object(
            extractor, "_extract_with_pdftotext", return_value="fallback"
        ) as fallback:
            self.assertEqual(extractor.extract_pdf_text(Path("file.pdf")), "fallback")
            primary.assert_called_once()
            fallback.assert_called_once()

        with patch.object(extractor, "_extract_with_pymupdf", return_value="") as primary, patch.object(
            extractor, "_extract_with_pdftotext", return_value=""
        ) as fallback:
            self.assertEqual(extractor.extract_pdf_text(Path("file.pdf")), "")
            primary.assert_called_once()
            fallback.assert_called_once()

    def test_extract_with_pymupdf_import_error(self) -> None:
        with patch.dict(sys.modules, {"pymupdf": None}):
            self.assertEqual(extractor._extract_with_pymupdf(Path("file.pdf")), "")

    def test_extract_with_pymupdf_reads_pages_and_handles_ocr_failure(self) -> None:
        class Page:
            def __init__(self, text: str, ocr_text: str | None = None, raise_ocr: bool = False) -> None:
                self.text = text
                self.ocr_text = ocr_text or ""
                self.raise_ocr = raise_ocr

            def get_text(self, mode: str, textpage=None) -> str:
                if textpage is not None:
                    return self.ocr_text
                return self.text

            def get_textpage_ocr(self, language: str):
                if self.raise_ocr:
                    raise RuntimeError("ocr unavailable")
                return object()

        class Doc:
            def __init__(self, pages: list[Page]) -> None:
                self.pages = pages

            def __enter__(self) -> "Doc":
                return self

            def __exit__(self, exc_type, exc, tb) -> bool:
                return False

            def __iter__(self):
                return iter(self.pages)

        fake_module = types.SimpleNamespace(
            open=lambda pdf_path: Doc(
                [
                    Page("Page 1 text"),
                    Page("", ocr_text="OCR text"),
                    Page("", raise_ocr=True),
                ]
            )
        )

        with patch.dict(sys.modules, {"pymupdf": fake_module}):
            text = extractor._extract_with_pymupdf(Path("file.pdf"))

        self.assertIn("Page 1 text", text)
        self.assertIn("OCR text", text)

    def test_extract_with_pymupdf_open_failure(self) -> None:
        fake_module = types.SimpleNamespace(open=lambda pdf_path: (_ for _ in ()).throw(RuntimeError("boom")))

        with patch.dict(sys.modules, {"pymupdf": fake_module}):
            self.assertEqual(extractor._extract_with_pymupdf(Path("file.pdf")), "")

    def test_extract_with_pdftotext_branches(self) -> None:
        with patch.object(extractor.shutil, "which", return_value=None):
            self.assertEqual(extractor._extract_with_pdftotext(Path("file.pdf")), "")

        class Result:
            stdout = "extracted text"

        with patch.object(extractor.shutil, "which", return_value="/usr/bin/pdftotext"), patch.object(
            extractor.subprocess, "run", return_value=Result()
        ) as run:
            self.assertEqual(extractor._extract_with_pdftotext(Path("file.pdf")), "extracted text")
            run.assert_called_once()

        with patch.object(extractor.shutil, "which", return_value="/usr/bin/pdftotext"), patch.object(
            extractor.subprocess,
            "run",
            side_effect=extractor.subprocess.CalledProcessError(1, ["pdftotext"]),
        ):
            self.assertEqual(extractor._extract_with_pdftotext(Path("file.pdf")), "")
