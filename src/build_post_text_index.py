#!/usr/bin/env python3
"""Build a lightweight text index from enriched posts.

Outputs JSONL with:
- id, title, link, date, slug
- plain_text (HTML stripped)
- word_count (from plain text)
- link_count, image_count (from HTML)
- symbols: counts of π, φ, Φ, ∞ in text
- tokens: lowercased alphabetic tokens (no stopword filtering here)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import List

SRC = Path("data/johndcook_posts_enriched.jsonl")
OUT = Path("data/johndcook_text_index.jsonl")


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: List[str] = []
        self.link_count = 0
        self.image_count = 0

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.link_count += 1
        if tag == "img":
            self.image_count += 1

    def handle_data(self, data):
        self.parts.append(data)

    def text(self) -> str:
        return " ".join(self.parts)


def tokenize(text: str) -> List[str]:
    return [t for t in re.split(r"[^A-Za-z]+", text.lower()) if t]


def symbol_counts(text: str) -> dict:
    return {
        "pi": text.count("π"),
        "phi": text.count("φ"),
        "Phi": text.count("Φ"),
        "infty": text.count("∞"),
    }


@dataclass
class PostIndex:
    id: int
    title: str
    link: str
    date: str
    slug: str
    plain_text: str
    word_count: int
    link_count: int
    image_count: int
    symbols: dict
    tokens: List[str]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with SRC.open() as f_in, OUT.open("w", encoding="utf-8") as f_out:
        for line in f_in:
            obj = json.loads(line)
            content = obj.get("content") or ""
            parser = TextExtractor()
            parser.feed(content)
            parser.close()
            text = parser.text()
            tokens = tokenize(text)
            wc = len(tokens)
            sym = symbol_counts(text)
            record = {
                "id": obj.get("id"),
                "title": obj.get("title") or "",
                "link": obj.get("link") or "",
                "date": obj.get("date") or "",
                "slug": obj.get("slug") or "",
                "plain_text": text.strip(),
                "word_count": wc,
                "link_count": parser.link_count,
                "image_count": parser.image_count,
                "symbols": sym,
                "tokens": tokens,
            }
            f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
            written += 1
    print(f"Wrote {written} records to {OUT}")


if __name__ == "__main__":
    main()
