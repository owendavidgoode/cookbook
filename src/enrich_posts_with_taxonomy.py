#!/usr/bin/env python3
"""Join post JSONL with taxonomy names and emit enriched JSONL."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.open()]


def load_taxonomy(path: Path) -> dict[int, str]:
    items = json.loads(path.read_text(encoding="utf-8"))
    return {int(item["id"]): item.get("name", "") for item in items}


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich posts with category/tag names.")
    parser.add_argument(
        "--posts",
        type=Path,
        default=Path("data/johndcook_posts_api.jsonl"),
        help="Posts JSONL from fetch_wp_api.py",
    )
    parser.add_argument(
        "--categories",
        type=Path,
        default=Path("data/wp_taxonomies/categories.json"),
        help="Categories JSON from fetch_wp_taxonomies.py",
    )
    parser.add_argument(
        "--tags",
        type=Path,
        default=Path("data/wp_taxonomies/tags.json"),
        help="Tags JSON from fetch_wp_taxonomies.py",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/johndcook_posts_enriched.jsonl"),
        help="Output JSONL with names",
    )
    args = parser.parse_args()

    posts = load_jsonl(args.posts)
    cat_map = load_taxonomy(args.categories)
    tag_map = load_taxonomy(args.tags)

    cat_counts = Counter()
    tag_counts = Counter()

    enriched = []
    for post in posts:
        cats = [cat_map.get(int(cid), str(cid)) for cid in post.get("categories", [])]
        tags = [tag_map.get(int(tid), str(tid)) for tid in post.get("tags", [])]
        cat_counts.update(cats)
        tag_counts.update(tags)
        post["category_names"] = cats
        post["tag_names"] = tags
        enriched.append(post)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for post in enriched:
            f.write(json.dumps(post, ensure_ascii=False) + "\n")

    print(f"Wrote {len(enriched)} posts to {args.output}")
    print("Top 10 categories:")
    for name, count in cat_counts.most_common(10):
        print(f"  {name}: {count}")
    print("Top 10 tags:")
    for name, count in tag_counts.most_common(10):
        print(f"  {name}: {count}")


if __name__ == "__main__":
    main()
