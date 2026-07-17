from __future__ import annotations

import sys
import tempfile
import unittest
import importlib
from pathlib import Path
from unittest.mock import patch

from diario_oficial.apps import boituva, run_crawlers, sorocaba
from diario_oficial.jobs import CrawlerJob
from diario_oficial.crawlers import BoituvaCrawler, SorocabaCrawler


class AppsTest(unittest.TestCase):
    def test_boituva_parse_args_and_main(self) -> None:
        with patch.object(sys, "argv", ["boituva"]):
            args = boituva.parse_args()
            self.assertEqual(args.url, boituva.BASE_URL)
            self.assertEqual(args.term, [])
            self.assertFalse(args.force)

        captured = {}

        def fake_run_crawler(*args, **kwargs):
            captured["args"] = args
            captured["kwargs"] = kwargs
            return 0

        with patch.object(boituva, "run_crawler", side_effect=fake_run_crawler), patch.object(
            sys, "argv", ["boituva", "--url", "https://example.com", "--term", "alpha", "--term", "beta", "--force"]
        ):
            self.assertEqual(boituva.main(), 0)

        self.assertIs(captured["args"][0], BoituvaCrawler)
        self.assertEqual(captured["kwargs"]["base_url"], "https://example.com")
        self.assertEqual(captured["kwargs"]["crawler_kwargs"]["target_terms"], ("alpha", "beta"))
        self.assertTrue(captured["kwargs"]["force"])

    def test_sorocaba_parse_args_and_main(self) -> None:
        with patch.object(sys, "argv", ["sorocaba"]):
            args = sorocaba.parse_args()
            self.assertEqual(args.url, sorocaba.BASE_URL)
            self.assertEqual(args.term, [])
            self.assertFalse(args.force)

        captured = {}

        def fake_run_crawler(*args, **kwargs):
            captured["args"] = args
            captured["kwargs"] = kwargs
            return 0

        with patch.object(sorocaba, "run_crawler", side_effect=fake_run_crawler), patch.object(
            sys, "argv", ["sorocaba", "--term", "gamma"]
        ):
            self.assertEqual(sorocaba.main(), 0)

        self.assertIs(captured["args"][0], SorocabaCrawler)
        self.assertEqual(captured["kwargs"]["crawler_kwargs"]["target_terms"], ("gamma",))

    def test_run_crawlers_setup_logging_run_job_and_main(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / "logs"
            log_file = log_dir / "run_crawlers.log"

            with patch.object(run_crawlers, "LOG_DIR", log_dir), patch.object(
                run_crawlers, "LOG_FILE", log_file
            ), patch.object(run_crawlers.logging, "basicConfig") as basic_config:
                run_crawlers.setup_logging()

            self.assertTrue(log_dir.exists())
            basic_config.assert_called_once()

        class Result:
            def __init__(self, returncode: int) -> None:
                self.returncode = returncode

        with patch.object(run_crawlers.subprocess, "run", return_value=Result(0)) as run:
            status = run_crawlers.run_job("boituva", Path("diario_oficial/apps/boituva.py"), ["--force"])

        self.assertEqual(status, 0)
        self.assertIn("-m", run.call_args.args[0])

        with patch.object(run_crawlers.subprocess, "run", return_value=Result(7)):
            status = run_crawlers.run_job("boituva", Path("diario_oficial/apps/boituva.py"), [])
        self.assertEqual(status, 7)

        with patch.object(run_crawlers, "setup_logging"), patch.object(
            run_crawlers, "CRAWLER_JOBS", [CrawlerJob(name="one", script=Path("one.py")), CrawlerJob(name="two", script=Path("two.py"))]
        ), patch.object(run_crawlers, "run_job", side_effect=[0, 3]) as run_job:
            self.assertEqual(run_crawlers.main(), 3)

        self.assertEqual(run_job.call_count, 2)

    def test_entrypoint_path_injection_can_run(self) -> None:
        root_dir = Path(__file__).resolve().parents[1]
        original_sys_path = list(sys.path)

        try:
            sys.path = [item for item in sys.path if Path(item).resolve() != root_dir]

            import diario_oficial.apps.boituva as boituva_module
            import diario_oficial.apps.sorocaba as sorocaba_module

            importlib.reload(boituva_module)
            importlib.reload(sorocaba_module)

            self.assertIn(str(root_dir), sys.path)
        finally:
            sys.path = original_sys_path
