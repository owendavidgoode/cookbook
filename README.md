# Cookbook: johndcook.com Data Projects

Utilities and datasets for extracting, analyzing, and repurposing content from johndcook.com/blog — 17 years and 5,233 posts of mathematical blogging.

## Projects

### 1. Calendar Facts (Primary)
A curated 365-day calendar of facts about the blog, suitable for a daily desk calendar or similar product.

**Status**: 365 facts curated from 9,000+ candidates across 21 categories.

**Key Files**:
- `data/johndcook_calendar_365.csv` — Final curated 365 facts
- `data/johndcook_calendar_candidates_filtered.csv` — 1,599 filtered candidates
- `data/johndcook_calendar_candidates_v3.csv` — 5,090 original candidates
- `data/new_deep_analysis_facts.csv` — 42 PhD-level analysis facts (twitter, scholar, code evolution, mathematicians)
- `data/new_analysis_facts.csv` — 37 GSC/crypto/tone/stats facts
- `data/hn_facts.csv` — 10 Hacker News impact facts

**Categories**:
- `otd` — On-this-day historical facts
- `stats` — PhD-level statistical analysis (Zipf's law, Heaps' law, autocorrelation, entropy)
- `gsc` — Google Search Console insights (traffic, CTR, geographic reach)
- `hn` — Hacker News impact (1,266 submissions, 25K+ upvotes, 4 posts with 500+ points)
- `code` — Programming language evolution (Perl→Python trajectory, Mathematica constant)
- `mathematician` — Most-referenced mathematicians (Euler 124, Fourier 65, Gauss 55)
- `crypto` — Cryptocurrency coverage (elliptic curves, Monero, Bitcoin)
- `twitter` — John's 20+ topic-specific Twitter accounts
- `scholar` — Academic impact (5,881 citations, 32 publications)
- `tools` — Standalone calculators (interpolation calculator drives 83.7% of search traffic)
- `tone` — Semantic analysis (86.4% first-person, explanatory style)
- `rarity`, `quirk`, `density`, `constant`, `span`, `evergreen`, `engagement`, `meta`

**To rebuild calendar with latest facts**:
```bash
cd data && python3 rebuild.py
```

