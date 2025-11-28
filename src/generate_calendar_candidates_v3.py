#!/usr/bin/env python3
"""Generate a large, more creative pool of calendar facts (~2000+).

This script:
- Uses full text index and enriched post metadata
- Emphasizes quirky / comparative facts, not just one-off rare words
- Does NOT trim to 365; output is a big candidate pool
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

TEXT_INDEX = Path("data/johndcook_text_index.jsonl")
POSTS_ENRICHED = Path("data/johndcook_posts_enriched.jsonl")
POSTS_META = Path("data/posts_metadata.csv")
OUT = Path("data/johndcook_calendar_candidates_v3.csv")


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


def load_metadata():
    by_doy = Counter()
    by_monthday = Counter()
    by_weekday = Counter()
    by_year = Counter()
    with POSTS_META.open() as f:
        r = csv.DictReader(f)
        for row in r:
            if not row["date"]:
                continue
            dt = datetime.fromisoformat(row["date"].replace("Z", ""))
            doy = dt.timetuple().tm_yday
            by_doy[doy] += 1
            by_monthday[(dt.month, dt.day)] += 1
            by_weekday[dt.strftime("%A")] += 1
            by_year[dt.year] += 1
    return by_doy, by_monthday, by_weekday, by_year


def build_term_doc_counts(posts: List[Post]) -> Counter:
    df = Counter()
    for p in posts:
        for t in set(p.tokens):
            df[t] += 1
    return df


def format_date(dt: datetime) -> str:
    return dt.strftime("%b %d %Y")


def month_day_str(month: int, day: int) -> str:
    return datetime(2000, month, day).strftime("%b %d")


def main() -> None:
    posts = load_posts()
    by_doy, by_monthday, by_weekday, by_year = load_metadata()
    df = build_term_doc_counts(posts)

    total_posts = len(posts)

    facts: List[dict] = []
    seen_text: Set[str] = set()
    next_id = 1

    def add(ftype: str, text: str, link: str = ""):
        nonlocal next_id
        if not text or text in seen_text:
            return
        seen_text.add(text)
        facts.append({"id": next_id, "type": ftype, "fact": text, "source_link": link})
        next_id += 1

    # 1) Date-density "on-this-day" style facts
    top_days = by_monthday.most_common(10)
    if top_days:
        (m0, d0), c0 = top_days[0]
        add(
            "date-density",
            f"The blog’s favorite calendar date is {month_day_str(m0, d0)}: {c0} different posts share that same day across the years.",
        )
        for (m, d), c in top_days[1:5]:
            add(
                "date-density",
                f"{month_day_str(m, d)} is one of the blog’s busiest dates, with {c} posts landing on that day.",
            )

    # Weekday and year patterns
    if by_weekday:
        busiest = max(by_weekday.items(), key=lambda kv: kv[1])
        quietest = min(by_weekday.items(), key=lambda kv: kv[1])
        add(
            "weekday",
            f"Tuesdays rule this blog: {by_weekday['Tuesday']} posts—more than any other weekday. Sundays are the quietest with only {by_weekday['Sunday']} posts.",
        )
        add(
            "weekday",
            f"Across {total_posts} posts, {busiest[1]} land on {busiest[0]}s while only {quietest[1]} appear on {quietest[0]}s.",
        )

    if by_year:
        busiest_year, busiest_count = max(by_year.items(), key=lambda kv: kv[1])
        earliest_year, earliest_count = min(by_year.items(), key=lambda kv: kv[0])
        add(
            "year",
            f"Back in {earliest_year}, the blog already pushed out {earliest_count} posts. By {busiest_year} it hit a peak of {busiest_count} posts in a single year.",
        )

    # 2) Symbol and constant facts
    pi_posts = sum(1 for p in posts if p.symbols.get("pi", 0))
    phi_posts = sum(1 for p in posts if p.symbols.get("phi", 0) or p.symbols.get("Phi", 0))
    infty_posts = sum(1 for p in posts if p.symbols.get("infty", 0))
    any_sym_posts = sum(
        1 for p in posts if p.symbols.get("pi", 0) or p.symbols.get("phi", 0) or p.symbols.get("Phi", 0) or p.symbols.get("infty", 0)
    )
    add(
        "symbols",
        f"At least one of π, φ, or ∞ appears in {any_sym_posts} posts—more than {any_sym_posts * 100 // total_posts}% of the blog.",
    )
    add(
        "symbols",
        f"π appears in {pi_posts} posts, φ in {phi_posts}, and ∞ in {infty_posts}. That’s a lot of Unicode for one math blog.",
    )

    # 3) Term-level comparative facts
    term_set = {
        "prime",
        "fibonacci",
        "unicode",
        "cryptography",
        "bayesian",
        "markov",
        "category",
        "graph",
        "topology",
        "music",
    }
    term_docs = {t: df.get(t, 0) for t in term_set}

    prime_docs = term_docs["prime"]
    fib_docs = term_docs["fibonacci"]
    if prime_docs and fib_docs:
        add(
            "term-comparison",
            f"Primes beat Fibonacci: {prime_docs} posts mention “prime” while only {fib_docs} mention “Fibonacci”.",
        )

    uni_docs = term_docs["unicode"]
    if uni_docs:
        ratio = total_posts / uni_docs
        add(
            "term-comparison",
            f"“Unicode” shows up in {uni_docs} posts, roughly one in every {int(round(ratio))}. This blog really likes its character sets.",
        )

    bayes_docs = term_docs["bayesian"]
    markov_docs = term_docs["markov"]
    if bayes_docs and markov_docs:
        add(
            "term-comparison",
            f"There are {bayes_docs} posts that say “Bayesian” and {markov_docs} that say “Markov” — enough to keep a stochastic Bayesian busy for a while.",
        )

    music_docs = term_docs["music"]
    if music_docs:
        add(
            "term-comparison",
            f"Even though it’s a math blog, {music_docs} posts explicitly talk about music.",
        )

    # 4) Category / tag flavor
    cat_counts = Counter()
    for p in posts:
        for c in p.categories:
            cat_counts[c] += 1
    if cat_counts:
        math_count = cat_counts.get("Math", 0)
        stats_count = cat_counts.get("Statistics", 0)
        python_count = cat_counts.get("Python", 0)
        creativity_count = cat_counts.get("Creativity", 0)
        add(
            "category",
            f"Nearly half the blog ({math_count} posts) lives in the “Math” category, but there are {stats_count} “Statistics” posts and {python_count} “Python” posts sneaking in too.",
        )
        add(
            "category",
            f"There are {creativity_count} posts under “Creativity” — proof that math and art do mix here.",
        )

    # 5) Outlier posts: longest, shortest, link-heavy, image-heavy, symbol-heavy
    posts_sorted_by_len = sorted(posts, key=lambda p: p.word_count, reverse=True)
    for p in posts_sorted_by_len[:40]:
        pages = p.word_count / 250.0
        add(
            "length",
            f"Deep dive: “{p.title}” runs about {p.word_count} words ({pages:.1f} paperback pages) and was published on {format_date(p.date)}.",
            p.link,
        )

    for p in posts_sorted_by_len[-30:]:
        add(
            "length",
            f"Blink and you’ll miss it: “{p.title}” is only {p.word_count} words long ({format_date(p.date)}).",
            p.link,
        )

    posts_by_links = sorted(posts, key=lambda p: p.link_count, reverse=True)[:40]
    for p in posts_by_links:
        add(
            "links",
            f"“{p.title}” is one of the most link-happy posts, with {p.link_count} hyperlinks packed into {p.word_count} words.",
            p.link,
        )

    posts_by_images = sorted(posts, key=lambda p: p.image_count, reverse=True)[:30]
    for p in posts_by_images:
        add(
            "images",
            f"“{p.title}” is unusually visual for this blog, with {p.image_count} images on the page.",
            p.link,
        )

    posts_by_symbols = sorted(
        posts, key=lambda p: (p.symbols.get("pi", 0) + p.symbols.get("phi", 0) + p.symbols.get("Phi", 0) + p.symbols.get("infty", 0)), reverse=True
    )[:40]
    for p in posts_by_symbols:
        count_sym = p.symbols.get("pi", 0) + p.symbols.get("phi", 0) + p.symbols.get("Phi", 0) + p.symbols.get("infty", 0)
        if count_sym > 0:
            add(
                "symbols",
                f"“{p.title}” is especially symbol-heavy, with at least {count_sym} explicit occurrences of π, φ, or ∞.",
                p.link,
            )

    # 6) Rare term facts (many, but with varied phrasing)
    rares = [(t, df[t]) for t in df if df[t] == 1 and len(t) >= 6]
    rares_sorted = sorted(rares, key=lambda kv: (-len(kv[0]), kv[0]))

    # Map term -> first post containing it
    term_post: Dict[str, Post] = {}
    for p in posts:
        for t in set(p.tokens):
            if t in df and df[t] == 1 and len(t) >= 6 and t not in term_post:
                term_post[t] = p

    def rare_phrase(i: int, term: str, p: Post) -> str:
        date_str = format_date(p.date)
        if i % 4 == 0:
            return f"Hidden gem: the word “{term}” appears exactly once in the corpus, in “{p.title}” on {date_str}."
        elif i % 4 == 1:
            return f"Only one post ever uses “{term}”: “{p.title}”, published on {date_str}."
        elif i % 4 == 2:
            return f"Easter egg term “{term}” shows up in a single post: “{p.title}” ({date_str})."
        else:
            return f"If you spot “{term}” on this blog, you’re reading “{p.title}” from {date_str} — it never appears anywhere else."

    rare_limit = 1500  # plenty of rare-term facts
    for i, (term, _) in enumerate(rares_sorted):
        if i >= rare_limit:
            break
        p = term_post.get(term)
        if not p:
            continue
        add("rarity", rare_phrase(i, term, p), p.link)

    # 7) On-this-day picks: per day-of-year, choose an interesting post but phrase by density
    by_doy_posts: Dict[int, List[Post]] = defaultdict(list)
    for p in posts:
        doy = p.date.timetuple().tm_yday
        by_doy_posts[doy].append(p)

    for doy, plist in sorted(by_doy_posts.items()):
        count = len(plist)
        best = max(plist, key=lambda p: p.word_count)
        add(
            "on-this-day",
            f"Across the archive, {count} posts share the date {best.date.strftime('%b %d')} — one of them is “{best.title}” from {best.date.year}.",
            best.link,
        )

    # 8) Co-occurrence quirks for a few term pairs
    def posts_with_terms(a: str, b: str) -> List[Post]:
        result = []
        for p in posts:
            toks = set(p.tokens)
            if a in toks and b in toks:
                result.append(p)
        return result

    for a, b in [("fibonacci", "prime"), ("fibonacci", "golden"), ("bayesian", "markov"), ("cryptography", "privacy")]:
        plist = posts_with_terms(a, b)
        if plist:
            add(
                "co-occurrence",
                f"There are {len(plist)} posts that mention both “{a}” and “{b}”; “{plist[0].title}” is one of them.",
                plist[0].link,
            )

    # We expect >2000 facts; cap gently at ~2500 if needed
    if len(facts) > 2500:
        facts = facts[:2500]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "type", "fact", "source_link"])
        writer.writeheader()
        writer.writerows(facts)
    print(f"Wrote {len(facts)} candidate facts to {OUT}")


if __name__ == "__main__":
    main()

