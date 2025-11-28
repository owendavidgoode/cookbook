"""Lightweight data models used across the calendar, bot, and book pipelines."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass(slots=True)
class Post:
    id: int
    title: str
    link: str
    date: datetime
    word_count: int
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    slug: str = ""
    content: Optional[str] = None
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Fact:
    id: int
    type: str
    fact: str
    source_link: str | None = None
    date: str | None = None
    slug: str | None = None
    source_file: str | None = None
