#!/usr/bin/env python3
"""
Rebuild the johndcook_calendar_365.csv by:
1. Removing 42 weaker facts to make room
2. Adding 42 new high-quality facts
3. Renumbering sequentially
"""

import csv
from collections import defaultdict

# Read current calendar
current_facts = []
with open('johndcook_calendar_365.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        current_facts.append(row)

# Read new facts
new_facts = []
with open('new_deep_analysis_facts.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        new_facts.append(row)

print(f"Current facts: {len(current_facts)}")
print(f"New facts to add: {len(new_facts)}")

# Group current facts by category
by_category = defaultdict(list)
for fact in current_facts:
    by_category[fact['type']].append(fact)

print("\nCurrent distribution:")
for cat in sorted(by_category.keys(), key=lambda x: len(by_category[x]), reverse=True):
    print(f"  {cat}: {len(by_category[cat])}")

# Strategy: Remove ~25 from rarity, ~10 from quirk, ~7 from otd
# Priority: Keep real words in rarity, keep interesting titles in otd

# For rarity: Remove facts with gibberish/random patterns, keep real words
rarity_to_keep = []
rarity_to_remove = []

# Keywords that suggest "interesting" rarity facts vs gibberish
interesting_keywords = [
    'word', 'letter', 'english', 'dictionary', 'language', 'sentence',
    'phrase', 'text', 'book', 'title', 'name', 'palindrome', 'poem'
]

for fact in by_category['rarity']:
    fact_lower = fact['fact'].lower()
    # Check if this is about real words/language vs random patterns
    has_interesting = any(kw in fact_lower for kw in interesting_keywords)

    # Keep facts about language/words, remove random patterns
    if has_interesting or 'pangram' in fact_lower or 'lipogram' in fact_lower:
        rarity_to_keep.append(fact)
    else:
        rarity_to_remove.append(fact)

print(f"\nRarity analysis:")
print(f"  Total: {len(by_category['rarity'])}")
print(f"  To keep (interesting): {len(rarity_to_keep)}")
print(f"  To remove (gibberish): {len(rarity_to_remove)}")

# Take only the first 25 to remove from rarity
rarity_removed = rarity_to_remove[:25]
rarity_kept = rarity_to_keep + rarity_to_remove[25:]

print(f"  Actually removing: {len(rarity_removed)}")
print(f"  Actually keeping: {len(rarity_kept)}")

# For otd: Remove less interesting titles (prefer recent, specific, or unique topics)
# Less interesting: generic titles, meta posts, very old posts
otd_scored = []
for fact in by_category['otd']:
    score = 0
    fact_lower = fact['fact'].lower()

    # Boost for specific mathematical/technical content
    if any(kw in fact_lower for kw in ['theorem', 'formula', 'function', 'equation', 'algorithm', 'proof']):
        score += 3

    # Boost for interesting topics
    if any(kw in fact_lower for kw in ['pi', 'euler', 'fibonacci', 'fractal', 'chaos', 'crypto', 'quantum']):
        score += 2

    # Penalty for meta/generic
    if any(kw in fact_lower for kw in ['highlight', 'posts', 'help wanted', 'monthly', 'carnival']):
        score -= 2

    # Boost for recent years (2020+)
    if 'date' in fact and fact['date']:
        year = fact['date'][:4]
        if year >= '2020':
            score += 1

    otd_scored.append((score, fact))

# Sort by score (lowest first = remove these)
otd_scored.sort(key=lambda x: x[0])

otd_removed = [f for s, f in otd_scored[:7]]
otd_kept = [f for s, f in otd_scored[7:]]

print(f"\nOTD analysis:")
print(f"  Total: {len(by_category['otd'])}")
print(f"  Removing: {len(otd_removed)}")
print(f"  Keeping: {len(otd_kept)}")

# For quirk: Remove 10 least interesting (arbitrary - just take first 10)
quirk_removed = by_category['quirk'][:10]
quirk_kept = by_category['quirk'][10:]

print(f"\nQuirk analysis:")
print(f"  Total: {len(by_category['quirk'])}")
print(f"  Removing: {len(quirk_removed)}")
print(f"  Keeping: {len(quirk_kept)}")

print(f"\nTotal removing: {len(rarity_removed) + len(otd_removed) + len(quirk_removed)}")

# Build new fact list
kept_facts = []

# Add all kept facts from modified categories
kept_facts.extend(rarity_kept)
kept_facts.extend(otd_kept)
kept_facts.extend(quirk_kept)

# Add all facts from unchanged categories
for cat in by_category:
    if cat not in ['rarity', 'otd', 'quirk']:
        kept_facts.extend(by_category[cat])

print(f"\nKept facts from original: {len(kept_facts)}")

# Add new facts with proper formatting
for new_fact in new_facts:
    kept_facts.append({
        'id': '0',  # Will renumber
        'type': new_fact['type'],
        'fact': new_fact['fact'],
        'source_link': 'https://www.johndcook.com/blog/',
        'date': '',
        'slug': ''
    })

print(f"After adding new facts: {len(kept_facts)}")

# Renumber sequentially
for i, fact in enumerate(kept_facts, 1):
    fact['id'] = str(i)

# Count final distribution
final_dist = defaultdict(int)
for fact in kept_facts:
    final_dist[fact['type']] += 1

print("\nFinal distribution:")
for cat in sorted(final_dist.keys(), key=lambda x: final_dist[x], reverse=True):
    print(f"  {cat}: {final_dist[cat]}")

# Write updated calendar
with open('johndcook_calendar_365.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['id', 'type', 'fact', 'source_link', 'date', 'slug']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(kept_facts)

print(f"\nWrote {len(kept_facts)} facts to johndcook_calendar_365.csv")
