from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ..helpers import DEFAULT_TARGET_TERMS
from ..crawlers import BoituvaCrawler
from ..runner import run_crawler


BASE_URL = "https://www.boituva.sp.gov.br/diario-oficial"
OUTPUT_DIR = Path("DO/Boituva")
LOG_DIR = Path("logs")
STATE_DIR = Path("state")
STATE_FILE = STATE_DIR / "edicoes_lidas_boituva.json"
LOG_FILE = LOG_DIR / "diario_oficial_boituva.log"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crawler do Diário Oficial de Boituva com notificações Telegram."
    )
    parser.add_argument(
        "--url",
        default=BASE_URL,
        help=f"URL inicial da página do Diário Oficial (padrão: {BASE_URL})",
    )
    parser.add_argument(
        "--term",
        action="append",
        default=[],
        metavar="TERMO",
        help="Termo a ser buscado no PDF. Pode ser informado várias vezes.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reprocessa edições mesmo que já existam no arquivo de estado.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_terms = tuple(args.term) if args.term else DEFAULT_TARGET_TERMS
    return run_crawler(
        BoituvaCrawler,
        base_url=args.url,
        output_dir=OUTPUT_DIR,
        state_file=STATE_FILE,
        log_file=LOG_FILE,
        user_agent=USER_AGENT,
        force=args.force,
        crawler_kwargs={"target_terms": target_terms},
    )


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
