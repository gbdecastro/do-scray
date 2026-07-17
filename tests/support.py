from __future__ import annotations

import types
from dataclasses import dataclass, field
from typing import Any, Callable


class FakeResponse:
    def __init__(
        self,
        *,
        text: str = "",
        chunks: list[bytes] | None = None,
        json_data: dict[str, Any] | None = None,
        raise_for_status_exc: Exception | None = None,
    ) -> None:
        self.text = text
        self.apparent_encoding = None
        self.encoding = None
        self._chunks = chunks or []
        self._json_data = json_data or {"ok": True}
        self._raise_for_status_exc = raise_for_status_exc

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def raise_for_status(self) -> None:
        if self._raise_for_status_exc is not None:
            raise self._raise_for_status_exc

    def iter_content(self, chunk_size: int):
        yield from self._chunks

    def json(self) -> dict[str, Any]:
        return self._json_data


class FakeSession:
    def __init__(self, responses: dict[tuple[str, bool], FakeResponse] | None = None) -> None:
        self.headers: dict[str, str] = {}
        self.responses = responses or {}
        self.calls: list[tuple[str, bool, int | None]] = []

    def get(self, url: str, timeout: int | None = None, stream: bool = False) -> FakeResponse:
        self.calls.append((url, stream, timeout))
        key = (url, stream)
        if key not in self.responses:
            raise AssertionError(f"Unexpected request: {key}")
        return self.responses[key]


@dataclass
class MemoryStateStore:
    initial_state: dict[str, dict[str, object]] = field(default_factory=dict)
    loaded: int = 0
    saved_payloads: list[dict[str, dict[str, object]]] = field(default_factory=list)

    def load(self) -> dict[str, dict[str, object]]:
        self.loaded += 1
        return dict(self.initial_state)

    def save(self, editions: dict[str, dict[str, object]]) -> None:
        self.saved_payloads.append(editions)


@dataclass
class MemoryNotifier:
    notifications: list[Any] = field(default_factory=list)
    closed: int = 0

    def notify(self, result: Any) -> None:
        self.notifications.append(result)

    def close(self) -> None:
        self.closed += 1


class StreamlitBlock:
    def __init__(self, label: str = "") -> None:
        self.label = label
        self.metrics: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
        self.subheaders: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
        self.downloads: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
        self.writes: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    def __enter__(self) -> "StreamlitBlock":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def metric(self, *args: Any, **kwargs: Any) -> None:
        self.metrics.append((args, kwargs))

    def subheader(self, *args: Any, **kwargs: Any) -> None:
        self.subheaders.append((args, kwargs))

    def download_button(self, *args: Any, **kwargs: Any) -> None:
        self.downloads.append((args, kwargs))

    def write(self, *args: Any, **kwargs: Any) -> None:
        self.writes.append((args, kwargs))


class StreamlitStub(types.ModuleType):
    def __init__(self) -> None:
        super().__init__("streamlit")
        self.selected_value: Any = None
        self.calls: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []

    def set_page_config(self, *args: Any, **kwargs: Any) -> None:
        self.calls.append(("set_page_config", args, kwargs))

    def title(self, *args: Any, **kwargs: Any) -> None:
        self.calls.append(("title", args, kwargs))

    def caption(self, *args: Any, **kwargs: Any) -> None:
        self.calls.append(("caption", args, kwargs))

    def info(self, *args: Any, **kwargs: Any) -> None:
        self.calls.append(("info", args, kwargs))

    def metric(self, *args: Any, **kwargs: Any) -> None:
        self.calls.append(("metric", args, kwargs))

    def write(self, *args: Any, **kwargs: Any) -> None:
        self.calls.append(("write", args, kwargs))

    def code(self, *args: Any, **kwargs: Any) -> None:
        self.calls.append(("code", args, kwargs))

    def dataframe(self, *args: Any, **kwargs: Any) -> None:
        self.calls.append(("dataframe", args, kwargs))

    def download_button(self, *args: Any, **kwargs: Any) -> None:
        self.calls.append(("download_button", args, kwargs))

    def subheader(self, *args: Any, **kwargs: Any) -> None:
        self.calls.append(("subheader", args, kwargs))

    def selectbox(self, *args: Any, **kwargs: Any) -> Any:
        self.calls.append(("selectbox", args, kwargs))
        if self.selected_value is not None:
            return self.selected_value

        options = args[1] if len(args) > 1 else kwargs.get("options", [])
        return options[0] if options else None

    def columns(self, spec: Any) -> list[StreamlitBlock]:
        self.calls.append(("columns", (spec,), {}))
        count = spec if isinstance(spec, int) else len(spec)
        return [StreamlitBlock(f"column-{index}") for index in range(count)]

    def tabs(self, labels: list[str]) -> list[StreamlitBlock]:
        self.calls.append(("tabs", (labels,), {}))
        return [StreamlitBlock(label) for label in labels]

    def expander(self, label: str, expanded: bool = False) -> StreamlitBlock:
        self.calls.append(("expander", (label,), {"expanded": expanded}))
        return StreamlitBlock(label)
