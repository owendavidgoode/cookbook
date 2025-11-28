"""Calendar helpers for candidate generation and snapshots."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from . import paths


def canonical_calendar_path() -> Path:
    return paths.data_path("johndcook_calendar_365.csv")


def snapshot_final(destination_dir: Path | None = None) -> Path:
    """Copy the canonical 365 file to a timestamped snapshot without altering the source."""
    src = canonical_calendar_path()
    dest_dir = destination_dir or paths.data_path("calendar", "final")
    dest_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    dest = dest_dir / f"johndcook_calendar_365-{timestamp}.csv"
    shutil.copy2(src, dest)
    return dest


def run_candidate_generator(version: str = "v4") -> Path:
    """Run an existing candidate generator script and return the output path."""
    # We reuse the latest generator as default; others can be chosen explicitly.
    if version == "v4":
        from src import generate_calendar_candidates as gen

        gen.main()
        return Path(gen.OUT)
    if version == "v3":
        from src import generate_calendar_candidates_v3 as gen

        gen.main()
        return Path(gen.OUT)
    raise ValueError(f"Unknown generator version: {version}")
