# Methodical Data Notes (Skeleton)

This file maps book chapters to data sources and scripts. It is a working document for anyone generating or regenerating visuals and tables.

## Conventions

- **Data sources** live under `data/` and are treated as read-only.
- **Analysis / visualization scripts** live under `scripts/` or `src/cookbook/`.
- **Outputs for the book** (figures, intermediate tables) should be written to `book/figures/` or an equivalent book-specific subfolder, not back into `data/`.

## Part I: The Architecture

### Chapter 1: The Shape of Seventeen Years
- Data:
  - `data/posts_metadata.csv` (dates, word counts, per-year aggregates)
- Scripts:
  - `scripts/explore_facts.py` (reference patterns / examples)
  - (To be added) `scripts/generate_chapter_1_visuals.py`
- Outputs:
  - Suggested folder: `book/figures/part-01/ch01/`

### Chapter 2: The Topography of Interest
- Data:
  - `data/posts_metadata.csv` (categories field)
  - `data/wp_taxonomies/categories.json`
- Scripts:
  - (To be added) `scripts/generate_chapter_2_visuals.py` (or equivalent)
- Outputs:
  - Suggested folder: `book/figures/part-01/ch02/`

### Chapter 3: The Rhythm of a Working Mind
- Data:
  - `data/posts_metadata.csv` (timestamp fields: date, year, month, weekday)
- Scripts:
  - (To be added) `scripts/generate_chapter_3_visuals.py`
- Outputs:
  - Suggested folder: `book/figures/part-01/ch03/`

## Part II: The Obsessions

### Chapter 4: The Numbers That Keep Appearing
- Data:
  - `data/johndcook_text_index.jsonl` (term-level counts)
  - `data/posts_metadata.csv` (titles, dates)
- Scripts:
  - (To be added) `scripts/generate_chapter_4_visuals.py`

### Chapter 5: A Bestiary of Functions
- Data:
  - `data/johndcook_text_index.jsonl`
  - `data/johndcook_posts_enriched.jsonl`
- Scripts:
  - (To be added) `scripts/generate_chapter_5_visuals.py`

### Chapter 6: The Mathematicians Behind the Theorems
- Data:
  - `data/johndcook_text_index.jsonl`
  - `data/johndcook_posts_enriched.jsonl`
- Scripts:
  - (To be added) `scripts/generate_chapter_6_visuals.py`

## Part III–V

For Parts III–V, follow the same pattern:

- List the primary data files (for example, cryptography/privacy term counts, language tags, interview post IDs).
- Link to any chapter-specific scripts in `scripts/` that generate figures or helper tables.
- Record output locations under `book/figures/part-0X/chYY/`.

As chapters are implemented, replace the "(To be added)" placeholders with actual script paths and briefly document any non-obvious preprocessing steps.

