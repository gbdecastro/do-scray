from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path


def extract_pdf_text(pdf_path: Path) -> str:
    text = _extract_with_pymupdf(pdf_path)
    if text.strip():
        return text

    fallback_text = _extract_with_pdftotext(pdf_path)
    if fallback_text.strip():
        logging.info("Fallback para pdftotext aplicado em %s.", pdf_path.name)
        return fallback_text

    return text or fallback_text


def _extract_with_pymupdf(pdf_path: Path) -> str:
    try:
        import pymupdf
    except ImportError:
        logging.info("PyMuPDF não está disponível; usando pdftotext.")
        return ""

    try:
        with pymupdf.open(pdf_path) as doc:
            pages: list[str] = []
            for page in doc:
                page_text = page.get_text("text")
                if page_text.strip():
                    pages.append(page_text)
                    continue

                try:
                    textpage = page.get_textpage_ocr(language="por+eng")
                    pages.append(page.get_text("text", textpage=textpage))
                except Exception as exc:
                    logging.debug("OCR via PyMuPDF indisponível para %s: %s", pdf_path, exc)
                    pages.append(page_text)

        return "\n".join(pages)
    except Exception as exc:
        logging.warning("Falha ao extrair texto com PyMuPDF de %s: %s", pdf_path, exc)
        return ""


def _extract_with_pdftotext(pdf_path: Path) -> str:
    if shutil.which("pdftotext") is None:
        logging.warning("pdftotext não encontrado; extração de texto indisponível.")
        return ""

    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        logging.warning("Falha ao extrair texto com pdftotext de %s: %s", pdf_path, exc)
        return ""

    return result.stdout
