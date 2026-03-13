"""JSON file store for lightweight local persistence."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


def _serialize(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if is_dataclass(value):
        return {key: _serialize(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    return value


class JsonStore:
    """Small JSON persistence helper for file-backed repositories."""

    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write(self, relative_path: str | Path, payload: dict[str, Any]) -> None:
        target = self.base_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(_serialize(payload), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def read(self, relative_path: str | Path) -> dict[str, Any] | None:
        target = self.base_dir / relative_path
        if not target.exists():
            return None
        return json.loads(target.read_text(encoding="utf-8"))
