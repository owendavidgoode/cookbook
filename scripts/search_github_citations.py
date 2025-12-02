#!/usr/bin/env python3
"""
Search GitHub for citations of johndcook.com in code and documentation.
Note: GitHub search API requires authentication for code search.
This script uses the web search as a fallback approach.
"""

import json
import requests
import time
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "github_impact"
OUTPUT_DIR.mkdir(exist_ok=True)


def search_github_code_web(query):
    """
    Search GitHub code via web (no auth required, but rate limited).
    Returns search result URLs for manual review.
    """
    # GitHub code search URL format
    search_url = f"https://github.com/search?q={query}&type=code"
    return search_url


def generate_search_queries():
    """Generate search queries for different citation patterns."""
    queries = [
        # Direct URL citations
        '"johndcook.com/blog"',
        '"www.johndcook.com"',

        # Specific popular posts
        '"dont-invert-that-matrix"',
        '"gamma-function"',
        '"gamma_function"',
        '"johndcook" gamma',
        '"johndcook" interpolation',
        '"johndcook" random',

        # Code patterns (function names from his posts)
        '"johndcook" scipy',
        '"johndcook" python statistics',

        # Documentation citations
        '"John D. Cook" reference',
        '"John Cook" blog math',
    ]
    return queries


def main():
    print("GitHub Citation Search Queries")
    print("=" * 60)
    print("\nThese queries can be run manually on GitHub:")
    print("(GitHub code search requires login)\n")

    queries = generate_search_queries()

    results = []
    for i, query in enumerate(queries, 1):
        url = search_github_code_web(query)
        print(f"{i}. {query}")
        print(f"   {url}\n")
        results.append({
            "query": query,
            "url": url,
        })

    # Save queries for reference
    with open(OUTPUT_DIR / "search_queries.json", "w") as f:
        json.dump(results, f, indent=2)

    # Create markdown file with instructions
    with open(OUTPUT_DIR / "github_search_instructions.md", "w") as f:
        f.write("# GitHub Citation Search Instructions\n\n")
        f.write("GitHub code search requires authentication. Run these searches manually:\n\n")

        for i, r in enumerate(results, 1):
            f.write(f"## {i}. `{r['query']}`\n\n")
            f.write(f"[Search GitHub]({r['url']})\n\n")

        f.write("---\n\n")
        f.write("## What to Look For\n\n")
        f.write("1. **Code comments** citing johndcook.com as source\n")
        f.write("2. **README files** recommending his blog\n")
        f.write("3. **Documentation** referencing his explanations\n")
        f.write("4. **Implementations** based on his code snippets\n")
        f.write("5. **Test files** using his examples\n\n")
        f.write("## Recording Findings\n\n")
        f.write("For each significant finding, record:\n")
        f.write("- Repository name and stars\n")
        f.write("- File path\n")
        f.write("- Relevant code/comment excerpt\n")
        f.write("- How it demonstrates impact\n")

    print(f"\nInstructions saved to {OUTPUT_DIR}/github_search_instructions.md")

    # Now try the GitHub API search for repos (doesn't require auth)
    print("\n" + "=" * 60)
    print("Searching GitHub repos via API...")

    try:
        # Search repos that mention johndcook
        resp = requests.get(
            "https://api.github.com/search/repositories",
            params={"q": "johndcook", "sort": "stars", "per_page": 20},
            headers={"Accept": "application/vnd.github.v3+json"}
        )

        if resp.status_code == 200:
            data = resp.json()
            print(f"\nRepositories mentioning 'johndcook': {data.get('total_count', 0)}")

            repos = []
            for item in data.get("items", []):
                repo = {
                    "name": item["full_name"],
                    "stars": item["stargazers_count"],
                    "description": item.get("description", ""),
                    "url": item["html_url"],
                }
                repos.append(repo)
                print(f"  - {repo['name']} ({repo['stars']} stars)")

            with open(OUTPUT_DIR / "repos_mentioning_johndcook.json", "w") as f:
                json.dump(repos, f, indent=2)
        else:
            print(f"API error: {resp.status_code}")

    except Exception as e:
        print(f"Error searching repos: {e}")

    print("\n" + "=" * 60)
    print("Next step: Run code searches manually on GitHub (requires login)")


if __name__ == "__main__":
    main()
