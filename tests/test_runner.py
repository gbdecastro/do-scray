from __future__ import annotations

import logging
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

from diario_oficial import runner
from tests.support import MemoryNotifier, MemoryStateStore


class RunnerTest(unittest.TestCase):
    def test_setup_logging_calls_basic_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "app.log"
            with patch.object(logging, "basicConfig") as basic_config, patch.object(
                logging, "FileHandler", return_value=object()
            ):
                runner.setup_logging(log_file)

            basic_config.assert_called_once()
            kwargs = basic_config.call_args.kwargs
            self.assertEqual(kwargs["level"], logging.INFO)
            self.assertEqual(len(kwargs["handlers"]), 2)

    def test_run_crawler_success_and_failure(self) -> None:
        class FakeSession:
            def __init__(self) -> None:
                self.headers: dict[str, str] = {}

        class SuccessCrawler:
            def __init__(self, **kwargs) -> None:
                self.kwargs = kwargs

            def run(self, force: bool = False) -> dict[str, int]:
                self.force = force
                return {"processed": 1, "skipped": 0, "match": 1, "no_match": 0}

        class FailureCrawler:
            def __init__(self, **kwargs) -> None:
                self.kwargs = kwargs

            def run(self, force: bool = False) -> dict[str, int]:
                raise requests.RequestException("boom")

        notifier_instances: list[MemoryNotifier] = []

        def notifier_factory(*args, **kwargs):
            notifier = MemoryNotifier()
            notifier_instances.append(notifier)
            return notifier

        store_instances: list[MemoryStateStore] = []

        def store_factory(state_file: Path):
            store = MemoryStateStore()
            store.state_file = state_file  # type: ignore[attr-defined]
            store_instances.append(store)
            return store

        with tempfile.TemporaryDirectory() as tmpdir, patch.object(runner, "setup_logging"), patch.object(
            runner.requests, "Session", return_value=FakeSession()
        ), patch.object(runner, "TelegramNotifier", side_effect=notifier_factory), patch.object(
            runner, "JsonStateStore", side_effect=store_factory
        ):
            output_dir = Path(tmpdir) / "out"
            state_file = Path(tmpdir) / "state.json"
            log_file = Path(tmpdir) / "log.txt"

            success = runner.run_crawler(
                SuccessCrawler,
                base_url="https://example.com",
                output_dir=output_dir,
                state_file=state_file,
                log_file=log_file,
                user_agent="UA",
                force=True,
                crawler_kwargs={"extra": "value"},
            )

            self.assertEqual(success, 0)
            self.assertEqual(len(notifier_instances), 1)
            self.assertEqual(notifier_instances[0].closed, 1)
            self.assertEqual(store_instances[0].state_file, state_file)  # type: ignore[attr-defined]

            failure = runner.run_crawler(
                FailureCrawler,
                base_url="https://example.com",
                output_dir=output_dir,
                state_file=state_file,
                log_file=log_file,
                user_agent="UA",
            )

            self.assertEqual(failure, 1)
            self.assertEqual(len(notifier_instances), 2)
            self.assertEqual(notifier_instances[1].closed, 2)
