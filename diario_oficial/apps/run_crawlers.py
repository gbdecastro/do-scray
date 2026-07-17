from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path

from ..jobs import CRAWLER_JOBS


ROOT_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT_DIR / "logs"
LOG_FILE = LOG_DIR / "run_crawlers.log"


def setup_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def run_job(job_name: str, script: Path, args: list[str]) -> int:
    module_name = ".".join(script.with_suffix("").parts)
    command = [sys.executable, "-m", module_name, *args]
    logging.info("Iniciando crawler %s: %s", job_name, " ".join(command))
    result = subprocess.run(command, cwd=ROOT_DIR)
    if result.returncode == 0:
        logging.info("Crawler %s finalizado com sucesso.", job_name)
    else:
        logging.error(
            "Crawler %s finalizado com erro. Código: %d",
            job_name,
            result.returncode,
        )
    return result.returncode


def main() -> int:
    setup_logging()
    overall_status = 0

    logging.info("Execução do conjunto de crawlers iniciada.")
    for job in CRAWLER_JOBS:
        status = run_job(job.name, job.script, job.args)
        if status != 0:
            overall_status = status

    logging.info("Execução do conjunto de crawlers finalizada.")
    return overall_status


if __name__ == "__main__":
    raise SystemExit(main())
