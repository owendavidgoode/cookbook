# Cookbook Refactoring Plan

**Author**: Claude
**Date**: December 1, 2025
**Status**: Plan only — do not execute without approval

---

## Executive Summary

The cookbook repository has evolved organically from exploration to production. Three services now exist (calendar, bot, book), but they grew independently and the codebase reflects this history: a hybrid architecture with a proper Python package (`src/cookbook/`) that wraps legacy standalone scripts (`src/*.py`) rather than containing the logic directly.

This plan consolidates the codebase into a clean, maintainable structure while preserving the canonical 365-fact calendar as immutable.

### What's Working (Don't Break It)

- **Calendar**: `data/johndcook_calendar_365.csv` — 365 curated facts, ready for print
- **Bot**: `@jdc_facts` posting 2x daily via GitHub Actions
- **Book**: 76-page draft PDF with 44 figures in `book/latex/main.pdf`
- **CLI**: `python -m cookbook` works for core commands

### What Needs Fixing

1. Legacy scripts in `src/` should be merged into `src/cookbook/` submodules
2. Data directory is fragmented — files scattered at root instead of organized subdirectories
3. Bot code duplicated between `bot/build_facts.py` and `cookbook.bot_utils`
4. Tests are minimal (3 files) with no fixtures or integration coverage
5. CI doesn't enforce calendar immutability

---

## Phase 1: Code Consolidation

**Goal**: Eliminate the hybrid architecture by moving all logic into `src/cookbook/` submodules.

### 1.1 Ingest Module Consolidation

| Current Location | Target | Action |
|-----------------|--------|--------|
| `src/fetch_wp_api.py` | `src/cookbook/ingest.py` | Extract core functions, merge |
| `src/fetch_wp_taxonomies.py` | `src/cookbook/ingest.py` | Merge taxonomy fetching |
| `src/enrich_posts_with_taxonomy.py` | `src/cookbook/ingest.py` | Merge enrichment logic |
| `src/build_post_text_index.py` | `src/cookbook/ingest.py` | Merge indexing logic |
| `src/extract_johndcook.py` | `src/cookbook/ingest.py` | Merge extraction (or archive if unused) |
| `src/extract_from_wp_sql.py` | Archive | Legacy SQL extraction — likely unused |
| `src/cookbook/ingest_utils.py` | Delete after merge | Was a thin wrapper |

**Result**: Single `src/cookbook/ingest.py` module with functions:
- `fetch_wp_api()` — Fetch posts from WordPress REST API
- `fetch_taxonomies()` — Fetch categories and tags
- `enrich_posts()` — Add taxonomy data to posts
- `build_text_index()` — Generate text analysis index

### 1.2 Calendar Module Consolidation

| Current Location | Target | Action |
|-----------------|--------|--------|
| `src/generate_calendar_candidates.py` | `src/cookbook/calendar.py` | Merge as v4 generator |
| `src/generate_calendar_candidates_v3.py` | Archive | Keep for reference only |
| `src/generate_calendar_facts.py` | Merge or archive | Check if still used |
| `src/cookbook/calendar_utils.py` | `src/cookbook/calendar.py` | Merge utilities |
| `src/cookbook/calendar_export.py` | Keep separate | Export logic is self-contained |

**Result**: `src/cookbook/calendar.py` with:
- `generate_candidates()` — Generate candidate facts from posts
- `validate_calendar()` — Check 365 against validation contracts
- `snapshot_calendar()` — Create timestamped backup
- `compute_checksum()` — SHA256 of calendar CSV

### 1.3 Bot Module Consolidation

| Current Location | Target | Action |
|-----------------|--------|--------|
| `bot/build_facts.py` | `src/cookbook/bot.py` | Merge fact building |
| `src/cookbook/bot_utils.py` | `src/cookbook/bot.py` | Consolidate posting logic |
| `bot/post_fact.py` | Keep as thin wrapper | GitHub Action entry point |

**Result**: `src/cookbook/bot.py` with:
- `build_facts()` — Generate `facts.json` from calendar + supplemental CSVs
- `select_fact()` — Pick unposted fact
- `post_fact()` — Post to X via Tweepy
- `get_status()` — Show remaining vs. posted counts

### 1.4 Delete Legacy Scripts

After consolidation and parity verification:

```bash
# Remove from src/
rm src/fetch_wp_api.py
rm src/fetch_wp_taxonomies.py
rm src/enrich_posts_with_taxonomy.py
rm src/build_post_text_index.py
rm src/generate_calendar_candidates.py
rm src/generate_calendar_candidates_v3.py
rm src/generate_calendar_facts.py
rm src/extract_johndcook.py
rm src/extract_from_wp_sql.py

# Remove wrappers
rm src/cookbook/ingest_utils.py
rm src/cookbook/calendar_utils.py
rm src/cookbook/bot_utils.py

# Remove deprecated data scripts
rm data/rebuild.py
rm data/rebuild_calendar.py
rm data/analyze_twitter.py
rm data/test.sh
```

