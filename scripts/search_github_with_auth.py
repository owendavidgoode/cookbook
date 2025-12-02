#!/usr/bin/env python3
"""
Search GitHub code for johndcook.com citations using authenticated API.
"""

import json
import requests
import time
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "github_impact"
OUTPUT_DIR.mkdir(exist_ok=True)

import os
TOKEN = os.environ.get("GITHUB_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def search_code(query, per_page=30):
    """Search GitHub code."""
    url = "https://api.github.com/search/code"
    params = {"q": query, "per_page": per_page}

    resp = requests.get(url, headers=HEADERS, params=params)

    if resp.status_code == 200:
        return resp.json()
    elif resp.status_code == 403:
        print(f"  Rate limited or forbidden: {resp.json().get('message', '')}")
        return None
    else:
        print(f"  Error {resp.status_code}: {resp.text[:200]}")
        return None


def main():
    print("GitHub Code Search for johndcook.com citations")
    print("=" * 60)

    queries = [
        "johndcook.com/blog",
        "johndcook.com",
        "johndcook gamma",
        "johndcook random",
        "johndcook interpolation",
        "dont-invert-that-matrix",
        '"John D. Cook"',
    ]

    all_results = []
    seen_repos = set()

    for query in queries:
        print(f"\nSearching: '{query}'")
        time.sleep(2)  # Rate limiting

        result = search_code(query)
        if not result:
            continue

        total = result.get("total_count", 0)
        items = result.get("items", [])
        print(f"  Found: {total} results (showing {len(items)})")

        for item in items:
            repo = item.get("repository", {}).get("full_name", "")
            path = item.get("path", "")
            html_url = item.get("html_url", "")

            if repo not in seen_repos:
                seen_repos.add(repo)

                entry = {
                    "query": query,
                    "repo": repo,
                    "path": path,
                    "url": html_url,
                    "stars": item.get("repository", {}).get("stargazers_count", 0),
                }
                all_results.append(entry)
                print(f"    - {repo}: {path}")

    # Sort by stars
    all_results.sort(key=lambda x: x.get("stars", 0), reverse=True)

    # Save results
    with open(OUTPUT_DIR / "code_search_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    # Create markdown summary
    with open(OUTPUT_DIR / "code_citations.md", "w") as f:
        f.write("# GitHub Code Citations of johndcook.com\n\n")
        f.write(f"Total unique repositories found: {len(all_results)}\n\n")
        f.write("---\n\n")

        for i, r in enumerate(all_results[:30], 1):  # Top 30
            f.write(f"## {i}. [{r['repo']}]({r['url']})\n\n")
            f.write(f"- **Stars:** {r.get('stars', 0)}\n")
            f.write(f"- **File:** `{r['path']}`\n")
            f.write(f"- **Query:** `{r['query']}`\n\n")

    print(f"\n{'=' * 60}")
    print(f"Total unique repos: {len(all_results)}")
    print(f"Results saved to {OUTPUT_DIR}/")

    # Print top 10 by stars
    print("\nTop 10 by stars:")
    for r in all_results[:10]:
        print(f"  {r['stars']:5d} ★  {r['repo']}")


if __name__ == "__main__":
    main()
