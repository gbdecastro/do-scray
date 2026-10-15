from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from diario_oficial.models.run_manifest import CrawlerRunResult, RunManifest, write_manifest
from diario_oficial.apps import run_crawlers


class ManifestTests(unittest.TestCase):
    def test_serialization(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "reports" / "run.json"
            item = CrawlerRunResult("boituva", "success", 0, "start", "end", 1.5)
            write_manifest(RunManifest(1, "start", "end", "success", [item]), destination)
            data = json.loads(destination.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], 1)
            self.assertEqual(data["crawlers"][0]["name"], "boituva")
            self.assertEqual(data["crawlers"][0]["duration_seconds"], 1.5)

    def test_main_continues_after_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "run.json"
            with patch.object(run_crawlers, "setup_logging"), patch.object(
                run_crawlers, "CRAWLER_JOBS",
                [run_crawlers.CRAWLER_JOBS[0], run_crawlers.CRAWLER_JOBS[1]],
            ), patch.object(run_crawlers, "run_job", side_effect=[1, 0]) as job, patch.dict(
                "os.environ", {"DO_SCRAY_MANIFEST": str(destination)}
            ):
                self.assertEqual(run_crawlers.main(), 1)
            self.assertEqual(job.call_count, 2)
            data = json.loads(destination.read_text())
            self.assertEqual(data["status"], "partial_failure")
            self.assertEqual([x["status"] for x in data["crawlers"]], ["failed", "success"])

    def test_main_captures_unexpected_exception(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "run.json"
            with patch.object(run_crawlers, "setup_logging"), patch.object(
                run_crawlers, "CRAWLER_JOBS", [run_crawlers.CRAWLER_JOBS[0]]
            ), patch.object(run_crawlers, "run_job", side_effect=RuntimeError("boom")), patch.dict(
                "os.environ", {"DO_SCRAY_MANIFEST": str(destination)}
            ):
                self.assertEqual(run_crawlers.main(), 1)
            self.assertEqual(json.loads(destination.read_text())["crawlers"][0]["status"], "failed")

    def test_preserves_last_nonzero_exit_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "run.json"
            with patch.object(run_crawlers, "setup_logging"), patch.object(
                run_crawlers, "CRAWLER_JOBS", [run_crawlers.CRAWLER_JOBS[0]]
            ), patch.object(run_crawlers, "run_job", return_value=7), patch.dict(
                "os.environ", {"DO_SCRAY_MANIFEST": str(destination)}
            ):
                self.assertEqual(run_crawlers.main(), 7)
            self.assertEqual(json.loads(destination.read_text())["crawlers"][0]["exit_code"], 7)

    def test_manifest_includes_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / 'run.json'
            result_dir = run_crawlers.ROOT_DIR / 'reports' / 'results'
            with patch.object(run_crawlers, 'ROOT_DIR', Path(tmp)), patch.object(run_crawlers, 'setup_logging'), patch.object(
                run_crawlers, 'CRAWLER_JOBS', [run_crawlers.CRAWLER_JOBS[0]]
            ), patch.object(run_crawlers, 'run_job', return_value=0), patch.dict(
                'os.environ', {'DO_SCRAY_MANIFEST': str(destination)}
            ):
                metrics_file = Path(tmp) / 'reports' / 'results' / f'{run_crawlers.CRAWLER_JOBS[0].name}.json'
                metrics_file.parent.mkdir(parents=True)
                metrics_file.write_text(json.dumps({'processed': 2, 'skipped': 1, 'match': 1, 'no_match': 1, 'errors': 0}))
                self.assertEqual(run_crawlers.main(), 0)
            self.assertEqual(json.loads(destination.read_text())['crawlers'][0]['metrics']['processed'], 2)

    def test_main_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "run.json"
            with patch.object(run_crawlers, "setup_logging"), patch.object(
                run_crawlers, "CRAWLER_JOBS", [run_crawlers.CRAWLER_JOBS[0]]
            ), patch.object(run_crawlers, "run_job", return_value=0), patch.dict(
                "os.environ", {"DO_SCRAY_MANIFEST": str(destination)}
            ):
                self.assertEqual(run_crawlers.main(), 0)
            self.assertEqual(json.loads(destination.read_text())["status"], "success")


if __name__ == "__main__":
    unittest.main()