---

## Phase 2: Data Directory Reorganization

**Goal**: Move scattered files into organized subdirectories per `refactor.md` spec.

### 2.1 Target Structure

```
data/
├── johndcook_calendar_365.csv    # PROTECTED — canonical 365 (stays at root)
├── sources/
│   ├── posts/
│   │   ├── johndcook_posts.jsonl
│   │   ├── johndcook_posts_api.jsonl
│   │   ├── johndcook_posts_enriched.jsonl
│   │   └── johndcook_posts_from_sql.jsonl
│   ├── gsc/                      # Renamed from gsc_exports/
│   │   └── (CSV exports)
│   └── taxonomies/               # Renamed from wp_taxonomies/
│       ├── categories.json
│       └── tags.json
├── index/
│   ├── johndcook_text_index.jsonl
│   └── posts_metadata.csv
├── calendar/
│   ├── candidates/
│   │   ├── johndcook_calendar_candidates_v2.csv
│   │   ├── johndcook_calendar_candidates_v3.csv
│   │   ├── johndcook_calendar_candidates_v4.csv
│   │   ├── johndcook_calendar_candidates_filtered.csv
│   │   ├── johndcook_calendar_candidates_merged.csv
│   │   └── johndcook_calendar_candidates_cleaned.csv
│   ├── final/
│   │   ├── CHECKSUM              # SHA256 of canonical 365
│   │   └── (timestamped revisions)
│   └── supplemental/
│       ├── hn_facts.csv
│       ├── new_analysis_facts.csv
│       └── additional_phd_facts.csv
├── impact/                       # Consolidated external data
│   ├── github/                   # From github_impact/
│   ├── hn/                       # From hn_impact/
│   └── scholar/                  # From scholar_impact/
└── book/                         # Chapter-ready datasets (future)
```

### 2.2 Migration Commands

```bash
# Create new directories
mkdir -p data/sources/posts data/sources/gsc data/sources/taxonomies
mkdir -p data/index
mkdir -p data/calendar/candidates data/calendar/final data/calendar/supplemental
mkdir -p data/impact/github data/impact/hn data/impact/scholar

# Move posts
mv data/johndcook_posts*.jsonl data/sources/posts/

# Move taxonomies (rename directory)
mv data/wp_taxonomies/* data/sources/taxonomies/
rmdir data/wp_taxonomies

# Move GSC exports (rename directory)
mv data/gsc_exports/* data/sources/gsc/
rmdir data/gsc_exports

# Move index files
mv data/johndcook_text_index.jsonl data/index/
mv data/posts_metadata.csv data/index/

# Move calendar candidates
mv data/johndcook_calendar_candidates_*.csv data/calendar/candidates/

# Move supplemental facts
mv data/hn_facts.csv data/calendar/supplemental/
mv data/new_analysis_facts.csv data/calendar/supplemental/
mv data/additional_phd_facts.csv data/calendar/supplemental/
mv data/new_deep_analysis_facts.csv data/calendar/supplemental/

# Move impact data
mv data/github_impact/* data/impact/github/
mv data/hn_impact/* data/impact/hn/
mv data/scholar_impact/* data/impact/scholar/
rmdir data/github_impact data/hn_impact data/scholar_impact

# Create checksum
sha256sum data/johndcook_calendar_365.csv > data/calendar/final/CHECKSUM
```

### 2.3 Update paths.py

Modify `src/cookbook/paths.py` to reflect new locations:

```python
# Current paths to update:
POSTS_ENRICHED = DATA_DIR / "sources" / "posts" / "johndcook_posts_enriched.jsonl"
TEXT_INDEX = DATA_DIR / "index" / "johndcook_text_index.jsonl"
TAXONOMIES_DIR = DATA_DIR / "sources" / "taxonomies"
CALENDAR_CANDIDATES_DIR = DATA_DIR / "calendar" / "candidates"
CALENDAR_SUPPLEMENTAL_DIR = DATA_DIR / "calendar" / "supplemental"
```

---

## Phase 3: CLI Updates

**Goal**: Update CLI to match new module structure and add missing commands.

### 3.1 Current CLI Structure (Keep)

