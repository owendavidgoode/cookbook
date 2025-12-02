# Refactor Plan (Calendar, Book, Bot) — Preserve the 365 Facts

## Non-Negotiable Guardrails
- Treat `data/johndcook_calendar_365.csv` as the canonical, ready-to-go set. Do not mutate or regenerate it by default.
- Add a read-only checksum/test that fails if the file changes without an explicit `--update-calendar` flag.
- Keep bot inputs and book datasets aligned to this file unless a deliberate rebuild is requested.

## Goals
- Consolidate the three services (calendar, bot, book) onto a shared data layer and CLI while keeping the current 365 facts intact.
- Remove ad-hoc scripts and hard-coded paths; make all pipelines reproducible via Makefile/CI.
- Add validation so future changes cannot silently alter counts, categories, or tweet lengths.

## Proposed Architecture
- Package: create a `cookbook` Python package under `src/` with clear submodules:
  - `cookbook.ingest`: fetch WP API, parse SQL dump, enrich with taxonomies.
  - `cookbook.index`: build text index and derived post metadata.
  - `cookbook.calendar`: candidate generation, scoring/filters, curation to 365, exports.
  - `cookbook.bot`: fact builder, validators, posting client.
  - `cookbook.book`: chapter-specific dataset builders and figure helpers.
- Shared models/utilities: `models.py` (Post, Fact), `paths.py` (data dir resolver/env override), `io.py` (jsonl/csv helpers).
- CLI: `python -m cookbook ...` or `cookbook` entrypoint with verbs:

| Command | Description |
|---------|-------------|
| `cookbook ingest [wp-api\|sql\|html]` | Fetch/parse posts from various sources |
| `cookbook index build` | Build text index from posts |
| `cookbook calendar build [--update]` | Generate candidates; `--update` to modify 365 |
| `cookbook calendar validate` | Check 365 against validation contracts |
| `cookbook calendar checksum` | Print SHA256 of current 365.csv |
| `cookbook calendar verify` | Compare against stored checksum, exit 1 on mismatch |
| `cookbook bot build` | Generate `bot/facts.json` from sources |
| `cookbook bot validate` | Check lengths, IDs, deduplication |
| `cookbook bot post [--dry-run]` | Post fact to X; `--dry-run` prints only |
| `cookbook bot status` | Show facts remaining vs. posted |
| `cookbook bot reset` | Clear posted state (requires confirmation) |
| `cookbook book <subcommand>` | See Book Support section |

## Validation Contracts
Concrete rules enforced by `cookbook calendar validate` and CI:

| Rule | Constraint | Rationale |
|------|------------|-----------|
| Row count | Exactly 365 | One fact per calendar day |
| Required columns | `id`, `type`, `fact`, `source_link`, `date`, `slug` | Schema consistency |
| Unique facts | No duplicate `fact` text (case-sensitive) | Avoid repeat tweets |
| Category: `otd` | 50–80 facts | Core "on-this-day" content |
| Category: `rarity` | ≤60 facts | Prevent overrepresentation |
| Category: `stats` | ≥5 facts | Ensure PhD-level depth |
| Tweet length | `len(fact) + len(source_link) + 2 ≤ 280` | Twitter character limit |
| Fact length (bot) | `len(fact) ≤ 260` | Leave room for link suffix |

## Data Directory Layout (Post-Refactor)
```
data/
├── johndcook_calendar_365.csv    # Canonical 365 (protected, stays at root)
├── calendar/
│   ├── candidates/               # Large candidate pools (v2, v3, v4, filtered)
│   ├── final/                    # Dated revisions (YYYYMMDD.csv) + CHECKSUM
│   └── supplemental/             # hn_facts.csv, new_analysis_facts.csv, etc.
├── sources/
│   ├── posts/                    # .jsonl extracts (enriched, api, sql)
│   ├── gsc/                      # Google Search Console exports
│   └── taxonomies/               # WordPress categories.json, tags.json
├── index/                        # Text index, metadata CSVs
└── book/                         # Chapter-ready datasets (future)
```

