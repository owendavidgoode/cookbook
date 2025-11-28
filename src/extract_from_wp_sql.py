#!/usr/bin/env python3
"""Extract published WordPress posts from a MySQL dump."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


POST_COLUMNS = [
    "ID",
    "post_author",
    "post_date",
    "post_date_gmt",
    "post_content",
    "post_title",
    "post_excerpt",
    "post_status",
    "comment_status",
    "ping_status",
    "post_password",
    "post_name",
    "to_ping",
    "pinged",
    "post_modified",
    "post_modified_gmt",
    "post_content_filtered",
    "post_parent",
    "guid",
    "menu_order",
    "post_type",
    "post_mime_type",
    "comment_count",
]


@dataclass
class PostRow:
    id: int
    slug: str
    title: str
    content: str
    excerpt: str
    status: str
    post_type: str
    guid: str
    date: str
    modified: str


def unescape_mysql(value: str) -> str:
    """Unescape common MySQL string escapes."""
    return (
        value.replace("\\'", "'")
        .replace('\\"', '"')
        .replace("\\n", "\n")
        .replace("\\r", "\r")
        .replace("\\t", "\t")
        .replace("\\\\", "\\")
    )


def split_fields(row: str) -> List[str]:
    """Split a single parenthesis-stripped row into fields respecting quotes."""
    fields: List[str] = []
    current: List[str] = []
    in_str = False
    escape = False

    for ch in row:
        if escape:
            current.append(ch)
            escape = False
            continue
        if ch == "\\" and in_str:
            escape = True
            continue
        if ch == "'" and not in_str:
            in_str = True
            continue
        if ch == "'" and in_str:
            in_str = False
            continue
        if ch == "," and not in_str:
            fields.append("".join(current))
            current = []
            continue
        current.append(ch)

    fields.append("".join(current))
    return fields


def parse_row(row: str) -> Optional[PostRow]:
    """Parse a single row string (without surrounding parentheses) into PostRow."""
    fields = split_fields(row)
    if len(fields) != len(POST_COLUMNS):
        return None

    def clean(val: str) -> Optional[str]:
        val = val.strip()
        if val == "NULL":
            return None
        return unescape_mysql(val)

    data = {col: clean(val) for col, val in zip(POST_COLUMNS, fields)}
    try:
        post_id = int(data["ID"] or 0)
    except ValueError:
        return None

    return PostRow(
        id=post_id,
        slug=data["post_name"] or "",
        title=data["post_title"] or "",
        content=data["post_content"] or "",
        excerpt=data["post_excerpt"] or "",
        status=data["post_status"] or "",
        post_type=data["post_type"] or "",
        guid=data["guid"] or "",
        date=data["post_date"] or "",
        modified=data["post_modified"] or "",
    )


def iter_rows_from_insert(values_part: str) -> Iterable[str]:
    """Yield row substrings from the VALUES portion of an INSERT, respecting quotes."""
    current: List[str] = []
    in_str = False
    escape = False

    i = 0
    length = len(values_part)
    while i < length:
        ch = values_part[i]
        next_two = values_part[i : i + 3]

        if escape:
            current.append(ch)
            escape = False
            i += 1
            continue

        if ch == "\\" and in_str:
            escape = True
            i += 1
            continue

        if ch == "'" and not in_str:
            in_str = True
            current.append(ch)
            i += 1
            continue
        if ch == "'" and in_str:
            in_str = False
            current.append(ch)
            i += 1
            continue

        if not in_str and next_two == "),(":
            yield "".join(current).strip().strip("()")
            current = []
            i += 3
            continue

        current.append(ch)
        i += 1

    if current:
        yield "".join(current).strip().strip("()")


def parse_dump_line(line: str) -> Iterable[PostRow]:
    if not line.startswith("INSERT INTO `wp_posts`"):
        return []
    try:
        _, values_part = line.split("VALUES", 1)
    except ValueError:
        return []
    values_part = values_part.strip().rstrip(";\n")
    rows = []
    for row_str in iter_rows_from_insert(values_part):
        parsed = parse_row(row_str)
        if parsed:
            rows.append(parsed)
    return rows


def extract_posts(dump_path: Path) -> List[PostRow]:
    posts: List[PostRow] = []
    with dump_path.open(errors="ignore") as f:
        for line in f:
            for row in parse_dump_line(line):
                if row.post_type == "post" and row.status == "publish":
                    posts.append(row)
    return posts


def write_jsonl(posts: Iterable[PostRow], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as f:
        for post in posts:
            content = unescape_mysql(post.content)
            excerpt = unescape_mysql(post.excerpt)
            record = {
                "id": post.id,
                "slug": post.slug,
                "title": post.title,
                "date": post.date,
                "modified": post.modified,
                "guid": post.guid,
                "content": content,
                "excerpt": excerpt,
                "word_count": len(content.split()),
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract published posts from a WordPress MySQL dump (wp_posts)."
    )
    repo_root = Path(__file__).resolve().parents[1]
    default_dump = repo_root.parent / "johndcook" / "app" / "public" / "wp_johndcook1-2024-07-05-bc4fb3d.sql"
    default_output = repo_root / "data" / "johndcook_posts_from_sql.jsonl"
    parser.add_argument("--dump", type=Path, default=default_dump)
    parser.add_argument("--output", type=Path, default=default_output)
    args = parser.parse_args()

    posts = extract_posts(args.dump)
    write_jsonl(posts, args.output)
    total_words = sum(len(unescape_mysql(p.content).split()) for p in posts)
    print(f"Exported {len(posts)} published posts to {args.output}")
    print(f"Approx total words: {total_words}")


if __name__ == "__main__":
    main()
