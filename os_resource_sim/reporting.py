from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def export_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def export_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = sorted({k for row in rows for k in row.keys()})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def to_markdown(title: str, data: dict[str, Any]) -> str:
    lines = [f"# {title}", "", "## Metrics", ""]
    for key, value in data.get("metrics", {}).items():
        lines.append(f"- **{key}**: {value}")
    if "details" in data:
        lines.extend(["", "## Details", "", "```json", json.dumps(data["details"], indent=2), "```"])
    lines.append("")
    return "\n".join(lines)


def export_markdown(title: str, payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(to_markdown(title, payload), encoding="utf-8")