Migration: Move existing files incrementally; keep symlinks for backwards compatibility until legacy scripts are removed.

## Calendar Pipeline (Preserve Final 365)
- Stage outputs under `data/calendar/` as shown above.
- Keep the existing `data/johndcook_calendar_365.csv` in place; also copy a frozen checksum into `data/calendar/final/CHECKSUM` to track provenance.
- Consolidate the three generators (`src/generate_calendar_candidates.py`, `src/generate_calendar_candidates_v3.py`, `scripts/generate_calendar_facts_opus.py`) into a single candidate builder with configurable knobs (term lists, rarity caps, on-this-day density).
- Merge the two rebuild scripts into one curated step that:
  - Loads the frozen 365 as baseline.
  - Applies optional replacements only when `--update-calendar` is passed.
  - Emits new finals as `data/calendar/final/YYYYMMDD.csv` without overwriting the baseline.
- Validation enforces all rules from the Validation Contracts table above.

## Bot Pipeline
- Move `bot/` logic into `cookbook.bot` while keeping the GitHub Action path stable.
- Source facts from the canonical 365 plus supplemental vetted CSVs; add a `bot build` command that writes `bot/facts.json` and a `bot validate` command that checks lengths, IDs, and dedupes.
- Harden `post_fact` with retry/backoff, clearer logs, and non-destructive state handling (no silent reset; require `--reset`).
- Add dry-run mode to print the tweet instead of posting for local testing.

## Book Support
Provide `book` commands that emit chapter-ready datasets into `data/book/`:

| Command | Output | Description |
|---------|--------|-------------|
| `cookbook book timeline` | `data/book/posting_timeline.csv` | Posts per day/month/year for Chapter 1 |
| `cookbook book categories` | `data/book/category_landscape.csv` | Category counts and cross-references for Chapter 2 |
| `cookbook book terms CHAPTER` | `data/book/terms_ch{N}.csv` | Term frequencies for specific chapter |
| `cookbook book mathematicians` | `data/book/mathematician_refs.csv` | Euler, Gauss, etc. mention counts for Chapter 14 |
| `cookbook book figures` | `data/book/figures/` | Generate all matplotlib visualizations |

Reuse the shared `Post`/`Fact` loaders so manuscripts and figures always align with the same source used by calendar/bot.

## Tooling and CI

### Dependency Management
Structure `pyproject.toml` with optional extras:

```toml
[project]
name = "cookbook"
version = "0.1.0"
dependencies = ["typer>=0.9"]

[project.optional-dependencies]
bot = ["tweepy>=4.14,<5"]
dev = ["pytest>=7.0", "ruff>=0.1", "syrupy>=4.0"]
all = ["cookbook[bot,dev]"]

[project.scripts]
cookbook = "cookbook.cli:app"
```

Install options:
- `pip install -e .` — CLI only
- `pip install -e .[bot]` — With Twitter posting
- `pip install -e .[dev]` — With test/lint tools
- `pip install -e .[all]` — Everything

### Makefile Targets
```makefile
setup:
	pip install -e .[all]

lint:
	ruff check src/ bot/ tests/
	ruff format --check src/ bot/ tests/

test:
	pytest tests/ -v

calendar-validate:
	cookbook calendar validate

bot-build:
	cookbook bot build

bot-validate:
	cookbook bot validate
```

### CI Protection for Calendar File
Add to `.github/workflows/ci.yml`:

```yaml
- name: Block unauthorized calendar changes
  if: ${{ !contains(github.event.head_commit.message, '[calendar-update]') }}
  run: |
    if git diff --name-only origin/main...HEAD | grep -q 'johndcook_calendar_365.csv'; then
      echo "::error::Calendar file changed without [calendar-update] in commit message"
      exit 1
    fi
```

To update the calendar legitimately, include `[calendar-update]` in the commit message.

## Proposed Enhancements

### Configuration Management
Externalize hard-coded lists into `config/` (use TOML for consistency with `pyproject.toml`):

