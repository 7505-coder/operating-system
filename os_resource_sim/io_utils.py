from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any


def load_json_or_csv(path: str) -> Any:
    if path == "-":
        import sys

        content = sys.stdin.read().strip()
        if not content:
            raise ValueError("No input received from stdin")
        return _parse_text(content)

    input_path = Path(path)
    if not input_path.exists():
        raise ValueError(f"Input file not found: {path}")
    text = input_path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("Input file is empty")
    if input_path.suffix.lower() == ".csv":
        return _parse_csv(text)
    if input_path.suffix.lower() == ".json":
        return json.loads(text)
    return _parse_text(text)


def _parse_text(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return _parse_csv(text)


def _parse_csv(text: str) -> list[dict[str, Any]]:
    reader = csv.DictReader(io.StringIO(text))
    rows = [dict(row) for row in reader]
    if not reader.fieldnames:
        raise ValueError("CSV must include headers")
    return rows
