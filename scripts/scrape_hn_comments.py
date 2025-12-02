#!/usr/bin/env python3
"""
Scrape Hacker News comments about johndcook.com via Algolia API.
Target: Find 15+ quotes demonstrating reader impact/application.
"""

import json
import requests
import time
from pathlib import Path
from html import unescape
import re

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "hn_impact"
OUTPUT_DIR.mkdir(exist_ok=True)

BASE_URL = "https://hn.algolia.com/api/v1"


def strip_html(text):
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def search_comments(query, page=0, hits_per_page=100):
    """Search HN comments via Algolia API."""
    params = {
        "query": query,
        "tags": "comment",
        "hitsPerPage": hits_per_page,
        "page": page,
    }
    resp = requests.get(f"{BASE_URL}/search", params=params)
    resp.raise_for_status()
    return resp.json()


def search_stories(query, page=0, hits_per_page=100):
    """Search HN stories via Algolia API."""
    params = {
        "query": query,
        "tags": "story",
        "hitsPerPage": hits_per_page,
        "page": page,
    }
    resp = requests.get(f"{BASE_URL}/search", params=params)
    resp.raise_for_status()
    return resp.json()


def get_story_comments(story_id):
    """Get all comments for a specific story."""
    resp = requests.get(f"{BASE_URL}/items/{story_id}")
    resp.raise_for_status()
    return resp.json()


def is_testimonial(text):
    """
    Heuristic: Does this comment suggest personal use/impact?
    Looking for: "I used", "helped me", "finally understood", "bookmarked",
    "production", "our system", "my research", etc.
    """
    text_lower = text.lower()

    # Strong indicators of personal impact
    strong_signals = [
        "i use", "i used", "i've used", "we use", "we used",
        "helped me", "helped us", "finally understood", "finally made sense",
        "bookmarked", "bookmark this", "saved this",
        "in production", "our production", "my production",
        "at work", "in our codebase", "our system",
        "my research", "our research", "my thesis", "my dissertation",
        "learned from", "taught me", "explained it",
        "go-to resource", "go to resource", "reference this",
        "changed how i", "changed the way i",
        "best explanation", "clearest explanation",
        "wish i had found", "years ago",
    ]

    # Weaker but still useful
    medium_signals = [
        "his blog", "cook's blog", "johndcook",
        "great resource", "invaluable", "indispensable",
        "recommend", "essential reading",
    ]

    strong_count = sum(1 for s in strong_signals if s in text_lower)
    medium_count = sum(1 for s in medium_signals if s in text_lower)

    # Require at least one strong signal, or multiple medium signals
    return strong_count >= 1 or medium_count >= 2


def extract_testimonials(comments):
    """Filter comments to likely testimonials."""
    testimonials = []

    for comment in comments:
        text = comment.get("comment_text", "")
        if not text:
            continue

        clean_text = strip_html(text)

        if len(clean_text) < 50:  # Too short to be meaningful
            continue
        if len(clean_text) > 2000:  # Too long, probably not a testimonial
            continue

        if is_testimonial(clean_text):
            testimonials.append({
                "text": clean_text,
                "author": comment.get("author"),
                "created_at": comment.get("created_at"),
                "story_title": comment.get("story_title"),
                "story_url": comment.get("story_url"),
                "comment_id": comment.get("objectID"),
                "story_id": comment.get("story_id"),
                "hn_url": f"https://news.ycombinator.com/item?id={comment.get('objectID')}",
            })

    return testimonials


def main():
    print("Scraping HN comments about johndcook.com...")
    print("=" * 60)

    all_comments = []
    all_testimonials = []

    # Search strategies
    queries = [
        "johndcook.com",
        "johndcook blog",
        "john d cook",
        '"john cook" math',
        '"john cook" statistics',
    ]

    for query in queries:
        print(f"\nSearching: '{query}'")

        for page in range(5):  # Up to 500 comments per query
            try:
                result = search_comments(query, page=page)
                hits = result.get("hits", [])

                if not hits:
                    break

                all_comments.extend(hits)
                print(f"  Page {page}: {len(hits)} comments")

                time.sleep(0.5)  # Rate limiting

            except Exception as e:
                print(f"  Error on page {page}: {e}")
                break

    # Deduplicate by comment ID
    seen_ids = set()
    unique_comments = []
    for c in all_comments:
        cid = c.get("objectID")
        if cid and cid not in seen_ids:
            seen_ids.add(cid)
            unique_comments.append(c)

    print(f"\nTotal unique comments: {len(unique_comments)}")

    # Extract testimonials
    testimonials = extract_testimonials(unique_comments)
    print(f"Potential testimonials found: {len(testimonials)}")

    # Save all comments
    with open(OUTPUT_DIR / "all_comments.json", "w") as f:
        json.dump(unique_comments, f, indent=2)

    # Save testimonials
    with open(OUTPUT_DIR / "testimonials.json", "w") as f:
        json.dump(testimonials, f, indent=2)

    # Save testimonials as readable markdown
    with open(OUTPUT_DIR / "testimonials.md", "w") as f:
        f.write("# HN Testimonials about johndcook.com\n\n")
        f.write(f"Scraped: {time.strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Total comments searched: {len(unique_comments)}\n")
        f.write(f"Testimonials found: {len(testimonials)}\n\n")
        f.write("---\n\n")

        for i, t in enumerate(testimonials, 1):
            f.write(f"## {i}. {t['author']} ({t['created_at'][:10]})\n\n")
            f.write(f"**Context:** {t['story_title']}\n\n")
            f.write(f"> {t['text']}\n\n")
            f.write(f"[Comment link]({t['hn_url']})\n\n")
            f.write("---\n\n")

    print(f"\nOutput saved to {OUTPUT_DIR}/")
    print("  - all_comments.json")
    print("  - testimonials.json")
    print("  - testimonials.md")

    # Print sample testimonials
    print("\n" + "=" * 60)
    print("SAMPLE TESTIMONIALS:")
    print("=" * 60)

    for t in testimonials[:5]:
        print(f"\n--- {t['author']} ---")
        print(t['text'][:300] + "..." if len(t['text']) > 300 else t['text'])


if __name__ == "__main__":
    main()
