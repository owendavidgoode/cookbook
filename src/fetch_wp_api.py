#!/usr/bin/env python3
"""Fetch all published posts via the WordPress REST API."""

from __future__ import annotations

import argparse
import json
import math
import ssl
from pathlib import Path
from typing import Iterable
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def fetch_page(base_url: str, page: int, per_page: int, verify_ssl: bool) -> tuple[list[dict], dict]:
    ctx = ssl.create_default_context()
    if not verify_ssl:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    params = {"per_page": per_page, "page": page}
    url = f"{base_url}?{urlencode(params)}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, context=ctx) as resp:
        data = json.load(resp)
        headers = {k.lower(): v for k, v in resp.getheaders()}
    return data, headers


def iter_posts(base_url: str, verify_ssl: bool) -> Iterable[dict]:
    per_page = 100
    first_page, headers = fetch_page(base_url, 1, per_page, verify_ssl)
    total = int(headers.get("x-wp-total", "0"))
    total_pages = int(headers.get("x-wp-totalpages", "1"))
    yield from first_page
    for page in range(2, total_pages + 1):
        data, _ = fetch_page(base_url, page, per_page, verify_ssl)
        yield from data


def normalize(post: dict) -> dict:
    rendered = post.get("content", {}).get("rendered", "") or ""
    title = post.get("title", {}).get("rendered", "") or ""
    excerpt = post.get("excerpt", {}).get("rendered", "") or ""
    return {
        "id": post.get("id"),
        "date": post.get("date"),
        "modified": post.get("modified"),
        "slug": post.get("slug"),
        "link": post.get("link"),
        "categories": post.get("categories", []),
        "tags": post.get("tags", []),
        "title": title,
        "excerpt": excerpt,
        "content": rendered,
        "word_count": len(rendered.split()),
        "status": post.get("status"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch WordPress posts via REST API.")
    parser.add_argument(
        "--base-url",
        default="https://www.johndcook.com/blog/wp-json/wp/v2/posts",
        help="Base REST endpoint for posts.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/johndcook_posts_api.jsonl"),
        help="Output JSONL file.",
    )
    parser.add_argument(
        "--verify-ssl",
        action="store_true",
        help="Verify SSL certificates (default: disabled).",
    )
    args = parser.parse_args()

    posts = []
    for post in iter_posts(args.base_url, args.verify_ssl):
        posts.append(normalize(post))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for post in posts:
            f.write(json.dumps(post, ensure_ascii=False) + "\n")

    total_words = sum(p["word_count"] for p in posts)
    print(f"Wrote {len(posts)} posts to {args.output}")
    print(f"Total words: {total_words}")


if __name__ == "__main__":
    main()
