#!/usr/bin/env python3
"""Generate a 365-fact CSV for a daily calendar from johndcook.com posts."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean, median
from typing import Dict, List, Set, Tuple

INPUT_PATH = Path("data/johndcook_posts_enriched.jsonl")
OUTPUT_PATH = Path("data/johndcook_calendar_facts.csv")


@dataclass
class Post:
    id: int
    title: str
    link: str
    date: datetime
    word_count: int
    categories: List[str]
    tags: List[str]
    slug: str


def load_posts(path: Path) -> List[Post]:
    posts: List[Post] = []
    with path.open() as f:
        for line in f:
            obj = json.loads(line)
            date_str = obj.get("date") or ""
            try:
                dt = datetime.fromisoformat(date_str.replace("Z", ""))
            except Exception:
                continue
            posts.append(
                Post(
                    id=obj.get("id"),
                    title=(obj.get("title") or "").strip(),
                    link=obj.get("link") or "",
                    date=dt,
                    word_count=int(obj.get("word_count", 0)),
                    categories=obj.get("category_names", []) or [],
                    tags=obj.get("tag_names", []) or [],
                    slug=obj.get("slug") or "",
                )
            )
    return posts


def format_date(dt: datetime) -> str:
    return dt.strftime("%b %d, %Y")


def ensure_unique(facts: List[dict], seen: Set[str], fact: dict) -> None:
    text = fact["fact"]
    if text in seen:
        return
    seen.add(text)
    facts.append(fact)


def add_year_facts(posts: List[Post], facts: List[dict], seen: Set[str]) -> None:
    by_year = defaultdict(list)
    for p in posts:
        by_year[p.date.year].append(p)
    for year, items in sorted(by_year.items()):
        wc = sum(p.word_count for p in items)
        avg_wc = wc / len(items)
        fact = {
            "type": "year",
            "fact": f"{year}: {len(items)} posts (~{wc:,} words, avg {int(avg_wc)} words each).",
            "source_link": "",
        }
        ensure_unique(facts, seen, fact)
    # Highlight extremes
    most_year = max(by_year.items(), key=lambda kv: len(kv[1]))
    least_year = min(by_year.items(), key=lambda kv: len(kv[1]))
    ensure_unique(
        facts,
        seen,
        {
            "type": "year",
            "fact": f"Busiest year: {most_year[0]} with {len(most_year[1])} posts.",
            "source_link": "",
        },
    )
    ensure_unique(
        facts,
        seen,
        {
            "type": "year",
            "fact": f"Quietest year: {least_year[0]} with {len(least_year[1])} posts.",
            "source_link": "",
        },
    )


def add_length_facts(posts: List[Post], facts: List[dict], seen: Set[str]) -> None:
    sorted_posts = sorted(posts, key=lambda p: p.word_count)
    shortest = sorted_posts[:10]
    longest = sorted_posts[-10:][::-1]
    for p in shortest:
        ensure_unique(
            facts,
            seen,
            {
                "type": "length",
                "fact": f"Short & sharp: “{p.title}” in {format_date(p.date)} packs {p.word_count} words.",
                "source_link": p.link,
            },
        )
    for p in longest:
        ensure_unique(
            facts,
            seen,
            {
                "type": "length",
                "fact": f"Deep dive: “{p.title}” ({format_date(p.date)}) runs {p.word_count} words.",
                "source_link": p.link,
            },
        )
    wc = [p.word_count for p in posts]
    ensure_unique(
        facts,
        seen,
        {
            "type": "length",
            "fact": f"Typical post: median {int(median(wc))} words vs average {int(mean(wc))}.",
            "source_link": "",
        },
    )
    ensure_unique(
        facts,
        seen,
        {
            "type": "length",
            "fact": f"Total payload: {sum(wc):,} words across {len(posts)} posts.",
            "source_link": "",
        },
    )


def add_category_facts(posts: List[Post], facts: List[dict], seen: Set[str]) -> None:
    cat_counts = Counter()
    cat_words = defaultdict(int)
    for p in posts:
        for c in p.categories:
            cat_counts[c] += 1
            cat_words[c] += p.word_count
    for cat, count in cat_counts.most_common(12):
        avg = int(cat_words[cat] / count)
        ensure_unique(
            facts,
            seen,
            {
                "type": "category",
                "fact": f"Category “{cat}” shows up {count} times, averaging {avg} words per post.",
                "source_link": "",
            },
        )


def add_tag_facts(posts: List[Post], facts: List[dict], seen: Set[str]) -> None:
    tag_counts = Counter()
    tag_words = defaultdict(int)
    for p in posts:
        for t in p.tags:
            tag_counts[t] += 1
            tag_words[t] += p.word_count
    for tag, count in tag_counts.most_common(20):
        avg = int(tag_words[tag] / count)
        ensure_unique(
            facts,
            seen,
            {
                "type": "tag",
                "fact": f"Tag “{tag}”: {count} posts, avg {avg} words.",
                "source_link": "",
            },
        )


def add_weekday_facts(posts: List[Post], facts: List[dict], seen: Set[str]) -> None:
    by_day = Counter(p.date.strftime("%A") for p in posts)
    most = by_day.most_common(1)[0]
    least = by_day.most_common()[-1]
    ensure_unique(
        facts,
        seen,
        {
            "type": "weekday",
            "fact": f"Busiest weekday: {most[0]} with {most[1]} posts; quietest: {least[0]} with {least[1]}.",
            "source_link": "",
        },
    )
    for day, count in by_day.items():
        ensure_unique(
            facts,
            seen,
            {"type": "weekday", "fact": f"{day}s host {count} posts on the blog.", "source_link": ""},
        )


def add_month_facts(posts: List[Post], facts: List[dict], seen: Set[str]) -> None:
    by_month = Counter((p.date.year, p.date.month) for p in posts)
    top = by_month.most_common(5)
    for (y, m), c in top:
        month_name = datetime(y, m, 1).strftime("%B %Y")
        ensure_unique(
            facts,
            seen,
            {
                "type": "month",
                "fact": f"{month_name} was busy with {c} posts.",
                "source_link": "",
            },
        )


def add_gap_facts(posts: List[Post], facts: List[dict], seen: Set[str]) -> None:
    posts_sorted = sorted(posts, key=lambda p: p.date)
    max_gap = 0
    max_gap_pair: Tuple[Post, Post] | None = None
    for prev, cur in zip(posts_sorted, posts_sorted[1:]):
        gap = (cur.date - prev.date).days
        if gap > max_gap:
            max_gap = gap
            max_gap_pair = (prev, cur)
    if max_gap_pair:
        prev, cur = max_gap_pair
        ensure_unique(
            facts,
            seen,
            {
                "type": "gap",
                "fact": f"Longest pause: {max_gap} days between “{prev.title}” ({format_date(prev.date)}) and “{cur.title}” ({format_date(cur.date)}).",
                "source_link": prev.link,
            },
        )


def add_on_this_day(posts: List[Post], facts: List[dict], seen: Set[str], limit: int = 60) -> None:
    by_doy: Dict[int, List[Post]] = defaultdict(list)
    for p in posts:
        doy = p.date.timetuple().tm_yday
        by_doy[doy].append(p)
    count = 0
    for doy, plist in sorted(by_doy.items()):
        if count >= limit:
            break
        pick = max(plist, key=lambda p: p.word_count)
        ensure_unique(
            facts,
            seen,
            {
                "type": "on-this-day",
                "fact": f"On {pick.date.strftime('%b %d')}: “{pick.title}” ({pick.word_count} words, {pick.date.year}).",
                "source_link": pick.link,
            },
        )
        count += 1


def add_symbol_facts(posts: List[Post], facts: List[dict], seen: Set[str]) -> None:
    symbols = {
        "π": 0,
        "φ": 0,
        "Φ": 0,
        "∞": 0,
    }
    for p in posts:
        content = p.title + " " + (p.slug or "")
        for sym in symbols:
            if sym in content:
                symbols[sym] += 1
    for sym, cnt in symbols.items():
        ensure_unique(
            facts,
            seen,
            {
                "type": "symbol",
                "fact": f"Posts with “{sym}”: {cnt}.",
                "source_link": "",
            },
        )


def add_first_last(posts: List[Post], facts: List[dict], seen: Set[str]) -> None:
    first = min(posts, key=lambda p: p.date)
    last = max(posts, key=lambda p: p.date)
    ensure_unique(
        facts,
        seen,
        {
            "type": "milestone",
            "fact": f"First post: “{first.title}” on {format_date(first.date)}.",
            "source_link": first.link,
        },
    )
    ensure_unique(
        facts,
        seen,
        {
            "type": "milestone",
            "fact": f"Latest post: “{last.title}” on {format_date(last.date)}.",
            "source_link": last.link,
        },
    )


def main() -> None:
    posts = load_posts(INPUT_PATH)
    facts: List[dict] = []
    seen: Set[str] = set()

    add_year_facts(posts, facts, seen)
    add_length_facts(posts, facts, seen)
    add_category_facts(posts, facts, seen)
    add_tag_facts(posts, facts, seen)
    add_weekday_facts(posts, facts, seen)
    add_month_facts(posts, facts, seen)
    add_gap_facts(posts, facts, seen)
    add_on_this_day(posts, facts, seen, limit=80)
    add_symbol_facts(posts, facts, seen)
    add_first_last(posts, facts, seen)

    # If we don't reach 365, recycle high-word posts as features.
    if len(facts) < 365:
        extras = sorted(posts, key=lambda p: p.word_count, reverse=True)
        for p in extras:
            if len(facts) >= 365:
                break
            fact = {
                "type": "feature",
                "fact": f"Heavyweight: “{p.title}” ({p.word_count} words, {format_date(p.date)}).",
                "source_link": p.link,
            }
            ensure_unique(facts, seen, fact)

    # Trim or pad to exactly 365 by truncating if necessary
    facts = facts[:365]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["day", "type", "fact", "source_link"])
        writer.writeheader()
        for idx, fact in enumerate(facts, start=1):
            writer.writerow({"day": idx, **fact})
    print(f"Wrote {len(facts)} facts to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
