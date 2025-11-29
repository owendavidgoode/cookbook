#!/usr/bin/env python3
"""Trim wordy commentary from facts.json while preserving genuine insights."""

import json
import re

# Load facts
with open("bot/facts.json") as f:
    facts = json.load(f)

# Patterns to remove (after em-dash or period)
TRIM_PATTERNS = [
    # Generic filler after em-dash
    r"—a meditation on[^.]+\.",
    r"—the power of[^.]+\.",
    r"—proof that[^.]+\.",
    r"—where [^.]+\.",
    r"—sometimes [^.]+\.",
    r"—even [^.]+\.",
    r"—the blog[^.]+\.",
    r"—one [^.]+\.",
    r"—a true [^.]+\.",
    r"—a surprisingly[^.]+\.",
    r"—this is [^.]+\.",
    r"—the intersection[^.]+\.",
    r"—a rare [^.]+\.",
    r"—more reliable[^.]+\.",
    r"—a classic [^.]+\.",
    r"—roughly [^.]+\.",
    r"—approximately [^.]+\.",
    r"—mathematics [^.]+\.",
    r"—Uncertainty[^.]+\.",
    r"—ancient math[^.]+\.",
    r"—that irrational[^.]+\.",
    r"—your encrypted[^.]+\.",
    r"—each one [^.]+\.",
    r"—the sequence[^.]+\.",
    r"—nearly [^.]+\.",
    r"—two [^.]+\.",
    r"—from the familiar[^.]+\.",
    r"—every shape[^.]+\.",
    r"—the building blocks[^.]+\.",
    r"—foundations[^.]+\.",
    r"—the blog's pace[^.]+\.",
    r"—linear algebra[^.]+\.",
    r"—the blog doesn't[^.]+\.",
    r"—why settle[^.]+\.",
    r"—probability as[^.]+\.",
    r"—the blog goes[^.]+\.",
    r"—abstract[^.]+\.",
    r"—the blog is [^.]+\.",
    r"—relativity[^.]+\.",
    r"—the blog reaches[^.]+\.",
    r"—not just what[^.]+\.",
    r"—cause and effect[^.]+\.",
    r"—sometimes what[^.]+\.",
    r"—math that computes[^.]+\.",
    r"—the blog explores[^.]+\.",
    r"—mathematical certainty[^.]+\.",
    r"—the blog prefers[^.]+\.",
    r"—mathematics as play[^.]+\.",
    r"—entropy is[^.]+\.",
    r"—the word[^.]+\.",
    r"—one of only[^.]+\.",
    r"—crossing disciplines[^.]+\.",
    r"—the blog plays[^.]+\.",
    r"—simplicity is[^.]+\.",
    r"—and they deliver[^.]+\.",
    r"—two approaches[^.]+\.",
    r"—the shortest of[^.]+\.",
    r"—sometimes cleverness[^.]+\.",
    r"—almost 1 in[^.]+\.",
    r"—some languages age[^.]+\.",
    r"—technology growing[^.]+\.",
    r"—16-dimensional[^.]+\.",
    r"—currency gets[^.]+\.",
    r"—each mathematically[^.]+\.",

    # Filler after periods (sentence-final commentary)
    r"\. A meditation[^.]+\.$",
    r"\. The blog [^.]+\.$",
    r"\. Ancient computing[^.]+\.$",
    r"\. Neural network[^.]+\.$",
    r"\. Google's phone[^.]+\.$",
    r"\. Word origins[^.]+\.$",
    r"\. Perelman's proof[^.]+\.$",
    r"\. Jazz meets[^.]+\.$",
    r"\. GPU computing[^.]+\.$",
    r"\. Back when[^.]+\.$",
    r"\. A math blog[^.]+\.$",
    r"\. Ironic—[^.]+\.$",
    r"\. Python exceptions[^.]+\.$",
    r"\. A German math book[^.]+\.$",
    r"\. A coined word[^.]+\.$",
    r"\. Predictions from[^.]+\.$",
    r"\. Even a math blog[^.]+\.$",
    r"\. A shoutout[^.]+\.$",
    r"\. Snowflakes as[^.]+\.$",
    r"\. Medical regulation[^.]+\.$",
    r"\. The tools are[^.]+\.$",
    r"\. Literary references[^.]+\.$",
    r"\. Explanatory writing[^.]+\.$",
    r"\. Inquisitive but[^.]+\.$",
    r"\. The statistical[^.]+\.$",
    r"\. Digital currency[^.]+\.$",
    r"\. A super-fan[^.]+\.$",
    r"\. Old blog, new[^.]+\.$",
    r"\. The comeback year[^.]+\.$",
    r"\. Some topics need[^.]+\.$",
    r"\. Theory meets[^.]+\.$",
    r"\. Statistics served[^.]+\.$",
    r"\. Wall Street[^.]+\.$",
    r"\. The heavens[^.]+\.$",
    r"\. Curiosity drives[^.]+\.$",
    r"\. High praise[^.]+\.$",
    r"\. Sometimes the punchline[^.]+\.$",
    r"\. The best proofs[^.]+\.$",
    r"\. Mathematics has[^.]+\.$",
    r"\. Both paths[^.]+\.$",
    r"\. Creative insights[^.]+\.$",
    r"\. Not every optimization[^.]+\.$",
    r"\. The best ideas[^.]+\.$",

    # Specific verbose patterns
    r" Composition matters\.$",
    r" Concision as an art form\. Sometimes less really is more\.$",
    r" Maximum density achieved\.$",
    r" One tool, many domains\.$",
    r" Why prove something can't be done\?$",
    r" Chaos, tamed by mathematics\.$",
    r" Indivisible and essential\.$",
    r" Sound waves are just vibrating math\.$",
    r" Arrows and objects all the way down\.$",
    r" Let chance do the heavy lifting\.$",
    r" Randomness shows up everywhere, even in post titles\.$",
    r" The blog reserves aesthetic judgments for the extraordinary\.$",
    r" Recreational math isn't an oxymoron on this blog\.$",
    r" Sometimes the best proof is a picture\.$",
]

def trim_fact(text):
    """Remove wordy commentary while preserving the core fact."""
    original = text

    for pattern in TRIM_PATTERNS:
        text = re.sub(pattern, ".", text)

    # Clean up double periods
    text = re.sub(r"\.+", ".", text)

    # Clean up orphaned em-dashes at end
    text = re.sub(r"—\.$", ".", text)
    text = re.sub(r"—$", ".", text)

    # Clean up whitespace
    text = text.strip()

    return text

# Process each fact
changes = 0
for fact in facts:
    original = fact["text"]
    trimmed = trim_fact(original)
    if trimmed != original:
        print(f"ID {fact['id']}:")
        print(f"  BEFORE: {original[:100]}...")
        print(f"  AFTER:  {trimmed[:100]}...")
        print()
        fact["text"] = trimmed
        changes += 1

print(f"\n{changes} facts modified out of {len(facts)}")

# Save
with open("bot/facts.json", "w") as f:
    json.dump(facts, f, indent=2)

print("Saved to bot/facts.json")
