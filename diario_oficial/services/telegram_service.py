from __future__ import annotations

import logging
import queue
import os
import threading
import time

import requests

from ..models import EditionResult


class TelegramNotifier:
    def __init__(
        self,
        token: str | None = None,
        chat_id: str | None = None,
        repeat_count: int = 1,
        repeat_interval_seconds: int = 120,
        request_timeout_seconds: int = 10,
    ) -> None:
        self.token = token or os.getenv("TELEGRAM_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.repeat_count = repeat_count
        self.repeat_interval_seconds = repeat_interval_seconds
        self.request_timeout_seconds = request_timeout_seconds
        self._warned_missing_config = False
        self._queue: queue.Queue[tuple[str, int] | None] = queue.Queue()
        self._closed = False
        self._worker = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker.start()

    def is_configured(self) -> bool:
        return bool(self.token and self.chat_id)

    def notify(self, result: EditionResult) -> None:
        message = self._build_message(result)
        repeat_total = self.repeat_count if result.status == "match" else 1
        self._queue.put((message, repeat_total))

    def close(self) -> None:
        if self._closed:
            return

        self._closed = True
        self._queue.put(None)
        self._worker.join()

    def _worker_loop(self) -> None:
        while True:
            message = self._queue.get()
            try:
                if message is None:
                    return

                payload, repeat_total = message
                for attempt in range(repeat_total):
                    sent = self._send_message(payload)
                    if sent:
                        logging.info(
                            "Mensagem Telegram enviada (%d/%d).",
                            attempt + 1,
                            repeat_total,
                        )
                    else:
                        logging.warning(
                            "Falha ao enviar mensagem Telegram na tentativa %d/%d.",
                            attempt + 1,
                            repeat_total,
                        )

                    if attempt < repeat_total - 1:
                        time.sleep(self.repeat_interval_seconds)
            finally:
                self._queue.task_done()

    def _send_message(self, message: str) -> bool:
        if not self.is_configured():
            if not self._warned_missing_config:
                logging.warning(
                    "Telegram não configurado. Defina TELEGRAM_TOKEN e TELEGRAM_CHAT_ID."
                )
                self._warned_missing_config = True
            return False

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "disable_web_page_preview": False,
        }

        try:
            response = requests.post(url, data=payload, timeout=self.request_timeout_seconds)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            logging.exception("Erro ao enviar mensagem ao Telegram: %s", exc)
            return False

        if not data.get("ok"):
            logging.warning("Telegram retornou erro: %s", data)
            return False

        return True

    @staticmethod
    def _build_message(result: EditionResult) -> str:
        status_label = "COM MATCH" if result.status == "match" else "SEM MATCH"
        lines = [
            f"Diário Oficial {result.source_name} {status_label}",
            f"Edição: {result.number}",
            f"Data: {result.date or 'data desconhecida'}",
            f"Link: {result.url}",
        ]

        if result.matched_terms:
            lines.append(f"Termos encontrados: {', '.join(result.matched_terms)}")
        else:
            lines.append("Termos encontrados: nenhum")

        if result.saved_pdf is not None:
            lines.append(f"PDF salvo: {result.saved_pdf}")

        return "\n".join(lines)