```
config/
├── terms.toml          # notable_terms, rare_words, mathematicians
├── categories.toml     # category tolerances and descriptions
└── bot.toml            # rate limits, retry settings
```

Example `config/terms.toml`:
```toml
[notable_terms]
mathematicians = ["Euler", "Gauss", "Fourier", "Riemann", "Ramanujan"]
constants = ["pi", "e", "phi", "gamma"]

[rarity]
max_per_category = 60
```

### Richer Data Models
The `Post` and `Fact` models in `cookbook.models` should include computed properties:

```python
@dataclass
class Fact:
    id: int
    type: str
    text: str
    source_url: str | None

    @property
    def tweet_length(self) -> int:
        """Total length including URL suffix."""
        base = len(self.text)
        if self.source_url:
            base += len(self.source_url) + 2  # "\n\n" prefix
        return base

    @property
    def is_tweetable(self) -> bool:
        return self.tweet_length <= 280

    @property
    def is_on_this_day(self) -> bool:
        return self.type == "otd"
```

### Testing Strategy
Multi-layered testing with `pytest` and `syrupy` for snapshots:

```
tests/
├── unit/
│   ├── test_models.py         # Post/Fact properties
│   ├── test_validators.py     # Validation contract checks
│   └── test_loaders.py        # CSV/JSONL parsing
├── integration/
│   ├── test_calendar_build.py # Full candidate generation
│   └── test_bot_build.py      # facts.json generation
├── snapshots/
│   └── test_parity.py         # Compare against stored outputs
└── fixtures/
    ├── sample_posts.jsonl     # 50 representative posts
    └── expected_facts.json    # Known-good bot output
```

Run with: `pytest tests/ -v --snapshot-update` (to update snapshots after intentional changes).

## Migration Steps (Low-Risk)
1) Freeze current 365: compute checksum, add validation test, and document in `data/calendar/final/README`.
2) Introduce package skeleton, shared loaders, and path resolver; leave existing scripts untouched initially.
3) Wrap bot build/post in the new CLI while keeping `facts.json` and workflow paths the same.
4) Consolidate calendar candidate generation into the new module; keep writing to the existing CSVs for comparison only.
5) Replace the old rebuild scripts with the guarded curation command; keep the baseline file unchanged unless manually opted in.
6) Add book data commands that read from the shared index; no changes to manuscripts yet.
7) Turn on CI and Makefile defaults; deprecate legacy scripts after parity is proven.

## Legacy Script Disposition
After parity is proven, handle existing scripts as follows:

| Script | Location | Action | Trigger |
|--------|----------|--------|---------|
| `rebuild.py` | `data/` | Delete | `cookbook calendar build --update` works |
| `rebuild_calendar.py` | `data/` | Delete | Same as above |
| `generate_calendar_facts.py` | `src/` | Merge into `cookbook.calendar` | After consolidation |
| `generate_calendar_candidates.py` | `src/` | Merge into `cookbook.calendar` | After consolidation |
| `generate_calendar_candidates_v3.py` | `src/` | Merge into `cookbook.calendar` | After consolidation |
| `generate_calendar_facts_opus.py` | `scripts/` | Keep as Claude API example | Never delete |
| `extract_johndcook.py` | `src/` | Merge into `cookbook.ingest` | After package setup |
| `extract_from_wp_sql.py` | `src/` | Merge into `cookbook.ingest` | After package setup |
| `build_facts.py` | `bot/` | Merge into `cookbook.bot` | After CLI wrapping |
| `post_fact.py` | `bot/` | Keep (GitHub Action entry point) | Thin wrapper only |

## Risks and Mitigations
- Risk: accidental overwrite of the 365 file. Mitigation: checksum test, `--update-calendar` gate, and versioned outputs.
- Risk: bot facts diverge. Mitigation: single builder that reads the same canonical inputs and a test that lengths and counts match expectations.
- Risk: path brittleness. Mitigation: central path resolver and removal of absolute paths before deprecating old scripts.
