from __future__ import annotations

import datetime as dt
import hashlib
import logging
import re
import shutil
import tempfile
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

from ..helpers import DEFAULT_TARGET_TERMS, extract_pdf_text
from ..models import EditionResult


class DocumentParser(HTMLParser):
    """Collect PDF and Drive links with their visible anchor labels."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.href: str | None = None
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            self.href = dict(attrs).get("href")
            self.parts = []

    def handle_data(self, data):
        if self.href is not None:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self.href is not None:
            self.links.append((" ".join(" ".join(self.parts).split()), self.href))
            self.href = None
            self.parts = []


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.casefold())
    return " ".join("".join(c for c in value if not unicodedata.combining(c)).split())


class CismetroCrawler:
    def __init__(
        self, session, output_dir, state_store, notifier,
        base_url="https://www.cismetro.com.br/convocacao-de-candidatos-para-admissao/",
        target_terms=DEFAULT_TARGET_TERMS,
    ):
        self.session = session
        self.output_dir = Path(output_dir)
        self.state_store = state_store
        self.notifier = notifier
        self.base_url = base_url
        self.target_terms = tuple(target_terms)

    def discover(self) -> list[tuple[str, str]]:
        response = self.session.get(self.base_url, timeout=30)
        response.raise_for_status()
        parser = DocumentParser()
        parser.feed(response.text)
        found = {}
        for label, href in parser.links:
            url = urljoin(self.base_url, href)
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https"):
                continue
            if parsed.path.lower().endswith(".pdf") or "drive.google.com/file/d/" in url:
                found[url] = label or Path(parsed.path).name
        return list(found.items())

    def run(self, force=False):
        state = self.state_store.load()
        summary = {"processed": 0, "skipped": 0, "match": 0, "no_match": 0}
        documents = self.discover()
        logging.info("CISMETRO: %d documentos encontrados", len(documents))
        if not documents:
            raise RuntimeError("Nenhum PDF encontrado na pagina CISMETRO; verificar HTML e links")
        for url, title in documents:
            key = hashlib.sha256(url.encode()).hexdigest()[:20]
            if not force and key in state:
                summary["skipped"] += 1
                continue
            try:
                result = self.process_document(key, url, title)
            except (requests.RequestException, OSError, ValueError) as exc:
                logging.error("Falha no documento %s: %s", url, exc)
                continue
            summary["processed"] += 1
            summary[result.status] += 1
            state[key] = {
                "number": key, "url": url, "title": title,
                "status": result.status, "source_name": result.source_name,
                "matched_terms": result.matched_terms,
                "checked_at": result.checked_at,
                "saved_pdf": str(result.saved_pdf) if result.saved_pdf else None,
            }
            self.state_store.save(state)
            if result.status == "match":
                self.notifier.notify(result)
        return summary

    def process_document(self, key, url, title):
        with tempfile.TemporaryDirectory(prefix="cismetro-") as tmp:
            path = Path(tmp) / "convocacao.pdf"
            pdf_url = url
            if "drive.google.com/file/d/" in url:
                file_id = url.split("/file/d/", 1)[1].split("/", 1)[0]
                if not re.fullmatch(r"[A-Za-z0-9_-]+", file_id):
                    raise ValueError("Identificador Google Drive invalido")
                pdf_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            response = self.session.get(pdf_url, timeout=60)
            response.raise_for_status()
            if not response.content.startswith(b"%PDF-"):
                raise ValueError("Link nao retornou PDF (pode exigir acesso ou confirmacao)")
            path.write_bytes(response.content)
            content = extract_pdf_text(path)
            if not content.strip():
                raise ValueError("PDF sem texto extraivel; nao marcar como processado")
            normalized = normalize(content)
            terms = [term for term in self.target_terms if normalize(term) in normalized]
            output = None
            if terms:
                self.output_dir.mkdir(parents=True, exist_ok=True)
                output = self.output_dir / f"convocacao_{key}.pdf"
                shutil.copy2(path, output)
            return EditionResult(
                number=title or key, date="", url=url,
                source_name="CISMETRO Convocacoes",
                status="match" if terms else "no_match",
                matched_terms=terms, saved_pdf=output,
                checked_at=dt.datetime.now().isoformat(timespec="seconds"),
            )
