#!/usr/bin/env python3
"""Build facts.json from all CSV sources."""

from pathlib import Path

from cookbook import bot_utils


def main() -> None:
    bot_dir = Path(__file__).parent
    facts = bot_utils.build_facts(max_length=260)
    bot_utils.write_facts_json(facts, bot_dir / "facts.json")
    print(f"Written {len(facts)} facts to {bot_dir / 'facts.json'}")
    if facts:
        print("\nSample facts:")
        for fact in facts[:3]:
            print(f"  [{fact.get('type')}] {fact.get('text','')[:80]}...")


if __name__ == "__main__":
    main()
