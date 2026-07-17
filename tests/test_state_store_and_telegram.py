from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

from diario_oficial.models import EditionResult
from diario_oficial.services import JsonStateStore, TelegramNotifier


class JsonStateStoreTest(unittest.TestCase):
    def test_load_handles_missing_corrupt_and_invalid_payloads(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / "state.json"
            store = JsonStateStore(state_file)

            self.assertEqual(store.load(), {})

            state_file.write_text("{not-json}", encoding="utf-8")
            self.assertEqual(store.load(), {})

            state_file.write_text(json.dumps({"editions": []}), encoding="utf-8")
            self.assertEqual(store.load(), {})

            state_file.write_text(json.dumps(["invalid"]), encoding="utf-8")
            self.assertEqual(store.load(), {})

    def test_save_writes_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = Path(tmpdir) / "state.json"
            store = JsonStateStore(state_file)
            store.save(
                {
                    "1": {
                        "number": "1",
                        "status": "match",
                        "matched_terms": ["term"],
                    }
                }
            )

            payload = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertIn("updated_at", payload)
            self.assertEqual(payload["editions"]["1"]["status"], "match")
            self.assertEqual(payload["editions"]["1"]["matched_terms"], ["term"])


class TelegramNotifierTest(unittest.TestCase):
    def test_build_message_with_and_without_pdf(self) -> None:
        result_with_pdf = EditionResult(
            number="12",
            date="2024-02-03",
            url="https://example.com/12",
            source_name="Boituva",
            status="match",
            matched_terms=["alpha", "beta"],
            saved_pdf=Path("saved.pdf"),
            checked_at="2024-02-03T10:00:00",
        )
        message = TelegramNotifier._build_message(result_with_pdf)
        self.assertIn("COM MATCH", message)
        self.assertIn("Termos encontrados: alpha, beta", message)
        self.assertIn("PDF salvo: saved.pdf", message)

        result_without_pdf = EditionResult(
            number="13",
            date="",
            url="https://example.com/13",
            source_name="Sorocaba",
            status="no_match",
            matched_terms=[],
            saved_pdf=None,
            checked_at="2024-02-03T10:00:00",
        )
        message = TelegramNotifier._build_message(result_without_pdf)
        self.assertIn("SEM MATCH", message)
        self.assertIn("Data: data desconhecida", message)
        self.assertIn("Termos encontrados: nenhum", message)

    def test_send_message_without_configuration(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            notifier = TelegramNotifier(token=None, chat_id=None)
            try:
                self.assertFalse(notifier.is_configured())
                self.assertFalse(notifier._send_message("hello"))
            finally:
                notifier.close()

    def test_send_message_success_failure_and_exception(self) -> None:
        notifier = TelegramNotifier(token="token", chat_id="chat", request_timeout_seconds=1)
        try:
            with patch("diario_oficial.services.telegram_service.requests.post") as post:
                response = type("Response", (), {
                    "raise_for_status": lambda self: None,
                    "json": lambda self: {"ok": True},
                })()
                post.return_value = response
                self.assertTrue(notifier._send_message("hello"))

            with patch("diario_oficial.services.telegram_service.requests.post") as post:
                response = type("Response", (), {
                    "raise_for_status": lambda self: None,
                    "json": lambda self: {"ok": False},
                })()
                post.return_value = response
                self.assertFalse(notifier._send_message("hello"))

            with patch(
                "diario_oficial.services.telegram_service.requests.post",
                side_effect=requests.RequestException("boom"),
            ):
                self.assertFalse(notifier._send_message("hello"))
        finally:
            notifier.close()

    def test_notify_and_close_process_queue(self) -> None:
        result = EditionResult(
            number="42",
            date="2024-02-03",
            url="https://example.com/42",
            source_name="Boituva",
            status="match",
            matched_terms=["term"],
            saved_pdf=None,
            checked_at="2024-02-03T10:00:00",
        )

        notifier = TelegramNotifier(
            token="token",
            chat_id="chat",
            repeat_count=2,
            repeat_interval_seconds=0,
        )
        calls: list[str] = []
        notifier._send_message = lambda message: calls.append(message) or True  # type: ignore[method-assign]

        notifier.notify(result)
        notifier._queue.join()
        notifier.close()
        notifier.close()

        self.assertEqual(len(calls), 2)
        self.assertTrue(notifier._closed)

        no_match_result = EditionResult(
            number="43",
            date="2024-02-03",
            url="https://example.com/43",
            source_name="Sorocaba",
            status="no_match",
            matched_terms=[],
            saved_pdf=None,
            checked_at="2024-02-03T10:00:00",
        )

        another = TelegramNotifier(
            token="token",
            chat_id="chat",
            repeat_count=3,
            repeat_interval_seconds=0,
        )
        second_calls: list[str] = []
        another._send_message = lambda message: second_calls.append(message) or True  # type: ignore[method-assign]
        another.notify(no_match_result)
        another._queue.join()
        another.close()

        self.assertEqual(len(second_calls), 1)