### 2. Twitter Bot (Live)
Autonomous bot posting facts to [@jdc_facts](https://x.com/jdc_facts).

**Status**: Live and running. Posts at 8am + 6pm UTC (2x daily).

**Facts**: 427 facts from calendar, HN, GSC, and analysis sources (~7 months runway).

**How it works**: GitHub Actions runs `bot/post_fact.py` on schedule, picks random unposted fact, posts to X, tracks state.

**See**: `bot/README.md` for full documentation.

### 3. Book: *Methodical* (Planned)
A data-driven companion book celebrating johndcook.com/blog as a long-running, quietly influential institution.

**Title**: **Methodical: One Blog, Seventeen Years, 1.8 Million Words**  
**Subtitle**: A Data Portrait of John D. Cook's Blog

**See**:
- `book/OUTLINE_V4.md` — canonical content outline
- `book/PRODUCTION_SPEC.md` — audience, style, and production details
- `book/README.md` — start-here guide for drafting agents

**Structure (high level)**:
- **Front Matter** — Foreword, Prologue
- **Part I: The Architecture** — scale, categories, rhythm
- **Part II: The Obsessions** — constants, special functions, mathematicians
- **Part III: The Bridge** — programming languages and cryptography
- **Part IV: The Unexpected** — music, typography, Unicode, clinical trials, interviews
- **Part V: The Long View** — evolution over eras and what the numbers miss
- **Back Matter** — reference tables and a curated reading list

**Target**: ~175 pages, narrative-first with supporting visualizations; gift for Cook, readable by his audience and data-viz/blogging enthusiasts.

## Data Sources

### Blog Content
- `data/johndcook_posts_enriched.jsonl` — 5,233 posts with full content, categories, tags, word counts
- `data/johndcook_posts.jsonl` — Basic post extraction
- `data/johndcook_text_index.jsonl` — Text analysis index
- `data/posts_metadata.csv` — Post metadata

### External Data
- `data/gsc_exports/` — 16 months of Google Search Console data (queries, pages, countries, Discover)
- `data/wp_taxonomies/` — WordPress category and tag definitions

## Key Findings

### Traffic & Reach
- Interpolation calculator: 538,000+ clicks (83.7% of all search traffic)
- 244 countries reached; Romania has mysterious 9.98% CTR (2x global average)
- Tools drive 98% of search traffic; blog posts drive 59%

### Hacker News Impact
- 1,266 submissions over 17 years
- 25,486 total upvotes, 10,757 comments
- 4 posts exceeded 500 points (likely #1): "Organizing complexity" (742), "Software reuse" (667), "987654321/123456789" (637), "Rule of succession" (575)
- ColinWright submitted 112 posts — a superfan since 2009

### Academic Impact
- 5,881 Google Scholar citations
- 32 peer-reviewed publications + 13 MD Anderson working papers
- 13 years at MD Anderson Cancer Center (2000-2013) before independent consulting

### Code Language Evolution
- Python: 731 posts (lingua franca since ~2015)
- Mathematica: 782 posts (steady since 2008)
- Perl: 147 posts (2008-2014, now legacy)
- LaTeX: 783 posts (nearly every math post)
- 2015 was the Python inflection point (3x jump from 2014)

### Publication Consistency
- 17 years continuous publication
- Longest gap: 12 days (Feb 13-26, 2025)
- Peak: 26 consecutive days (Nov 13 - Dec 8, 2022)

### Mathematician References
- Euler: 124 posts (most-referenced)
- Fourier: 65 posts
- Gauss: 55 posts
- Riemann: 47 posts
- Ramanujan: 34 posts
- Living mathematicians: Terence Tao (15+), Donald Knuth (12+)

### Google Discover
- "Dungeons, Dragons, and Numbers" went viral: 3,282 clicks, 53,563 impressions
- "TV tuned to a dead channel" hit 5.04% CTR — literary references outperform

## Quick Start

```bash
# Extract posts from downloaded site
python3 src/extract_johndcook.py --source ../johndcook/app/public --output data/johndcook_posts.jsonl

# Generate calendar fact candidates
python3 scripts/generate_calendar_facts_opus.py

# Rebuild curated 365 with latest analysis facts
cd data && python3 rebuild.py
```

## Tooling
- Install dev deps: `make setup`
- Lint/test: `make lint` / `make test`
- Validate the canonical 365 set stays unchanged: `python -m cookbook.cli calendar validate`
- Snapshot the 365 for print/export: `python -m cookbook.cli calendar snapshot`
- Run candidate generators: `python -m cookbook.cli calendar candidates --version v4`
- Fetch/enrich/index data: `python -m cookbook.cli ingest wp-api|taxonomies|enrich|index`
- Bot: rebuild facts (`python -m cookbook.cli bot build`), validate (`python -m cookbook.cli bot validate`), post (`python -m cookbook.cli bot post --dry-run`)

## Legacy Scripts
- Older scripts in `data/` (e.g., `rebuild.py`, `rebuild_calendar.py`, `REBUILD_PLAN.md`) remain for reference but are deprecated. Use the CLI commands above instead. See `docs/legacy-scripts.md` for details.

## Requirements
- Python 3.x
- Optional but recommended: install repo deps with `make setup` (Typer/Tweepy for CLI/bot, pytest/ruff for validation)

## Notes
- Treat source blog data as read-only
- All generated artifacts go in `data/`
- Content preserves Unicode (Greek letters, math symbols)
- Calendar facts designed to be nerdy and technical — gift for a mathematician

## Session History

**2025-11-28**: Major analysis pass
- Integrated 16 months of Google Search Console data
- Scraped Hacker News API (1,266 submissions, 25K+ upvotes)
- Google Scholar citations (5,881)
- Deep code language evolution analysis (Perl→Python trajectory)
- Mathematician reference counts
- Twitter account network mapping (20+ topic accounts)
- Rebuilt calendar from 13 to 21 categories with 42 new PhD-level facts
- Twitter bot launched at @jdc_facts