```
cookbook
├── calendar
│   ├── validate      # Check 365 against contracts
│   ├── snapshot      # Create timestamped backup
│   ├── candidates    # Generate candidate facts
│   └── export        # Render cards to PNG
├── bot
│   ├── build         # Generate facts.json
│   ├── validate      # Check lengths/IDs
│   ├── post          # Post to X
│   └── status        # Show remaining vs. posted
└── ingest
    ├── wp-api        # Fetch posts from API
    ├── taxonomies    # Fetch categories/tags
    ├── enrich        # Add taxonomy data
    └── index         # Build text index
```

### 3.2 New Commands to Add

| Command | Description |
|---------|-------------|
| `cookbook calendar checksum` | Print SHA256 of current 365.csv |
| `cookbook calendar verify` | Compare against stored checksum, exit 1 on mismatch |
| `cookbook bot reset` | Clear posted state (requires confirmation) |
| `cookbook book timeline` | Generate posting timeline data for Chapter 1 |
| `cookbook book categories` | Generate category landscape data for Chapter 2 |
| `cookbook book figures` | Regenerate all matplotlib visualizations |

### 3.3 Update CLI Imports

After module consolidation, update `src/cookbook/cli.py`:

```python
# Before:
from cookbook.ingest_utils import fetch_wp_api, fetch_taxonomies
from cookbook.calendar_utils import generate_candidates
from cookbook.bot_utils import build_facts, post_fact

# After:
from cookbook.ingest import fetch_wp_api, fetch_taxonomies, enrich_posts, build_text_index
from cookbook.calendar import generate_candidates, validate_calendar, compute_checksum
from cookbook.bot import build_facts, select_fact, post_fact, get_status
```

---

## Phase 4: Testing Infrastructure

**Goal**: Expand test coverage with fixtures and integration tests.

### 4.1 Test Directory Structure

```
tests/
├── fixtures/
│   ├── sample_posts.jsonl        # 50 representative posts
│   ├── sample_calendar.csv       # 10 sample facts for validation tests
│   └── expected_facts.json       # Known-good bot output
├── unit/
│   ├── test_models.py            # Post/Fact dataclass tests
│   ├── test_validators.py        # Validation contract tests
│   └── test_loaders.py           # CSV/JSONL parsing tests
├── integration/
│   ├── test_calendar_build.py    # Full candidate generation
│   └── test_bot_build.py         # facts.json generation
└── test_calendar_guard.py        # Existing integrity tests (keep)
```

### 4.2 New Tests to Write

**Unit Tests**:
- `test_models.py`: Test `Fact.tweet_length`, `Fact.is_tweetable`, `Post` computed properties
- `test_validators.py`: Test each validation contract (365 rows, unique IDs, category counts)
- `test_loaders.py`: Test CSV/JSONL loading with fixtures

**Integration Tests**:
- `test_calendar_build.py`: Run candidate generation on fixture data, verify output format
- `test_bot_build.py`: Run fact building, verify JSON structure and lengths

### 4.3 Test Fixtures

Create `tests/fixtures/sample_posts.jsonl` with 50 representative posts covering:
- Different years (2008, 2014, 2020, 2024)
- Different categories (Math, Programming, Statistics)
- Different lengths (short tweets vs. long essays)
- Posts with and without code blocks

---

## Phase 5: CI/CD Hardening

**Goal**: Enforce calendar immutability and expand validation.

### 5.1 Calendar Protection (Add to .github/workflows/ci.yml)

```yaml
- name: Block unauthorized calendar changes
  if: ${{ !contains(github.event.head_commit.message, '[calendar-update]') }}
  run: |
    if git diff --name-only origin/main...HEAD | grep -q 'johndcook_calendar_365.csv'; then
      echo "::error::Calendar file changed without [calendar-update] in commit message"
      exit 1
    fi
```

### 5.2 Checksum Verification (Add job)

```yaml
- name: Verify calendar checksum
  run: |
    cookbook calendar verify
```

### 5.3 Expanded CI Matrix

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e .[dev]
      - run: ruff check src/ tests/
      - run: ruff format --check src/ tests/

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e .[dev]
      - run: pytest tests/ -v --tb=short

  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e .
      - run: cookbook calendar validate
      - run: cookbook bot validate
```

---

## Phase 6: Configuration Externalization

**Goal**: Move hard-coded values into config files.

### 6.1 Create config/ Directory

```
config/
├── terms.toml          # notable_terms, rare_words, mathematicians
├── categories.toml     # category tolerances and descriptions
└── bot.toml            # rate limits, retry settings
```

### 6.2 Example config/terms.toml

```toml
[notable_terms]
mathematicians = ["Euler", "Gauss", "Fourier", "Riemann", "Ramanujan", "Tao", "Knuth"]
constants = ["pi", "e", "phi", "gamma", "zeta"]
languages = ["Python", "Mathematica", "Perl", "R", "LaTeX"]

