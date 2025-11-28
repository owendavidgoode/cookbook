"""Ingestion and indexing helpers wrapping existing scripts."""

from __future__ import annotations

from pathlib import Path
import json

from . import paths


def fetch_wp_api(
    base_url: str = "https://www.johndcook.com/blog/wp-json/wp/v2/posts",
    output: Path | None = None,
    verify_ssl: bool = False,
) -> Path:
    from src import fetch_wp_api as script

    output_path = output or paths.data_path("johndcook_posts_api.jsonl")
    script.main = getattr(script, "main")  # type: ignore
    # Reuse script functions directly
    posts = []
    for post in script.iter_posts(base_url, verify_ssl):
        posts.append(script.normalize(post))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        import json

        for post in posts:
            fh.write(json.dumps(post, ensure_ascii=False) + "\n")
    return output_path


def fetch_taxonomies(
    base_url: str = "https://www.johndcook.com/blog/wp-json/wp/v2",
    output_dir: Path | None = None,
    verify_ssl: bool = False,
) -> Path:
    from src import fetch_wp_taxonomies as script

    out_dir = output_dir or paths.data_path("wp_taxonomies")
    out_dir.mkdir(parents=True, exist_ok=True)
    for kind in ("categories", "tags"):
        url = f"{base_url}/{kind}"
        items = script.fetch_all(url, verify_ssl=verify_ssl)
        (out_dir / f"{kind}.json").write_text(
            json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return out_dir


def enrich_posts(
    posts_path: Path | None = None,
    categories_path: Path | None = None,
    tags_path: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    from src import enrich_posts_with_taxonomy as script

    posts = posts_path or paths.data_path("johndcook_posts_api.jsonl")
    categories = categories_path or paths.data_path("wp_taxonomies", "categories.json")
    tags = tags_path or paths.data_path("wp_taxonomies", "tags.json")
    output = output_path or paths.data_path("johndcook_posts_enriched.jsonl")

    script.main = getattr(script, "main")  # type: ignore
    # Reuse script logic
    posts_data = script.load_jsonl(posts)
    cat_map = script.load_taxonomy(categories)
    tag_map = script.load_taxonomy(tags)
    enriched = []
    for post in posts_data:
        post["category_names"] = [cat_map.get(int(cid), str(cid)) for cid in post.get("categories", [])]
        post["tag_names"] = [tag_map.get(int(tid), str(tid)) for tid in post.get("tags", [])]
        enriched.append(post)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as fh:
        import json

        for post in enriched:
            fh.write(json.dumps(post, ensure_ascii=False) + "\n")
    return output


def build_text_index(output_path: Path | None = None) -> Path:
    from src import build_post_text_index as script

    out_path = output_path or paths.data_path("johndcook_text_index.jsonl")
    script.SRC = paths.data_path("johndcook_posts_enriched.jsonl")
    script.OUT = out_path
    script.main()
    return out_path
