#!/usr/bin/env python3
"""Generate a large candidate pool of calendar facts (~800+) without culling to 365."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set, Tuple

TEXT_INDEX = Path("data/johndcook_text_index.jsonl")
POSTS_ENRICHED = Path("data/johndcook_posts_enriched.jsonl")
OUT = Path("data/johndcook_calendar_candidates_v4.csv")

STOPWORDS = {
    "the",
    "and",
    "for",
    "that",
    "with",
    "this",
    "from",
    "have",
    "your",
    "about",
    "into",
    "when",
    "what",
    "where",
    "why",
    "which",
    "will",
    "would",
    "could",
    "should",
    "there",
    "their",
    "they",
    "them",
    "then",
    "than",
    "just",
    "also",
    "some",
    "most",
    "more",
    "very",
    "been",
    "because",
    "while",
    "using",
    "use",
    "used",
    "much",
    "many",
    "other",
    "only",
    "like",
    "over",
    "under",
    "between",
    "within",
    "without",
    "after",
    "before",
    "around",
    "across",
    "through",
    "every",
    "each",
    "than",
    "does",
    "done",
    "very",
    "may",
    "might",
    "must",
    "can",
    "cant",
    "cannot",
    "dont",
    "didnt",
    "was",
    "were",
    "are",
    "is",
    "am",
    "be",
    "being",
    "been",
}


@dataclass
class Post:
    id: int
    title: str
    link: str
    date: datetime
    word_count: int
    link_count: int
    image_count: int
    symbols: Dict[str, int]
    tokens: List[str]
    categories: List[str]
    tags: List[str]


def load_posts() -> List[Post]:
    by_id = {}
    with POSTS_ENRICHED.open() as f:
        for line in f:
            obj = json.loads(line)
            by_id[obj["id"]] = obj
    posts: List[Post] = []
    with TEXT_INDEX.open() as f:
        for line in f:
            idx = json.loads(line)
            base = by_id.get(idx["id"], {})
            date_str = base.get("date") or idx.get("date") or ""
            try:
                dt = datetime.fromisoformat(date_str.replace("Z", ""))
            except Exception:
                continue
            posts.append(
                Post(
                    id=idx["id"],
                    title=base.get("title") or idx.get("title") or "",
                    link=base.get("link") or idx.get("link") or "",
                    date=dt,
                    word_count=idx.get("word_count", 0),
                    link_count=idx.get("link_count", 0),
                    image_count=idx.get("image_count", 0),
                    symbols=idx.get("symbols", {}),
                    tokens=idx.get("tokens", []),
                    categories=base.get("category_names", []),
                    tags=base.get("tag_names", []),
                )
            )
    return posts


def rare_terms(posts: List[Post], max_terms: int = 400) -> List[Tuple[str, Post]]:
    tf = Counter()
    posting = defaultdict(list)
    for p in posts:
        seen = set()
        for t in p.tokens:
            if not t or t in STOPWORDS or len(t) < 4:
                continue
            seen.add(t)
        for t in seen:
            tf[t] += 1
            posting[t].append(p)
    rares = [(t, posting[t][0]) for t, c in tf.items() if c == 1]
    # sort by length then alphabetically
    rares.sort(key=lambda x: (-len(x[0]), x[0]))
    return rares[:max_terms]


def first_last_terms(posts: List[Post], targets: List[str]) -> List[Tuple[str, str, Post]]:
    # returns list of (label, mode[first/last], post)
    results = []
    by_term = defaultdict(list)
    for p in posts:
        toks = set(p.tokens)
        for t in targets:
            if t in toks:
                by_term[t].append(p)
    for t in targets:
        if by_term[t]:
            by_term[t].sort(key=lambda p: p.date)
            results.append((t, "first", by_term[t][0]))
            results.append((t, "last", by_term[t][-1]))
    return results


def top_outliers(posts: List[Post], key, n=10, reverse=True) -> List[Post]:
    return sorted(posts, key=key, reverse=reverse)[:n]


def on_this_day(posts: List[Post], limit: int = 150) -> List[Post]:
    by_doy = defaultdict(list)
    for p in posts:
        by_doy[p.date.timetuple().tm_yday].append(p)
    picks = []
    for doy, plist in by_doy.items():
        pick = max(plist, key=lambda p: p.word_count)
        picks.append(pick)
    picks.sort(key=lambda p: p.date.timetuple().tm_yday)
    return picks[:limit]


def fmt_date(dt: datetime) -> str:
    return dt.strftime("%b %d %Y")


def main() -> None:
    posts = load_posts()
    facts = []
    idx = 1
    seen_text: Set[str] = set()

    def add_fact(ftype: str, text: str, link: str):
        nonlocal idx
        if text in seen_text:
            return
        seen_text.add(text)
        facts.append({"id": idx, "type": ftype, "fact": text, "source_link": link})
        idx += 1

    # Rare terms
    for term, p in rare_terms(posts, max_terms=400):
        add_fact(
            "rarity",
            f"Only one post mentions “{term}”: “{p.title}” on {fmt_date(p.date)}.",
            p.link,
        )

    # First/last for notable terms
    targets = [
        "bayesian",
        "markov",
        "prime",
        "fibonacci",
        "golden",
        "riemann",
        "zeta",
        "elliptic",
        "fft",
        "pde",
        "monte",
        "carlo",
        "lambda",
        "category",
        "graph",
        "topology",
        "linear",
        "algebra",
        "cryptography",
        "crypto",
        "hipaa",
        "gdpr",
        "ccpa",
        "unicode",
        "regex",
        "music",
        "interview",
        "fortran",
        "haskell",
        "python",
        "mathematica",
        "julia",
        "rust",
        "cuda",
        "privacy",
        "entropy",
        "gaussian",
        "normal",
        "erf",
    ]
    for term, mode, p in first_last_terms(posts, targets):
        add_fact(
            "first-last",
            f"{mode.title()} “{term}” post: “{p.title}” on {fmt_date(p.date)}.",
            p.link,
        )

    # Outliers: longest/shortest, links/images
    for p in top_outliers(posts, key=lambda x: x.word_count, n=30, reverse=True):
        add_fact(
            "length",
            f"Long read: “{p.title}” runs {p.word_count} words ({fmt_date(p.date)}).",
            p.link,
        )
    for p in top_outliers(posts, key=lambda x: x.word_count, n=20, reverse=False):
        add_fact(
            "length",
            f"Shortest snippets: “{p.title}” at {p.word_count} words ({fmt_date(p.date)}).",
            p.link,
        )
    for p in top_outliers(posts, key=lambda x: x.link_count, n=30, reverse=True):
        add_fact(
            "links",
            f"Link-happy: “{p.title}” packs {p.link_count} links ({fmt_date(p.date)}).",
            p.link,
        )
    for p in top_outliers(posts, key=lambda x: x.image_count, n=20, reverse=True):
        add_fact(
            "images",
            f"Image-heavy: “{p.title}” includes {p.image_count} images ({fmt_date(p.date)}).",
            p.link,
        )

    # Symbols
    for sym_key, label in [("pi", "π"), ("phi", "φ"), ("Phi", "Φ"), ("infty", "∞")]:
        hits = [p for p in posts if p.symbols.get(sym_key, 0) > 0]
        for p in hits[:50]:
            add_fact(
                "symbol",
                f"Math symbol {label} appears in “{p.title}” ({fmt_date(p.date)}).",
                p.link,
            )

    # On this day (pick long/interesting)
    for p in on_this_day(posts, limit=200):
        add_fact(
            "on-this-day",
            f"On {p.date.strftime('%b %d')}: “{p.title}” ({p.word_count} words, {p.date.year}).",
            p.link,
        )

    # Code-ish keywords
    code_terms = ["python", "c++", "cuda", "rust", "haskell", "fortran", "regex", "unicode"]
    for term, mode, p in first_last_terms(posts, code_terms):
        add_fact(
            "code",
            f"{mode.title()} “{term}” mention: “{p.title}” on {fmt_date(p.date)}.",
            p.link,
        )

    # Privacy/crypto mix
    privacy_terms = ["hipaa", "gdpr", "ccpa", "privacy", "cryptography", "crypto"]
    for term, mode, p in first_last_terms(posts, privacy_terms):
        add_fact(
            "privacy",
            f"{mode.title()} “{term}” mention: “{p.title}” on {fmt_date(p.date)}.",
            p.link,
        )

    # Cap to ~900 to avoid overrun, but keep >800
    if len(facts) > 900:
        facts = facts[:900]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "type", "fact", "source_link"])
        writer.writeheader()
        writer.writerows(facts)
    print(f"Wrote {len(facts)} candidate facts to {OUT}")


if __name__ == "__main__":
    main()