[rarity]
max_per_category = 60
min_stats_facts = 5
otd_range = [50, 80]

[tweet]
max_length = 280
fact_max_length = 260
```

### 6.3 Config Loader

Add to `src/cookbook/config.py`:

```python
import tomllib
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent.parent / "config"

def load_config(name: str) -> dict:
    """Load a TOML config file."""
    path = CONFIG_DIR / f"{name}.toml"
    with open(path, "rb") as f:
        return tomllib.load(f)
```

---

## Phase 7: Book Integration

**Goal**: Add CLI commands for book data generation.

### 7.1 New book Submodule

Create `src/cookbook/book.py`:

```python
def generate_timeline() -> Path:
    """Generate posting_timeline.csv for Chapter 1."""
    ...

def generate_categories() -> Path:
    """Generate category_landscape.csv for Chapter 2."""
    ...

def generate_figures() -> Path:
    """Regenerate all matplotlib visualizations."""
    ...
```

### 7.2 Preserve scripts/generate_book_figures.py

The existing figure generation script is complex and works. Rather than rewriting it:
1. Keep it in `scripts/` as the implementation
2. Add CLI wrapper that calls it
3. Document dependencies (matplotlib, etc.)

---

## Phase 8: Documentation Updates

**Goal**: Align documentation with new structure.

### 8.1 Files to Update

| File | Changes |
|------|---------|
| `README.md` | Update paths, simplify structure section |
| `CLAUDE.md` | Update project structure description |
| `docs/legacy-scripts.md` | Mark additional scripts as deprecated |
| `bot/README.md` | Update to reflect CLI integration |
| `book/README.md` | Add figure regeneration instructions |

### 8.2 New Documentation

| File | Purpose |
|------|---------|
| `docs/architecture.md` | Document module responsibilities |
| `docs/data-layout.md` | Explain data directory structure |
| `.env.example` | Template for dev setup (X API keys) |

---

## Execution Order

Execute phases in this order to minimize risk:

1. **Phase 1.1-1.3**: Consolidate modules (code changes only, no deletions yet)
2. **Phase 3**: Update CLI imports
3. **Run tests**: Verify parity with existing behavior
4. **Phase 1.4**: Delete legacy scripts (after parity confirmed)
5. **Phase 2**: Reorganize data directory
6. **Phase 4**: Add test infrastructure
7. **Phase 5**: Harden CI
8. **Phase 6**: Externalize configuration
9. **Phase 7**: Add book integration
10. **Phase 8**: Update documentation

---

## Risk Mitigations

| Risk | Mitigation |
|------|------------|
| Accidental calendar overwrite | Checksum test + CI gate + `--update-calendar` flag |
| Bot facts diverge from calendar | Single source: canonical 365 + supplemental CSVs |
| Path brittleness during migration | Central `paths.py` resolver; update once |
| Breaking GitHub Action | Keep `bot/post_fact.py` as thin wrapper |
| Losing history | Archive old scripts to `scripts/archive/` before deletion |

---

## Success Criteria

- [ ] All legacy `src/*.py` scripts removed
- [ ] All data files in organized subdirectories
- [ ] `cookbook calendar validate` passes
- [ ] `cookbook bot validate` passes
- [ ] `pytest` passes with >70% coverage
- [ ] CI blocks unauthorized calendar changes
- [ ] README accurately describes current structure
- [ ] No `from src import ...` statements remain

---

## Files to Keep As-Is

These files should NOT be modified during refactoring:

- `data/johndcook_calendar_365.csv` — Canonical, protected
- `bot/facts.json` — Generated artifact, valid
- `bot/state.json` — Runtime state, auto-updated
- `scripts/generate_calendar_facts_opus.py` — Claude API example
- `book/*.md` — Manuscript content
- `book/figures/*.svg` — Visualization sources
- `.github/workflows/post-fact.yml` — Working bot schedule

---

## Estimated Effort

| Phase | Complexity | Notes |
|-------|------------|-------|
| Phase 1 (Code) | Medium | Most impactful; unblocks everything |
| Phase 2 (Data) | Low | Mostly `mv` commands + path updates |
| Phase 3 (CLI) | Low | Import updates only |
| Phase 4 (Tests) | Medium | New test files to write |
| Phase 5 (CI) | Low | YAML additions |
| Phase 6 (Config) | Low | Optional; can defer |
| Phase 7 (Book) | Low | Optional; can defer |
| Phase 8 (Docs) | Low | Final polish |

Recommend executing Phases 1-5 together as the "core refactor", then Phases 6-8 as "polish".
