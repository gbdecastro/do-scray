from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.support import StreamlitStub


sys.modules.setdefault("streamlit", StreamlitStub())

import diario_oficial.dashboard as dashboard  # noqa: E402


class DashboardTest(unittest.TestCase):
    def test_format_dt_and_read_tail(self) -> None:
        self.assertEqual(dashboard.format_dt(0), "1969-12-31 21:00:00")

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "log.txt"
            self.assertEqual(dashboard.read_tail(path), "Arquivo não encontrado.")

            path.write_text("one\ntwo\nthree\n", encoding="utf-8")
            self.assertEqual(dashboard.read_tail(path, limit=2), "two\nthree")

    def test_list_files_and_state_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            log_dir = root / "logs"
            state_dir = root / "state"
            output_dir = root / "DO"
            log_dir.mkdir()
            state_dir.mkdir()
            output_dir.mkdir()

            log1 = log_dir / "a.log"
            log2 = log_dir / "b.log"
            log1.write_text("one", encoding="utf-8")
            log2.write_text("two", encoding="utf-8")
            os.utime(log1, (1, 1))
            os.utime(log2, (2, 2))

            pdf_root = output_dir / "root.pdf"
            pdf_city_dir = output_dir / "City"
            pdf_city_dir.mkdir()
            pdf_city = pdf_city_dir / "city.pdf"
            pdf_root.write_bytes(b"root")
            pdf_city.write_bytes(b"city")
            os.utime(pdf_root, (1, 1))
            os.utime(pdf_city, (3, 3))

            (state_dir / "valid.json").write_text(
                json.dumps(
                    {
                        "updated_at": "2024-01-01",
                        "editions": {
                            "1": {"status": "match"},
                            "2": {"status": "no_match"},
                            "3": {"status": "ignored"},
                        },
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "invalid.json").write_text("not-json", encoding="utf-8")
            (state_dir / "editions_list.json").write_text(
                json.dumps({"updated_at": "2024-01-01", "editions": []}),
                encoding="utf-8",
            )
            (state_dir / "plain_list.json").write_text(json.dumps([1, 2, 3]), encoding="utf-8")

            with patch.object(dashboard, "LOG_DIR", log_dir), patch.object(
                dashboard, "STATE_DIR", state_dir
            ), patch.object(dashboard, "OUTPUT_DIR", output_dir):
                log_files = dashboard.list_log_files()
                pdf_files = dashboard.list_pdf_files()
                state_rows = dashboard.load_state_summary()

        self.assertEqual([item.name for item in log_files], ["b.log", "a.log"])
        self.assertEqual([city for city, _ in pdf_files], ["City", "Sem cidade"])
        self.assertEqual(len(state_rows), 3)
        valid_row = next(row for row in state_rows if row["arquivo"] == "valid.json")
        self.assertEqual(valid_row["matches"], "1")
        self.assertEqual(valid_row["sem_match"], "1")

    def test_empty_dashboard_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            log_dir = root / "logs-missing"
            state_dir = root / "state-missing"
            output_dir = root / "DO-missing"

            dashboard.st.calls.clear()

            with patch.object(dashboard, "LOG_DIR", log_dir), patch.object(
                dashboard, "STATE_DIR", state_dir
            ), patch.object(dashboard, "OUTPUT_DIR", output_dir):
                self.assertEqual(dashboard.list_log_files(), [])
                self.assertEqual(dashboard.list_pdf_files(), [])
                self.assertEqual(dashboard.load_state_summary(), [])
                dashboard.render_metrics()
                dashboard.render_logs()
                dashboard.render_outputs()
                dashboard.render_states()

            call_names = [item[0] for item in dashboard.st.calls]
            self.assertIn("info", call_names)

    def test_render_functions_and_main(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            log_dir = root / "logs"
            state_dir = root / "state"
            output_dir = root / "DO"
            log_dir.mkdir()
            state_dir.mkdir()
            output_dir.mkdir()

            log_file = log_dir / "a.log"
            log_file.write_text("line-1\nline-2\n", encoding="utf-8")
            pdf_file = output_dir / "City" / "doc.pdf"
            pdf_file.parent.mkdir()
            pdf_file.write_bytes(b"pdf")
            state_file = state_dir / "valid.json"
            state_file.write_text(
                json.dumps({"updated_at": "2024-01-01", "editions": {"1": {"status": "match"}}}),
                encoding="utf-8",
            )

            dashboard.st.calls.clear()
            dashboard.st.selected_value = log_file

            with patch.object(dashboard, "LOG_DIR", log_dir), patch.object(
                dashboard, "STATE_DIR", state_dir
            ), patch.object(dashboard, "OUTPUT_DIR", output_dir):
                dashboard.render_header()
                dashboard.render_metrics()
                dashboard.render_logs()
                dashboard.render_outputs()
                dashboard.render_states()

            call_names = [item[0] for item in dashboard.st.calls]
            self.assertIn("title", call_names)
            self.assertIn("columns", call_names)
            self.assertIn("selectbox", call_names)
            self.assertIn("download_button", call_names)
            self.assertIn("dataframe", call_names)

            call_order: list[str] = []

            with patch.object(dashboard, "render_header", side_effect=lambda: call_order.append("header")), patch.object(
                dashboard, "render_metrics", side_effect=lambda: call_order.append("metrics")
            ), patch.object(dashboard, "render_logs", side_effect=lambda: call_order.append("logs")), patch.object(
                dashboard, "render_outputs", side_effect=lambda: call_order.append("outputs")
            ), patch.object(
                dashboard, "render_states", side_effect=lambda: call_order.append("states")
            ):
                dashboard.main()

            self.assertEqual(call_order, ["header", "metrics", "logs", "outputs", "states"])
