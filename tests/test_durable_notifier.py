from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from diario_oficial.models import EditionResult
from diario_oficial.services.durable_notifier import DurableNotifier


def edition(number: str = "10") -> EditionResult:
    return EditionResult(
        number=number, date="2026-10-15", url=f"https://example.org/{number}",
        source_name="Boituva", status="match", matched_terms=["alpha"],
        saved_pdf=None, checked_at="2026-10-15T00:00:00",
    )


class DurableNotifierTests(unittest.TestCase):
    def test_retries_pending_and_never_resends_delivered(self):
        with tempfile.TemporaryDirectory() as tmp, patch(
            "diario_oficial.services.durable_notifier.TelegramNotifier"
        ) as notifier_type:
            sender = notifier_type.return_value
            notifier_type._build_message.return_value = "alert"
            sender._send_message.side_effect = [False, True]
            state_file = Path(tmp) / "state" / "edicoes.json"

            first = DurableNotifier(state_file)
            first.notify(edition())
            first.notify(edition())
            self.assertEqual(len(first.pending), 1)
            first.close()
            self.assertEqual(len(first.pending), 1)

            second = DurableNotifier(state_file)
            second.notify(edition())
            second.close()
            self.assertEqual(len(second.pending), 0)
            self.assertEqual(len(second.delivered), 1)

            third = DurableNotifier(state_file)
            third.notify(edition())
            third.close()
            self.assertEqual(sender._send_message.call_count, 2)
            self.assertEqual(sender.close.call_count, 3)

    def test_corrupted_outbox_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp, patch(
            "diario_oficial.services.durable_notifier.TelegramNotifier"
        ):
            path = Path(tmp) / "state" / "notifications" / "edicoes.json"
            path.parent.mkdir(parents=True)
            path.write_text('{"pending":[],"delivered":[]}')
            with self.assertRaises(ValueError):
                DurableNotifier(Path(tmp) / "state" / "edicoes.json")

    def test_notification_identity_is_stable(self):
        self.assertEqual(DurableNotifier.key(edition()), DurableNotifier.key(edition()))
        self.assertNotEqual(DurableNotifier.key(edition()), DurableNotifier.key(edition("11")))

    def test_pending_persisted_before_send(self):
        with tempfile.TemporaryDirectory() as tmp, patch(
            "diario_oficial.services.durable_notifier.TelegramNotifier"
        ) as notifier_type:
            notifier_type._build_message.return_value = "alert"
            notifier_type.return_value._send_message.return_value = False
            store = DurableNotifier(Path(tmp) / "state" / "edicoes.json")
            store.notify(edition())
            data = json.loads(store.path.read_text())
            self.assertEqual(len(data["pending"]), 1)
            store.close()
