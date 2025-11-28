#!/usr/bin/env python3
"""Post a random fact to X (Twitter)."""

import json
import os
import random
import sys
from pathlib import Path

import tweepy


def load_facts(facts_path: Path) -> list[dict]:
    """Load facts from JSON file."""
    with facts_path.open() as f:
        return json.load(f)


def load_state(state_path: Path) -> set[int]:
    """Load set of already-posted fact IDs."""
    if not state_path.exists():
        return set()
    with state_path.open() as f:
        data = json.load(f)
        return set(data.get("posted_ids", []))


def save_state(state_path: Path, posted_ids: set[int]) -> None:
    """Save posted fact IDs to state file."""
    with state_path.open("w") as f:
        json.dump({"posted_ids": sorted(posted_ids)}, f, indent=2)


def get_client() -> tweepy.Client:
    """Create authenticated X API client."""
    return tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )


def pick_fact(facts: list[dict], posted_ids: set[int]) -> dict | None:
    """Pick a random unposted fact. Returns None if all facts have been posted."""
    unposted = [f for f in facts if f["id"] not in posted_ids]
    if not unposted:
        return None
    return random.choice(unposted)


def format_tweet(fact: dict) -> str:
    """Format fact as tweet text."""
    text = fact["text"]
    # Add source link if present and fits
    if "source_url" in fact:
        link = f"\n\n{fact['source_url']}"
        if len(text) + len(link) <= 280:
            text += link
    return text


def main() -> int:
    bot_dir = Path(__file__).parent
    facts_path = bot_dir / "facts.json"
    state_path = bot_dir / "state.json"

    if not facts_path.exists():
        print(f"Error: {facts_path} not found")
        return 1

    facts = load_facts(facts_path)
    posted_ids = load_state(state_path)

    print(f"Loaded {len(facts)} facts, {len(posted_ids)} already posted")

    fact = pick_fact(facts, posted_ids)
    if fact is None:
        print("All facts have been posted! Resetting...")
        posted_ids = set()
        fact = pick_fact(facts, posted_ids)

    tweet_text = format_tweet(fact)
    print(f"Posting fact #{fact['id']}: {tweet_text[:80]}...")

    # Post to X
    client = get_client()
    response = client.create_tweet(text=tweet_text)
    print(f"Posted! Tweet ID: {response.data['id']}")

    # Update state
    posted_ids.add(fact["id"])
    save_state(state_path, posted_ids)
    print(f"State updated: {len(posted_ids)} facts posted")

    return 0


if __name__ == "__main__":
    sys.exit(main())
