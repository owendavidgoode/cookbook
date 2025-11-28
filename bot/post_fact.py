#!/usr/bin/env python3
"""Post a random fact to X (Twitter)."""

from __future__ import annotations

import argparse
from pathlib import Path

from cookbook import bot_utils


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Post a random fact to X.")
    parser.add_argument(
        "--facts",
        default=str(Path(__file__).parent / "facts.json"),
        help="Path to facts.json",
    )
    parser.add_argument(
        "--state",
        default=str(Path(__file__).parent / "state.json"),
        help="Path to state.json",
    )
    parser.add_argument(
        "--reset-when-empty",
        action="store_true",
        help="Allow reset when all facts have been posted.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not post; print the tweet instead.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    facts_path = Path(args.facts)
    state_path = Path(args.state)

    if not facts_path.exists():
        print(f"Error: {facts_path} not found")
        return 1

    meta = bot_utils.post_random_fact(
        facts_path=facts_path,
        state_path=state_path,
        reset_when_empty=args.reset_when_empty,
        dry_run=args.dry_run,
    )

    status = meta.get("status")
    if status == "dry-run":
        print(f"DRY RUN: {meta.get('tweet')}")
        return 0
    if status == "empty":
        print(meta.get("message", "All facts posted; no reset allowed."))
        return 1
    if status == "failed":
        print(f"Failed to post fact: {meta.get('error')}")
        return 1

    print(f"Posted fact #{meta.get('fact_id')} (tweet id {meta.get('tweet_id')})")
    if meta.get("posted_count") is not None:
        print(f"State updated: {meta.get('posted_count')} facts posted")
    if meta.get("warning"):
        print(f"Warning: {meta.get('warning')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
