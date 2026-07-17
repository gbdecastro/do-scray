from __future__ import annotations

import json
from collections import deque
from datetime import datetime
from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT_DIR / "logs"
STATE_DIR = ROOT_DIR / "state"
OUTPUT_DIR = ROOT_DIR / "DO"


st.set_page_config(
    page_title="Diário Oficial Scraper",
    page_icon="📰",
    layout="wide",
)


def format_dt(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def read_tail(path: Path, limit: int = 200) -> str:
    if not path.exists():
        return "Arquivo não encontrado."

    lines: deque[str] = deque(maxlen=limit)
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            lines.append(line.rstrip("\n"))
    return "\n".join(lines)


def list_log_files() -> list[Path]:
    if not LOG_DIR.exists():
        return []
    return sorted(LOG_DIR.glob("*.log"), key=lambda item: item.stat().st_mtime, reverse=True)


def list_pdf_files() -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    if not OUTPUT_DIR.exists():
        return files

    for path in sorted(
        OUTPUT_DIR.rglob("*.pdf"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    ):
        city = path.parent.name if path.parent != OUTPUT_DIR else "Sem cidade"
        files.append((city, path))
    return files


def load_state_summary() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not STATE_DIR.exists():
        return rows

    for path in sorted(STATE_DIR.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        editions = payload.get("editions", {}) if isinstance(payload, dict) else {}
        if not isinstance(editions, dict):
            editions = {}

        match_count = sum(1 for item in editions.values() if isinstance(item, dict) and item.get("status") == "match")
        no_match_count = sum(1 for item in editions.values() if isinstance(item, dict) and item.get("status") == "no_match")
        updated_at = payload.get("updated_at", "desconhecido") if isinstance(payload, dict) else "desconhecido"
        rows.append(
            {
                "arquivo": path.name,
                "edicoes": str(len(editions)),
                "matches": str(match_count),
                "sem_match": str(no_match_count),
                "atualizado_em": str(updated_at),
            }
        )

    return rows


def render_header() -> None:
    st.title("Diário Oficial Scraper")
    st.caption("Painel simples para acompanhar logs, estados e PDFs gerados pelos crawlers.")


def render_metrics() -> None:
    log_files = list_log_files()
    pdf_files = list_pdf_files()
    state_files = list(STATE_DIR.glob("*.json")) if STATE_DIR.exists() else []

    col1, col2, col3 = st.columns(3)
    col1.metric("Arquivos de log", len(log_files))
    col2.metric("PDFs salvos", len(pdf_files))
    col3.metric("Arquivos de estado", len(state_files))


def render_logs() -> None:
    log_files = list_log_files()
    if not log_files:
        st.info("Nenhum log encontrado ainda.")
        return

    selected = st.selectbox(
        "Escolha um log para visualizar",
        log_files,
        format_func=lambda item: f"{item.name} · {format_dt(item.stat().st_mtime)}",
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(selected.name)
    with col2:
        st.download_button(
            "Baixar log",
            data=selected.read_bytes(),
            file_name=selected.name,
            mime="text/plain",
            use_container_width=True,
        )

    st.code(read_tail(selected, 250), language="text")


def render_outputs() -> None:
    pdf_files = list_pdf_files()
    if not pdf_files:
        st.info("Ainda não existem PDFs salvos com match.")
        return

    for city, path in pdf_files:
        with st.expander(f"{city} · {path.name}", expanded=False):
            st.write(f"Atualizado em: {format_dt(path.stat().st_mtime)}")
            st.download_button(
                "Baixar PDF",
                data=path.read_bytes(),
                file_name=path.name,
                mime="application/pdf",
                key=str(path),
            )


def render_states() -> None:
    rows = load_state_summary()
    if not rows:
        st.info("Nenhum estado salvo ainda.")
        return

    st.dataframe(rows, use_container_width=True, hide_index=True)


def main() -> None:
    render_header()
    render_metrics()

    tab_logs, tab_outputs, tab_states = st.tabs(["Logs", "PDFs", "Estados"])

    with tab_logs:
        render_logs()

    with tab_outputs:
        render_outputs()

    with tab_states:
        render_states()


main()
