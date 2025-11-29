"""CLI entrypoint for shared cookbook tooling."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import typer

from . import paths
from . import bot_utils, calendar_utils, calendar_export, ingest_utils

app = typer.Typer(help="Cookbook utilities for calendar, bot, and book workflows.")
calendar_app = typer.Typer(help="Calendar validation and curation utilities.")
bot_app = typer.Typer(help="Bot fact utilities.")
ingest_app = typer.Typer(help="Ingestion and indexing helpers.")


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _load_hash_file(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8").strip()
    if " " in text:
        text = text.split()[0]
    return text


def _fail_if_errors(errors: list[str]) -> None:
    if errors:
        for err in errors:
            typer.secho(f"ERROR: {err}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


@calendar_app.command("validate", help="Validate the canonical 365 calendar file.")
def calendar_validate(
    calendar_path: Path = typer.Option(
        paths.data_path("johndcook_calendar_365.csv"),
        "--calendar-path",
        "-c",
        exists=True,
        readable=True,
        help="Path to the curated 365 calendar CSV.",
    ),
    hash_path: Path = typer.Option(
        paths.data_path("calendar", "final", "canonical.sha256"),
        "--hash-path",
        "-h",
        exists=False,
        help="Path to the stored checksum for the canonical calendar.",
    ),
) -> None:
    errors: list[str] = []

    try:
        rows = list(csv.DictReader(calendar_path.open(encoding="utf-8")))
    except Exception as exc:
        errors.append(f"Failed to read calendar: {exc}")
        _fail_if_errors(errors)
        return

    if len(rows) != 365:
        errors.append(f"Expected 365 facts, found {len(rows)}.")

    required_fields = {"id", "type", "fact", "source_link", "date", "slug"}
    missing_fields = required_fields.difference(set(rows[0].keys()) if rows else set())
    if missing_fields:
        errors.append(f"Missing expected columns: {', '.join(sorted(missing_fields))}")

    ids = [r.get("id") for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate IDs detected in calendar CSV.")

    facts = [r.get("fact", "").strip() for r in rows]
    if len(facts) != len(set(facts)):
        errors.append("Duplicate fact texts detected in calendar CSV.")

    expected_hash = _load_hash_file(hash_path)
    if expected_hash:
        actual_hash = _sha256(calendar_path)
        if actual_hash != expected_hash:
            errors.append(
                f"Checksum mismatch for {calendar_path} "
                f"(expected {expected_hash}, got {actual_hash})."
            )

    _fail_if_errors(errors)
    typer.secho(
        f"Calendar OK: {len(rows)} rows; checksum verified against {hash_path.name}.",
        fg=typer.colors.GREEN,
    )


@calendar_app.command("checksum", help="Print the SHA-256 of the calendar file.")
def calendar_checksum(
    calendar_path: Path = typer.Option(
        paths.data_path("johndcook_calendar_365.csv"),
        "--calendar-path",
        "-c",
        exists=True,
        readable=True,
        help="Path to the curated 365 calendar CSV.",
    )
) -> None:
    digest = _sha256(calendar_path)
    typer.echo(f"{digest}  {calendar_path}")


@calendar_app.command("snapshot", help="Copy the canonical 365 to a timestamped file.")
def calendar_snapshot(
    destination: Path = typer.Option(
        paths.data_path("calendar", "final"),
        "--dest",
        "-d",
        help="Directory for snapshots.",
    )
) -> None:
    dest = calendar_utils.snapshot_final(destination)
    typer.secho(f"Snapshot written to {dest}", fg=typer.colors.GREEN)


@calendar_app.command("candidates", help="Run a candidate generator (v3 or v4).")
def calendar_candidates(
    version: str = typer.Option(
        "v4",
        "--version",
        "-v",
        help="Which generator to run (v3 or v4).",
    )
) -> None:
    try:
        out = calendar_utils.run_candidate_generator(version)
    except ValueError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    typer.secho(f"Candidate facts written to {out}", fg=typer.colors.GREEN)


@calendar_app.command("export-images", help="Export calendar cards as PNG images.")
def calendar_export_images(
    output: Path = typer.Option(
        Path("out/calendar"),
        "--output",
        "-o",
        help="Output directory for card images.",
    ),
    facts_path: Path = typer.Option(
        paths.BOT_DIR / "facts.json",
        "--facts",
        "-f",
        exists=True,
        readable=True,
        help="Path to the 365 facts JSON (or CSV).",
    ),
    limit: int = typer.Option(
        None,
        "--limit",
        "-l",
        help="Limit number of cards to render (for testing).",
    ),
) -> None:
    typer.echo(f"Exporting calendar cards to {output}...")

    count = 0
    for card_path in calendar_export.export_cards(
        facts_path=facts_path,
        output_dir=output,
        limit=limit,
    ):
        count += 1
        if count % 50 == 0 or count <= 5:
            typer.echo(f"  Rendered {card_path.name}")

    typer.secho(f"Exported {count} cards to {output}", fg=typer.colors.GREEN)

    # Validate
    errors = calendar_export.validate_export(output, expected_count=limit or 365)
    if errors:
        for err in errors:
            typer.secho(f"WARNING: {err}", fg=typer.colors.YELLOW, err=True)


def _format_tweet_text(fact: dict) -> str:
    text = fact.get("text", "")
    link = fact.get("source_url")
    if link:
        candidate = f"{text}\n\n{link}"
        return candidate if len(candidate) <= 280 else text
    return text


@bot_app.command("validate", help="Validate bot facts for length and uniqueness.")
def bot_validate(
    facts_path: Path = typer.Option(
        paths.BOT_DIR / "facts.json",
        "--facts-path",
        "-f",
        exists=True,
        readable=True,
        help="Path to bot facts JSON.",
    ),
    max_length: int = typer.Option(
        260,
        "--max-length",
        "-m",
        help="Maximum fact text length (without link) to keep tweetable.",
    ),
) -> None:
    errors: list[str] = []
    facts = json.loads(facts_path.read_text(encoding="utf-8"))

    ids = [f.get("id") for f in facts]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate fact IDs detected in bot facts.")

    texts = []
    for fact in facts:
        text = fact.get("text", "")
        texts.append(text)
        if len(text) > max_length:
            errors.append(
                f"Fact id {fact.get('id')} exceeds max length ({len(text)} > {max_length})."
            )
        tweet = _format_tweet_text(fact)
        if len(tweet) > 280:
            errors.append(
                f"Fact id {fact.get('id')} would exceed tweet limit ({len(tweet)} chars)."
            )

    if len(texts) != len(set(texts)):
        errors.append("Duplicate fact texts detected in bot facts.")

    _fail_if_errors(errors)
    typer.secho(
        f"Bot facts OK: {len(facts)} facts validated against max length {max_length}.",
        fg=typer.colors.GREEN,
    )


@bot_app.command("build", help="Rebuild bot/facts.json from CSV sources.")
def bot_build(
    output_path: Path = typer.Option(
        paths.BOT_DIR / "facts.json",
        "--output",
        "-o",
        help="Where to write the aggregated facts JSON.",
    ),
    max_length: int = typer.Option(
        260,
        "--max-length",
        "-m",
        help="Maximum fact length to include (text only).",
    ),
) -> None:
    facts = bot_utils.build_facts(max_length=max_length)
    bot_utils.write_facts_json(facts, output_path)
    typer.secho(f"Wrote {len(facts)} facts to {output_path}", fg=typer.colors.GREEN)


@bot_app.command("status", help="Show how many facts remain to post.")
def bot_status(
    facts_path: Path = typer.Option(
        paths.BOT_DIR / "facts.json",
        "--facts",
        "-f",
        exists=True,
        readable=True,
        help="facts.json to draw from.",
    ),
    state_path: Path = typer.Option(
        paths.BOT_DIR / "state.json",
        "--state",
        "-s",
        help="State file tracking posted IDs.",
    ),
) -> None:
    facts = bot_utils.load_facts_json(facts_path)
    posted = bot_utils.load_state(state_path)
    remaining = len(facts) - len(posted)
    days_left = remaining // 2  # 2 posts per day
    typer.echo(f"Posted: {len(posted)}/{len(facts)}")
    typer.echo(f"Remaining: {remaining} (~{days_left} days at 2/day)")


@bot_app.command("post", help="Post a random fact to X.")
def bot_post(
    facts_path: Path = typer.Option(
        paths.BOT_DIR / "facts.json",
        "--facts",
        "-f",
        exists=True,
        readable=True,
        help="facts.json to draw from.",
    ),
    state_path: Path = typer.Option(
        paths.BOT_DIR / "state.json",
        "--state",
        "-s",
        help="State file tracking posted IDs.",
    ),
    reset_when_empty: bool = typer.Option(
        False,
        "--reset-when-empty",
        help="Allow reset to start over when all facts are posted.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Skip posting to X; print the tweet text.",
    ),
) -> None:
    meta = bot_utils.post_random_fact(
        facts_path=facts_path,
        state_path=state_path,
        reset_when_empty=reset_when_empty,
        dry_run=dry_run,
    )
    status = meta.get("status")
    if status == "dry-run":
        typer.echo(f"DRY RUN: {meta.get('tweet')}")
    elif status == "empty":
        typer.secho(meta.get("message", "No facts available."), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    elif status == "failed":
        typer.secho(f"Failed to post fact: {meta.get('error')}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    else:
        typer.secho(
            f"Posted fact #{meta.get('fact_id')} (tweet id {meta.get('tweet_id')})",
            fg=typer.colors.GREEN,
        )
        if meta.get("posted_count") is not None:
            typer.echo(f"Total posted: {meta.get('posted_count')}")


@ingest_app.command("wp-api", help="Fetch posts from the WordPress REST API.")
def ingest_wp_api(
    base_url: str = typer.Option(
        "https://www.johndcook.com/blog/wp-json/wp/v2/posts",
        "--base-url",
        help="Base posts endpoint.",
    ),
    output: Path = typer.Option(
        paths.data_path("johndcook_posts_api.jsonl"),
        "--output",
        "-o",
        help="Output path for posts JSONL.",
    ),
    verify_ssl: bool = typer.Option(
        False,
        "--verify-ssl",
        help="Verify SSL certificates.",
    ),
) -> None:
    out = ingest_utils.fetch_wp_api(base_url=base_url, output=output, verify_ssl=verify_ssl)
    typer.secho(f"Wrote posts to {out}", fg=typer.colors.GREEN)


@ingest_app.command("taxonomies", help="Fetch WP categories and tags.")
def ingest_taxonomies(
    base_url: str = typer.Option(
        "https://www.johndcook.com/blog/wp-json/wp/v2",
        "--base-url",
        help="Base WP REST URL (without trailing slash).",
    ),
    output_dir: Path = typer.Option(
        paths.data_path("wp_taxonomies"),
        "--output-dir",
        "-o",
        help="Directory for taxonomy JSON files.",
    ),
    verify_ssl: bool = typer.Option(
        False,
        "--verify-ssl",
        help="Verify SSL certificates.",
    ),
) -> None:
    out = ingest_utils.fetch_taxonomies(base_url=base_url, output_dir=output_dir, verify_ssl=verify_ssl)
    typer.secho(f"Wrote taxonomies to {out}", fg=typer.colors.GREEN)


@ingest_app.command("enrich", help="Enrich posts with taxonomy names.")
def ingest_enrich(
    posts: Path = typer.Option(
        paths.data_path("johndcook_posts_api.jsonl"),
        "--posts",
        "-p",
        help="Posts JSONL (from wp-api).",
    ),
    categories: Path = typer.Option(
        paths.data_path("wp_taxonomies", "categories.json"),
        "--categories",
        "-c",
        help="Categories JSON.",
    ),
    tags: Path = typer.Option(
        paths.data_path("wp_taxonomies", "tags.json"),
        "--tags",
        "-t",
        help="Tags JSON.",
    ),
    output: Path = typer.Option(
        paths.data_path("johndcook_posts_enriched.jsonl"),
        "--output",
        "-o",
        help="Output enriched posts JSONL.",
    ),
) -> None:
    out = ingest_utils.enrich_posts(posts_path=posts, categories_path=categories, tags_path=tags, output_path=output)
    typer.secho(f"Wrote enriched posts to {out}", fg=typer.colors.GREEN)


@ingest_app.command("index", help="Build the text index JSONL.")
def ingest_index(
    output: Path = typer.Option(
        paths.data_path("johndcook_text_index.jsonl"),
        "--output",
        "-o",
        help="Output text index path.",
    )
) -> None:
    out = ingest_utils.build_text_index(output_path=output)
    typer.secho(f"Wrote text index to {out}", fg=typer.colors.GREEN)


app.add_typer(calendar_app, name="calendar")
app.add_typer(bot_app, name="bot")
app.add_typer(ingest_app, name="ingest")


def main() -> None:
    # Typer handles argv parsing; default invocation uses sys.argv.
    app()


if __name__ == "__main__":
    main()
