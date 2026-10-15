from __future__ import annotations

import logging
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests

from .services import JsonStateStore, TelegramNotifier
from .services.durable_notifier import DurableNotifier


def setup_logging(log_file: Path) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def run_crawler(
    crawler_cls: type[Any],
    *,
    base_url: str,
    output_dir: Path,
    state_file: Path,
    log_file: Path,
    user_agent: str,
    force: bool = False,
    crawler_kwargs: dict[str, Any] | None = None,
) -> int:
    setup_logging(log_file)
    logging.info("Execução iniciada")
    logging.info("URL base: %s", base_url)
    logging.info("Saída dos PDFs: %s", output_dir.resolve())
    logging.info("Arquivo de log: %s", log_file.resolve())
    logging.info("Arquivo de estado: %s", state_file.resolve())

    session = requests.Session()
    session.headers.update({"User-Agent": user_agent})
    notifier = DurableNotifier(state_file) if os.environ.get('DO_SCRAY_DURABLE_NOTIFICATIONS') == '1' else TelegramNotifier()

    crawler = crawler_cls(
        session=session,
        output_dir=output_dir,
        state_store=JsonStateStore(state_file),
        notifier=notifier,
        base_url=base_url,
        **(crawler_kwargs or {}),
    )

    try:
        summary = crawler.run(force=force)
    except requests.RequestException as exc:
        logging.exception("Falha geral na execução do crawler: %s", exc)
        return 1
    finally:
        notifier.close()

    result_path = os.environ.get('DO_SCRAY_RESULT')
    if result_path:
        try:
            metrics = {key: int(summary.get(key, 0)) for key in ('processed', 'skipped', 'match', 'no_match', 'errors')}
            destination = Path(result_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_suffix('.tmp')
            temporary.write_text(json.dumps(metrics, ensure_ascii=False) + '\n', encoding='utf-8')
            temporary.replace(destination)
        except (OSError, ValueError, TypeError) as exc:
            logging.error('Falha ao registrar métricas: %s', exc)
            return 1

    logging.info(
        "Execução finalizada. Processadas: %d | Ignoradas: %d | Matches: %d | Sem match: %d",
        summary["processed"],
        summary["skipped"],
        summary["match"],
        summary["no_match"],
    )
    return 0
