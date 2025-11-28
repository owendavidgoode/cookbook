#!/usr/bin/env python3
"""Fetch WordPress categories and tags via REST API."""

from __future__ import annotations

import argparse
import json
import ssl
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def fetch_all(base_url: str, verify_ssl: bool = False) -> list[dict]:
    ctx = ssl.create_default_context()
    if not verify_ssl:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    per_page = 100
    page = 1
    items: list[dict] = []
    while True:
        params = {"per_page": per_page, "page": page}
        url = f"{base_url}?{urlencode(params)}"
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, context=ctx) as resp:
            data = json.load(resp)
        if not data:
            break
        items.extend(data)
        if len(data) < per_page:
            break
        page += 1
    return items


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch WP categories and tags.")
    parser.add_argument(
        "--base",
        default="https://www.johndcook.com/blog/wp-json/wp/v2",
        help="Base WP REST URL (without trailing slash).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/wp_taxonomies"),
        help="Output directory for JSON files.",
    )
    parser.add_argument(
        "--verify-ssl",
        action="store_true",
        help="Verify SSL certificates (default: disabled).",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    for kind in ("categories", "tags"):
        url = f"{args.base}/{kind}"
        items = fetch_all(url, verify_ssl=args.verify_ssl)
        out_path = args.output_dir / f"{kind}.json"
        out_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {len(items)} {kind} to {out_path}")


if __name__ == "__main__":
    main()
