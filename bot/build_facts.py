#!/usr/bin/env python3
"""Build facts.json from all CSV sources."""

import csv
import json
from pathlib import Path


def load_csv_facts(csv_path: Path, has_header: bool = True) -> list[dict]:
    """Load facts from a CSV file."""
    facts = []
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f) if has_header else csv.reader(f)
        for row in reader:
            if has_header:
                fact_text = row.get("fact", "").strip()
                source_url = row.get("source_link", "").strip()
                fact_type = row.get("type", "general").strip()
                slug = row.get("slug", "").strip()
            else:
                continue  # Skip non-header CSVs for now

            if fact_text and len(fact_text) <= 280:
                facts.append({
                    "text": fact_text,
                    "source_url": source_url if source_url else None,
                    "type": fact_type,
                    "slug": slug if slug else None,
                    "source_file": csv_path.name
                })
    return facts


def main():
    data_dir = Path(__file__).parent.parent / "data"
    bot_dir = Path(__file__).parent

    all_facts = []

    # Primary source: calendar facts
    calendar_365 = data_dir / "johndcook_calendar_365.csv"
    if calendar_365.exists():
        facts = load_csv_facts(calendar_365)
        print(f"Loaded {len(facts)} from johndcook_calendar_365.csv")
        all_facts.extend(facts)

    # HN facts
    hn_facts = data_dir / "hn_facts.csv"
    if hn_facts.exists():
        facts = load_csv_facts(hn_facts)
        print(f"Loaded {len(facts)} from hn_facts.csv")
        all_facts.extend(facts)

    # GSC/analysis facts
    analysis_facts = data_dir / "new_analysis_facts.csv"
    if analysis_facts.exists():
        facts = load_csv_facts(analysis_facts)
        print(f"Loaded {len(facts)} from new_analysis_facts.csv")
        all_facts.extend(facts)

    # Additional PhD facts
    phd_facts = data_dir / "additional_phd_facts.csv"
    if phd_facts.exists():
        facts = load_csv_facts(phd_facts)
        print(f"Loaded {len(facts)} from additional_phd_facts.csv")
        all_facts.extend(facts)

    # Assign IDs
    for i, fact in enumerate(all_facts, start=1):
        fact["id"] = i

    # Filter out any that are too long for Twitter
    valid_facts = [f for f in all_facts if len(f["text"]) <= 260]  # Leave room for link
    print(f"\nTotal valid facts (<=260 chars): {len(valid_facts)}")

    # Write to facts.json
    output_path = bot_dir / "facts.json"
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(valid_facts, f, indent=2, ensure_ascii=False)

    print(f"Written to {output_path}")

    # Show some samples
    print("\nSample facts:")
    for fact in valid_facts[:3]:
        print(f"  [{fact['type']}] {fact['text'][:80]}...")


if __name__ == "__main__":
    main()
