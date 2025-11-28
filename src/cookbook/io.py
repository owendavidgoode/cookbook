"""Common file IO helpers."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Iterator


def read_jsonl(path: Path) -> Iterator[dict]:
    """Yield JSON objects from a JSONL file."""
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    """Write an iterable of objects to JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_csv_rows(path: Path) -> list[dict]:
    """Read a CSV into a list of dicts."""
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv_rows(path: Path, fieldnames: list[str], rows: Iterable[dict]) -> None:
    """Write rows to CSV with the given fieldnames."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
