# Facts Pool QA Checklist

Use this document to verify the quality of `bot/facts.json` after any regeneration or modification.

## Quick Validation Commands

```bash
# Count total facts (target: 365)
python3 -c "import json; f=json.load(open('bot/facts.json')); print(f'Total: {len(f)}')"

# Distribution by type
python3 -c "
import json
from collections import Counter
facts = json.load(open('bot/facts.json'))
for t, c in Counter(f.get('type','?') for f in facts).most_common():
    print(f'{t}: {c}')
"
```

## Quality Criteria

### Required Types (from gold standard 365)
These types MUST be present in any quality facts pool:

| Type | Min Count | Description |
|------|-----------|-------------|
| `stats` | 100+ | Blog statistics with insights |
| `rarity` | 40+ | Unique word/tag appearances |
| `content` | 50+ | Content patterns and analysis |
| `quirk` | 20+ | Engaging hooks and surprises |
| `evolution` | 15+ | How topics changed over time |
| `span` | 10+ | Topic longevity across years |
| `code` | 10+ | Programming language insights |
| `hn` | 5+ | Hacker News performance |
| `mathematician` | 5+ | Referenced mathematicians |
| `density` | 10+ | Longest/shortest/most-visual posts |

### Patterns to REJECT

These patterns indicate low-quality facts that should be filtered out:

```python
# Generic yearly counts - REJECT
"In 2008, 410 posts were published on the blog."

# Generic day-of-week counts - REJECT
"Tuesday has 1003 blog posts published on that day of the week."

# Generic month counts - REJECT
"October has seen 480 blog posts over the years."

# Generic category counts - REJECT
"The 'Math' category contains 2378 posts."

# Generic OTD (no highlight) - REJECT
"On November 27, 2025: 'Equal things that don't look equal' was published."
"The earliest November 27 post was 'The Tangled Web' in 2011."

# Generic constant mentions - REJECT
"The mathematical symbol π appears across 404 different posts on the blog."

# Very short facts (<60 chars) - REJECT
"In 2014, 147 posts were published."
```

### Patterns to KEEP

These patterns indicate high-quality facts:

```python
# Specific rarity with title - KEEP
"The word 'pickle' appears in only one blog post: \"Dump a pickle file...\" on August 16, 2022."

# Tag used exactly once - KEEP
"The tag 'Etymology' was used exactly once, in \"Two meanings of 'argument'\" (2010)."

# Stats with insight and voice - KEEP
"Tuesday is the blog's favorite day: 1,003 posts. Sunday trails with 466—even mathematicians rest."
"103 posts explore prime numbers—nearly 2% of the blog is dedicated to these mathematical atoms."

# Span facts - KEEP
"'Python' spans the blog from 2008 to 2025: first in \"Three-hour-a-week language\", most recently in..."
"'Riemann' spans the blog from 2012 to 2025: first in \"Equivalent form of the Riemann hypothesis\", most recently in..."

# First mentions - KEEP
"The first mention of 'FDA' on the blog was on June 19, 2008 in \"Bugs in food and software\"."

# Quirks with character - KEEP
"'An elegant proof from Erdős'—elegance appears in exactly one title on the entire blog."
"Only 4 posts mention 'impossible'—the blog prefers possibilities to limitations."
```

## Spot Check Process

1. **Random sample 20 facts** and verify each is tweetable:
   ```bash
   python3 -c "
   import json, random
   facts = json.load(open('bot/facts.json'))
   for f in random.sample(facts, 20):
       print(f['type'][:8].ljust(8), f['text'][:80])
       print()
   "
   ```

2. **Check for duplicates:**
   ```bash
   python3 -c "
   import json
   facts = json.load(open('bot/facts.json'))
   texts = [f['text'].lower().strip() for f in facts]
   dupes = len(texts) - len(set(texts))
   print(f'Duplicates: {dupes}')
   "
   ```

3. **Check length distribution** (tweets should be <280 chars):
   ```bash
   python3 -c "
   import json
   facts = json.load(open('bot/facts.json'))
   lengths = [len(f['text']) for f in facts]
   over_280 = sum(1 for l in lengths if l > 280)
   print(f'Over 280 chars: {over_280}/{len(facts)}')
   print(f'Avg length: {sum(lengths)/len(lengths):.0f} chars')
   "
   ```

## Gold Standard Reference

The current 365 facts were methodically generated from the corpus data (`data/posts_metadata.csv`) using patterns from the original gold standard. The target is exactly 365 facts—one for each day of the year.

## Regeneration

If you need to regenerate facts.json:

1. Start from the corpus data in `data/posts_metadata.csv`
2. Generate facts one at a time, checking for duplicates
3. Apply strict quality filters (see patterns above)
4. Target exactly 365 facts with good voice

## Sign-off

After QA, update this section:

- **Last QA Date:** 2025-11-29
- **Fact Count:** 365
- **QA Agent:** Claude (Opus 4.5)
- **Status:** ✓ Passed
- **Checks:**
  - 0 duplicates
  - 0 facts over 280 characters
  - 0 HTML entities
  - All facts have IDs
  - 24 distinct fact types
