from __future__ import annotations

import argparse
from pathlib import Path

from ..crawlers.cismetro import CismetroCrawler
from ..helpers import DEFAULT_TARGET_TERMS
from ..runner import run_crawler

BASE_URL = "https://www.cismetro.com.br/convocacao-de-candidatos-para-admissao/"
OUTPUT_DIR = Path("DO/CISMETRO")
STATE_FILE = Path("state/cismetro_convocacoes.json")
LOG_FILE = Path("logs/cismetro_convocacoes.log")
USER_AGENT = "Mozilla/5.0 (compatible; do-scray/1.0)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Busca termos nas convocacoes do CISMETRO.")
    parser.add_argument("--url", default=BASE_URL)
    parser.add_argument("--term", action="append", default=[], metavar="TERMO")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_crawler(
        CismetroCrawler,
        base_url=args.url,
        output_dir=OUTPUT_DIR,
        state_file=STATE_FILE,
        log_file=LOG_FILE,
        user_agent=USER_AGENT,
        force=args.force,
        crawler_kwargs={"target_terms": tuple(args.term) if args.term else DEFAULT_TARGET_TERMS},
    )


if __name__ == "__main__":
    raise SystemExit(main())
