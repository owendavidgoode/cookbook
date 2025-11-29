# Calendar Rebuild Plan

## Current State
- Total facts: 365
- Categories: otd (84), quirk (74), rarity (68), stats (44), density (30), constant (15), span (13), gsc (11), hn (10), tone (6), crypto (6), links (3), first (1)

## New Facts to Add
- 42 new facts from new_deep_analysis_facts.csv
- Categories: twitter (3), scholar (4), code (13), mathematician (10), tools (4), evergreen (3), engagement (2), meta (3)

## Removal Strategy

### Rarity (remove 25 from 68 → keep 43)
Remove facts about common words that happened to appear once (not interesting):
- "discriminative", "differentiated", "epidemiologist", "freelance", "factorialpower"
- "insignificance", "discouragement", "geometrization", "improvisations", "harmonicnumber"
- "indistractable", "hookrightarrow", "embellishments", "experimentally", "exponentiating"
- "constructivist", "anthropologist", "inefficiencies", "groundbreaking", "circumscribing"
- "downloadstring", "entanglement", and similar single-word rarities

KEEP facts about:
- Real interesting words: "ambidextrously", "onomatopoeia", "pickle", "abacus", "crypt"
- Programming/tech terms: "Julia", "bleichenbacher", "backpropagation", "libphonenumber", "GDPR", "FDA"
- Cultural references: "Bach", "Mozart", "dinosaur", "pizza", "tea", "pancake", "elephant"

### OTD (remove 7 from 84 → keep 77)
Remove generic/meta posts (lowest value):
1. "Help wanted" (2014)
2. "Monthly highlights" (2017)
3. "Faint praise for Expression Web" (2008)
4. "Elephant lifespans in captivity" (2008)
5. "Business literature" (2010)
6. "Personal organization software" (2011)
7. "Carnival of Mathematics 235" (2025)

KEEP posts about specific mathematical/technical content and interesting topics.

### Quirk (remove 10 from 74 → keep 64)
Remove the first 10 facts (arbitrary, as they're all roughly equal value).

## Execution
Run `python3 rebuild.py` to:
1. Load johndcook_calendar_365.csv (365 facts)
2. Remove 42 weaker facts (25 rarity + 7 otd + 10 quirk)
3. Add 42 new facts from new_deep_analysis_facts.csv
4. Renumber all facts sequentially 1-365
5. Write back to johndcook_calendar_365.csv

## Expected Final Distribution
- code: 13 (NEW)
- otd: 77 (was 84, removed 7)
- quirk: 64 (was 74, removed 10)
- stats: 44 (unchanged)
- rarity: 43 (was 68, removed 25)
- density: 30 (unchanged)
- constant: 15 (unchanged)
- span: 13 (unchanged)
- gsc: 11 (unchanged)
- mathematician: 10 (NEW)
- hn: 10 (unchanged)
- tone: 6 (unchanged)
- crypto: 6 (unchanged)
- scholar: 4 (NEW)
- tools: 4 (NEW)
- twitter: 3 (NEW)
- evergreen: 3 (NEW)
- links: 3 (unchanged)
- engagement: 2 (NEW)
- meta: 3 (NEW)
- first: 1 (unchanged)

Total: 365 facts
