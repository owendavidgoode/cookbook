"""Path helpers to keep data locations centralized."""

from __future__ import annotations

import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = Path(os.environ.get("COOKBOOK_DATA_DIR", REPO_ROOT / "data")).resolve()
BOT_DIR = REPO_ROOT / "bot"


def data_path(*parts: str) -> Path:
    """Return a path under the configured data directory."""
    return DATA_ROOT.joinpath(*parts)


def repo_path(*parts: str) -> Path:
    """Return a path under the repository root."""
    return REPO_ROOT.joinpath(*parts)
