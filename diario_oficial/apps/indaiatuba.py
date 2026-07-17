from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ..crawlers import IndaiatubaCrawler
from ..helpers import DEFAULT_TARGET_TERMS
from ..runner import run_crawler


BASE_URL = "https://www.indaiatuba.sp.gov.br/comunicacao-social/imprensa-oficial/edicoes/"
OUTPUT_DIR = Path("DO/Indaiatuba")
LOG_DIR = Path("logs")
STATE_DIR = Path("state")
STATE_FILE = STATE_DIR / "edicoes_lidas_indaiatuba.json"
LOG_FILE = LOG_DIR / "diario_oficial_indaiatuba.log"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crawler da Imprensa Oficial de Indaiatuba com notificacoes Telegram."
    )
    parser.add_argument(
        "--url",
        default=BASE_URL,
        help=f"URL inicial da pagina da Imprensa Oficial (padrao: {BASE_URL})",
    )
    parser.add_argument(
        "--term",
        action="append",
        default=[],
        metavar="TERMO",
        help="Termo a ser buscado no PDF. Pode ser informado varias vezes.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reprocessa edicoes mesmo que ja existam no arquivo de estado.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_terms = tuple(args.term) if args.term else DEFAULT_TARGET_TERMS
    return run_crawler(
        IndaiatubaCrawler,
        base_url=args.url,
        output_dir=OUTPUT_DIR,
        state_file=STATE_FILE,
        log_file=LOG_FILE,
        user_agent=USER_AGENT,
        force=args.force,
        crawler_kwargs={"target_terms": target_terms},
    )


if __name__ == "__main__":
    raise SystemExit(main())
