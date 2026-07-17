from __future__ import annotations

import datetime as dt
import logging
import re
import shutil
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin

import requests

from ..helpers import DEFAULT_TARGET_TERMS, extract_pdf_text
from ..models import EditionLink, EditionResult


class AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._current_href: str | None = None
        self._current_text: list[str] = []
        self.anchors: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        attr_map = dict(attrs)
        self._current_href = attr_map.get("href")
        self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._current_href is not None:
            self._current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or self._current_href is None:
            return

        text = " ".join(" ".join(self._current_text).split())
        href = self._current_href.strip()
        if href:
            self.anchors.append((text, href))

        self._current_href = None
        self._current_text = []


class IndaiatubaCrawler:
    def __init__(
        self,
        session: requests.Session,
        output_dir: Path,
        state_store,
        notifier,
        base_url: str = "https://www.indaiatuba.sp.gov.br/comunicacao-social/imprensa-oficial/edicoes/",
        target_terms: Iterable[str] = DEFAULT_TARGET_TERMS,
    ) -> None:
        self.session = session
        self.output_dir = output_dir
        self.state_store = state_store
        self.notifier = notifier
        self.base_url = base_url
        self.target_terms = list(target_terms)

    def run(self, force: bool = False) -> dict[str, int]:
        state = self.state_store.load()
        editions = self.crawl_all_edition_links(self.base_url)

        summary = {"processed": 0, "skipped": 0, "match": 0, "no_match": 0}
        logging.info("Total de edicoes encontradas: %d", len(editions))
        logging.info("Processando edicoes com termos de busca: %s", self.target_terms)

        if not self.target_terms:
            logging.warning(
                "Nenhum termo de busca foi configurado para Indaiatuba. "
                "As edicoes serao apenas registradas como 'sem match'."
            )

        for edition in editions:
            state_key = edition.number
            if not force and state_key in state:
                logging.info(
                    "Edicao %s (%s) ja foi processada, ignorando.",
                    edition.number,
                    edition.date or "data desconhecida",
                )
                summary["skipped"] += 1
                continue

            try:
                result = self.process_edition(edition)
            except requests.RequestException as exc:
                logging.exception("Falha ao baixar a edicao %s: %s", edition.number, exc)
                continue
            except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
                logging.exception("Erro ao processar a edicao %s: %s", edition.number, exc)
                continue

            summary["processed"] += 1
            summary[result.status] += 1
            state[state_key] = {
                "number": result.number,
                "date": result.date,
                "url": result.url,
                "source_name": result.source_name,
                "checked_at": result.checked_at,
                "status": result.status,
                "matched_terms": result.matched_terms,
                "saved_pdf": str(result.saved_pdf) if result.saved_pdf else None,
            }
            self.notifier.notify(result)

        self.state_store.save(state)
        return summary

    def fetch_html(self, url: str) -> str:
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or response.encoding
        return response.text

    def crawl_all_edition_links(self, start_url: str) -> list[EditionLink]:
        visited_pages: set[str] = set()
        queued_pages: list[str] = [start_url]
        found: dict[str, EditionLink] = {}

        while queued_pages:
            page_url = queued_pages.pop(0)
            if page_url in visited_pages:
                continue

            visited_pages.add(page_url)
            logging.info("Lendo pagina: %s", page_url)
            html = self.fetch_html(page_url)

            for item in self.extract_edition_links(html, page_url):
                found[item.number] = item

            for next_page in self.extract_pagination_links(html, page_url):
                if next_page not in visited_pages and next_page not in queued_pages:
                    queued_pages.append(next_page)

        return sorted(found.values(), key=lambda item: int(item.number), reverse=True)

    def extract_edition_links(self, html: str, page_url: str) -> list[EditionLink]:
        parser = AnchorParser()
        parser.feed(html)

        edition_links: list[EditionLink] = []
        edition_pattern = re.compile(r"Edi[cç][aã]o\s+N[^\d]*(\d+)", re.IGNORECASE)
        date_pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{4})")

        for text, href in parser.anchors:
            match = edition_pattern.search(text)
            if not match:
                continue

            date_match = date_pattern.search(text)
            edition_links.append(
                EditionLink(
                    number=match.group(1),
                    date=" ".join(date_match.group(1).split()) if date_match else "",
                    text=text,
                    url=urljoin(page_url, href),
                )
            )

        return edition_links

    def extract_pagination_links(self, html: str, page_url: str) -> list[str]:
        parser = AnchorParser()
        parser.feed(html)
        links: list[str] = []

        for text, href in parser.anchors:
            normalized = " ".join(text.lower().split())
            if normalized in {"próxima", "proxima", "next", ">", "»"}:
                links.append(urljoin(page_url, href))
                continue

            if re.fullmatch(r"\d+", text.strip()):
                links.append(urljoin(page_url, href))
                continue

            if re.search(r"[?&](page|pagina|p)=\d+", href, re.IGNORECASE):
                links.append(urljoin(page_url, href))

        return links

    def download_file(self, url: str, destination: Path) -> None:
        with self.session.get(url, stream=True, timeout=60) as response:
            response.raise_for_status()
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=1024 * 128):
                    if chunk:
                        handle.write(chunk)

    @staticmethod
    def normalize_text(text: str) -> str:
        return text.casefold()

    def find_target_terms(self, text: str) -> list[str]:
        normalized = self.normalize_text(text)
        return [
            term for term in self.target_terms if self.normalize_text(term) in normalized
        ]

    @staticmethod
    def safe_filename(name: str) -> str:
        cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_.")
        return cleaned or "arquivo"

    def process_edition(self, edition: EditionLink) -> EditionResult:
        logging.info(
            "Baixando edicao %s (%s): %s",
            edition.number,
            edition.date or "data desconhecida",
            edition.url,
        )

        with tempfile.TemporaryDirectory(prefix="indaiatuba-do-") as temp_dir:
            temp_pdf = Path(temp_dir) / f"edicao_{edition.number}.pdf"
            self.download_file(edition.url, temp_pdf)
            pdf_text = extract_pdf_text(temp_pdf)
            matched_terms = self.find_target_terms(pdf_text)

            if matched_terms:
                self.output_dir.mkdir(parents=True, exist_ok=True)
                date_slug = self.safe_filename(
                    edition.date.replace("/", "-") if edition.date else "sem-data"
                )
                output_file = self.output_dir / f"edicao_{edition.number}_{date_slug}.pdf"
                shutil.copy2(temp_pdf, output_file)
                logging.info(
                    "Correspondencia encontrada na edicao %s (%s). PDF salvo em %s",
                    edition.number,
                    ", ".join(matched_terms),
                    output_file,
                )
                status = "match"
                saved_pdf = output_file
            else:
                logging.info("Sem correspondencia na edicao %s", edition.number)
                status = "no_match"
                saved_pdf = None

            return EditionResult(
                number=edition.number,
                date=edition.date,
                url=edition.url,
                source_name="Indaiatuba",
                status=status,
                matched_terms=matched_terms,
                saved_pdf=saved_pdf,
                checked_at=dt.datetime.now().isoformat(timespec="seconds"),
            )
