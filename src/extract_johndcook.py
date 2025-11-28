#!/usr/bin/env python3
"""Extract blog content from the downloaded johndcook.com site."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, List, Optional
from urllib.parse import urlparse


BLOCK_TAGS = {"p", "li", "h1", "h2", "h3", "pre", "blockquote"}


@dataclass
class ParsedPage:
    canonical: Optional[str]
    title: Optional[str]
    description: Optional[str]
    blocks: List[dict]


class MainContentParser(HTMLParser):
    """Minimal HTML extractor tailored to johndcook.com pages."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title_parts: List[str] = []
        self.description: Optional[str] = None
        self.canonical: Optional[str] = None
        self.in_main = False
        self.main_depth = 0
        self.skip_depth = 0
        self.block_stack: List[dict] = []
        self.blocks: List[dict] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs_dict = {k.lower(): v for k, v in attrs}

        if tag == "title":
            self.in_title = True

        if tag == "meta" and attrs_dict.get("name", "").lower() == "description":
            self.description = attrs_dict.get("content")

        rel_value = attrs_dict.get("rel", "")
        if tag == "link" and rel_value.lower() == "canonical":
            href = attrs_dict.get("href")
            if href:
                if self.canonical is None or "/blog/" in href:
                    self.canonical = href

        if tag == "div" and attrs_dict.get("id") == "main":
            self.in_main = True
            self.main_depth = 1
            return

        if self.in_main and tag == "div":
            self.main_depth += 1

        if not self.in_main:
            return

        if tag in {"script", "style"}:
            self.skip_depth += 1
            return

        if self.skip_depth > 0:
            return

        if tag in BLOCK_TAGS:
            self.block_stack.append({"tag": tag, "parts": []})
        elif tag == "br" and self.block_stack:
            self.block_stack[-1]["parts"].append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

        if tag in {"script", "style"} and self.skip_depth > 0:
            self.skip_depth -= 1
            return

        if self.in_main and tag == "div":
            self.main_depth -= 1
            if self.main_depth <= 0:
                self.in_main = False
            return

        if not self.in_main or self.skip_depth > 0:
            return

        if tag in BLOCK_TAGS and self.block_stack:
            block = self.block_stack.pop()
            text = "".join(block["parts"])
            if block["tag"] != "pre":
                text = " ".join(text.split())
            else:
                text = text.strip("\n")
            if text.strip():
                self.blocks.append({"tag": block["tag"], "text": text.strip()})

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data.strip())

        if not self.in_main or self.skip_depth > 0 or not self.block_stack:
            return

        self.block_stack[-1]["parts"].append(data)


def parse_html(path: Path) -> ParsedPage:
    parser = MainContentParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    parser.close()

    title = " ".join(part for part in parser.title_parts if part).strip() or None
    return ParsedPage(
        canonical=parser.canonical,
        title=title,
        description=parser.description,
        blocks=parser.blocks,
    )


def is_blog_page(canonical: Optional[str], path: Path) -> bool:
    if canonical and "/blog/" in canonical:
        return True
    return "/blog/" in str(path)


def slug_from_canonical(canonical: Optional[str], path: Path) -> str:
    if canonical:
        parsed = urlparse(canonical)
        slug_path = parsed.path.strip("/")
        if slug_path.startswith("blog/"):
            slug_path = slug_path[len("blog/") :]
        return slug_path or path.stem
    return path.stem


def should_drop_block(block: dict) -> bool:
    text = block["text"].strip().lower()
    if not text:
        return True
    if block["tag"] == "p" and text in {"home", "contact"}:
        return True
    return False


def summarize(blocks: List[dict], word_limit: int = 60) -> Optional[str]:
    for block in blocks:
        if block["tag"] in {"p", "li", "blockquote"}:
            words = block["text"].split()
            if not words:
                continue
            excerpt = " ".join(words[:word_limit])
            if len(words) > word_limit:
                excerpt += " ..."
            return excerpt
    return None


def build_entry(path: Path, page: ParsedPage) -> Optional[dict]:
    if not is_blog_page(page.canonical, path):
        return None

    filtered_blocks = [b for b in page.blocks if not should_drop_block(b)]
    content = "\n\n".join(block["text"] for block in filtered_blocks)
    heading = next((b["text"] for b in filtered_blocks if b["tag"] == "h1"), None)

    return {
        "slug": slug_from_canonical(page.canonical, path),
        "canonical_url": page.canonical,
        "source_path": str(path),
        "title": page.title,
        "heading": heading,
        "description": page.description,
        "summary": summarize(filtered_blocks),
        "word_count": len(content.split()),
        "blocks": filtered_blocks,
        "content": content,
    }


def iter_html_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*.html")):
        yield path


def write_jsonl(entries: Iterable[dict], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    default_source = (repo_root.parent / "johndcook" / "app" / "public").resolve()
    default_output = (repo_root / "data" / "johndcook_posts.jsonl").resolve()

    parser = argparse.ArgumentParser(
        description="Extract blog posts from a downloaded johndcook.com site."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=default_source,
        help="Path to the downloaded site root (default: %(default)s)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output,
        help="Where to write JSONL output (default: %(default)s)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limit number of files processed (0 means no limit).",
    )

    args = parser.parse_args()
    source_root: Path = args.source

    html_files = list(iter_html_files(source_root))
    if args.limit:
        html_files = html_files[: args.limit]

    entries: List[dict] = []
    for path in html_files:
        parsed = parse_html(path)
        entry = build_entry(path, parsed)
        if entry:
            entries.append(entry)

    write_jsonl(entries, args.output)
    print(f"Wrote {len(entries)} blog entries to {args.output}")


if __name__ == "__main__":
    main()
