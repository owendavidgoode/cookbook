"""Shared helpers for bot posting."""

from __future__ import annotations

import json
import os
import random
import time
from pathlib import Path
from typing import Iterable

import tweepy


def write_facts_json(facts: Iterable[dict], output_path: Path) -> None:
    """Write facts list to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(list(facts), fh, indent=2, ensure_ascii=False)


def load_facts_json(path: Path) -> list[dict]:
    """Load facts from JSON, ensuring each fact has an ID."""
    with path.open(encoding="utf-8") as fh:
        facts = json.load(fh)
    # Ensure all facts have IDs (assign if missing)
    for idx, fact in enumerate(facts, start=1):
        if not fact.get("id"):
            fact["id"] = idx
    return facts


RECENCY_WINDOW = 50  # Don't repeat a fact within this many days


def load_state(path: Path) -> list[int]:
    """Load ordered list of recently-posted fact IDs (most recent last)."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
        # Support both old format (posted_ids set) and new format (recent_ids list)
        if "recent_ids" in data:
            return data["recent_ids"]
        # Migrate from old format - treat all as recent
        return data.get("posted_ids", [])


def save_state(path: Path, recent_ids: list[int]) -> None:
    """Save recently-posted fact IDs to state file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump({"recent_ids": recent_ids}, fh, indent=2)


def pick_fact(facts: list[dict], recent_ids: list[int]) -> dict | None:
    """Pick a random fact not posted in the last RECENCY_WINDOW days."""
    excluded = set(recent_ids[-RECENCY_WINDOW:])
    eligible = [f for f in facts if f.get("id") not in excluded]
    if not eligible:
        return None
    return random.choice(eligible)


def format_tweet(fact: dict) -> str:
    """Format fact as tweet text, optionally appending source link."""
    text = fact.get("text", "")
    link = fact.get("source_url") or fact.get("source_link")
    if link:
        candidate = f"{text}\n\n{link}"
        if len(candidate) <= 280:
            return candidate
    return text


def get_client() -> tweepy.Client:
    """Create authenticated Twitter/X client from environment variables."""
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
    recent_ids = load_state(state_path)

    picked = pick_fact(facts, recent_ids)
    if picked is None:
        # With sliding window, this shouldn't happen unless pool < RECENCY_WINDOW
        return {"status": "empty", "message": "No eligible facts available."}

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

    # Append to recent list (sliding window maintained by pick_fact)
    recent_ids.append(picked["id"])
    save_state(state_path, recent_ids)
    meta["recent_count"] = len(recent_ids)
    meta["window_size"] = RECENCY_WINDOW
    if last_exc:
        meta["warning"] = f"succeeded after retry: {last_exc}"
    return meta
