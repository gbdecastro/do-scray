from __future__ import annotations

import logging
import json
import os
import time
import subprocess
import sys
from pathlib import Path

from ..jobs import CRAWLER_JOBS
from ..models.run_manifest import CrawlerRunResult, RunManifest, timestamp, write_manifest


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
    result_path = ROOT_DIR / 'reports' / 'results' / f'{job_name}.json'
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.unlink(missing_ok=True)
    env = os.environ.copy()
    env['DO_SCRAY_RESULT'] = str(result_path)
    result = subprocess.run(command, cwd=ROOT_DIR, env=env)
    if result.returncode == 0:
        logging.info("Crawler %s finalizado com sucesso.", job_name)
    else:
        logging.error(
            "Crawler %s finalizado com erro. Código: %d",
            job_name,
            result.returncode,
        )
    return result.returncode


def select_jobs(selection: str):
    if selection == "all":
        return CRAWLER_JOBS
    jobs = [job for job in CRAWLER_JOBS if job.name == selection]
    if not jobs:
        raise ValueError(f"Unknown crawler: {selection}")
    return jobs


def main() -> int:
    setup_logging()
    overall_status = 0
    started_at = timestamp()
    results: list[CrawlerRunResult] = []

    logging.info("Execução do conjunto de crawlers iniciada.")
    selection = os.environ.get("DO_SCRAY_CRAWLER", "all")
    force = os.environ.get("DO_SCRAY_FORCE", "false").lower() == "true"
    for job in select_jobs(selection):
        job_started_at = timestamp()
        start_clock = time.monotonic()
        try:
            status = run_job(job.name, job.script, [*job.args, *(["--force"] if force else [])])
        except Exception:
            logging.exception("Falha inesperada ao iniciar crawler %s", job.name)
            status = 1
        metrics_path = ROOT_DIR / 'reports' / 'results' / f'{job.name}.json'
        metrics = None
        if metrics_path.exists():
            try:
                raw = json.loads(metrics_path.read_text(encoding='utf-8'))
                if isinstance(raw, dict) and all(isinstance(raw.get(k), int) and raw[k] >= 0 for k in ('processed', 'skipped', 'match', 'no_match', 'errors')):
                    metrics = {k: raw[k] for k in ('processed', 'skipped', 'match', 'no_match', 'errors')}
            except (OSError, ValueError, TypeError):
                logging.warning('Métricas inválidas para %s', job.name)
        results.append(CrawlerRunResult(
            name=job.name,
            status="success" if status == 0 else "failed",
            exit_code=status,
            started_at=job_started_at,
            finished_at=timestamp(),
            duration_seconds=round(time.monotonic() - start_clock, 3),
            metrics=metrics,
        ))
        if status != 0:
            overall_status = status

    manifest = RunManifest(
        schema_version=1,
        started_at=started_at,
        finished_at=timestamp(),
        status="success" if overall_status == 0 else "partial_failure",
        crawlers=results,
    )
    destination = Path(os.environ.get("DO_SCRAY_MANIFEST", str(ROOT_DIR / "reports" / "run.json")))
    try:
        write_manifest(manifest, destination)
        logging.info("Manifesto da execução: %s", destination)
    except OSError:
        logging.exception("Não foi possível gravar o manifesto")
        overall_status = 1
    logging.info("Execução do conjunto de crawlers finalizada.")
    return overall_status


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
