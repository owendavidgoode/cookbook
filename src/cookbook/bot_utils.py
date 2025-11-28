"""Shared helpers for bot fact building and posting."""

from __future__ import annotations

import json
import os
import random
import time
from pathlib import Path
from typing import Iterable

import tweepy

from . import paths


DEFAULT_FACT_FILES = [
    "johndcook_calendar_365.csv",
    "hn_facts.csv",
    "new_analysis_facts.csv",
    "additional_phd_facts.csv",
]


def load_csv_facts(csv_path: Path) -> list[dict]:
    """Load facts from a CSV file; expects header with 'fact' and optional columns."""
    import csv  # Lazy import to keep top-level light

    facts: list[dict] = []
    with csv_path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            fact_text = row.get("fact", "").strip()
            if not fact_text:
                continue
            source_url = (row.get("source_link") or "").strip() or None
            fact_type = (row.get("type") or "general").strip()
            slug = (row.get("slug") or "").strip() or None
            facts.append(
                {
                    "text": fact_text,
                    "source_url": source_url,
                    "type": fact_type,
                    "slug": slug,
                    "source_file": csv_path.name,
                }
            )
    return facts


def build_facts(data_dir: Path | None = None, max_length: int = 260) -> list[dict]:
    """Aggregate facts from the default CSV sources, assigning IDs and enforcing length."""
    base = data_dir or paths.DATA_ROOT
    all_facts: list[dict] = []
    for filename in DEFAULT_FACT_FILES:
        path = base / filename
        if not path.exists():
            continue
        facts = load_csv_facts(path)
        all_facts.extend(facts)

    # Assign IDs
    for idx, fact in enumerate(all_facts, start=1):
        fact["id"] = idx

    # Filter for tweetable length (room for link)
    valid = [f for f in all_facts if len(f.get("text", "")) <= max_length]
    return valid


def write_facts_json(facts: Iterable[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(list(facts), fh, indent=2, ensure_ascii=False)


def load_facts_json(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_state(path: Path) -> set[int]:
    if not path.exists():
        return set()
    with path.open(encoding="utf-8") as fh:
        return set(json.load(fh).get("posted_ids", []))


def save_state(path: Path, posted_ids: set[int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump({"posted_ids": sorted(posted_ids)}, fh, indent=2)


def pick_fact(facts: list[dict], posted_ids: set[int]) -> dict | None:
    unposted = [f for f in facts if f.get("id") not in posted_ids]
    if not unposted:
        return None
    return random.choice(unposted)


def format_tweet(fact: dict) -> str:
    text = fact.get("text", "")
    link = fact.get("source_url")
    if link:
        candidate = f"{text}\n\n{link}"
        if len(candidate) <= 280:
            return candidate
    return text


def get_client() -> tweepy.Client:
    return tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )


def post_random_fact(
    facts_path: Path,
    state_path: Path,
    reset_when_empty: bool = False,
    dry_run: bool = False,
    retries: int = 2,
    backoff_seconds: float = 2.0,
) -> dict:
    """Pick and post a fact; returns metadata about the attempt."""
    facts = load_facts_json(facts_path)
    posted_ids = load_state(state_path)

    picked = pick_fact(facts, posted_ids)
    if picked is None:
        if not reset_when_empty:
            return {"status": "empty", "message": "All facts posted; reset prohibited."}
        posted_ids = set()
        picked = pick_fact(facts, posted_ids)
        if picked is None:
            return {"status": "empty", "message": "No facts available after reset."}

    tweet_text = format_tweet(picked)
    meta: dict[str, object] = {"status": "posted", "fact_id": picked.get("id"), "tweet": tweet_text}

    if dry_run:
        meta["status"] = "dry-run"
        return meta

    client = get_client()
    last_exc: Exception | None = None
    for attempt in range(1, retries + 2):
        try:
            response = client.create_tweet(text=tweet_text)
            meta["tweet_id"] = response.data.get("id")
            break
        except Exception as exc:  # tweepy raises generic errors
            last_exc = exc
            if attempt > retries:
                meta["status"] = "failed"
                meta["error"] = str(exc)
                return meta
            time.sleep(backoff_seconds * attempt)

    posted_ids.add(picked["id"])
    save_state(state_path, posted_ids)
    meta["posted_count"] = len(posted_ids)
    if last_exc:
        meta["warning"] = f"succeeded after retry: {last_exc}"
    return meta
