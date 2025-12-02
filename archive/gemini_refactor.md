# Gemini Refactor Plan

Based on the repository state and the comprehensive `refactor.md` document, here is a concrete execution plan to complete the refactoring. The goal is to consolidate the loose scripts into the `cookbook` package, enforce the data organization, and standardize on the new CLI.

### Phase 1: Code Consolidation (The "Src" Cleanup)

The `src/cookbook/` package currently wraps the old scripts rather than containing the logic. We need to move the implementation inside.

1.  **Migrate Ingestion Scripts**:
    *   Move `src/fetch_wp_api.py` → `src/cookbook/ingest_wp.py`
    *   Move `src/fetch_wp_taxonomies.py` → merge into `src/cookbook/ingest_wp.py`
    *   Move `src/enrich_posts_with_taxonomy.py` → `src/cookbook/ingest_enrich.py`
    *   Move `src/build_post_text_index.py` → `src/cookbook/ingest_index.py`
    *   *Action*: Refactor these from standalone scripts (with `if __name__ == "__main__":`) into callable modules.

2.  **Migrate Calendar Generators**:
    *   Move `src/generate_calendar_candidates.py` → `src/cookbook/calendar_gen.py`
    *   Move `src/generate_calendar_candidates_v3.py` → `src/cookbook/calendar_gen_legacy.py`
    *   *Action*: Update `src/cookbook/calendar_utils.py` to import from these new internal modules instead of `src.*`.

3.  **Update Wrappers**:
    *   Refactor `src/cookbook/ingest_utils.py` to call the new internal modules directly, removing the `from src import ...` dependency.
    *   Refactor `src/cookbook/calendar_utils.py` similarly.

4.  **Delete Legacy Scripts**:
    *   Once ported, delete the original files in `src/` to prevent confusion.

### Phase 2: Data Organization

Move data files to match the "Data Directory Layout" in `refactor.md`.

1.  **Create Directory Structure**:
    *   `data/sources/posts/`
    *   `data/sources/taxonomies/`
    *   `data/index/`
    *   `data/calendar/candidates/`
    *   `data/calendar/final/`

2.  **Move Files**:
    *   `data/johndcook_posts_*.jsonl` → `data/sources/posts/`
    *   `data/wp_taxonomies/` → `data/sources/taxonomies/`
    *   `data/johndcook_text_index.jsonl` → `data/index/`
    *   `data/johndcook_calendar_candidates_*.csv` → `data/calendar/candidates/`

3.  **Update Paths**:
    *   Update `src/cookbook/paths.py` to reflect these new locations so the CLI finds them automatically.

### Phase 3: Bot & CI Standardization

1.  **Verify Bot Parity**:
    *   Ensure `cookbook bot post` behaves exactly like `bot/post_fact.py`.
    *   *Note*: `bot/post_fact.py` is currently a thin wrapper around `cookbook.bot_utils`. It can be kept as a "shim" for GitHub Actions, or update the Action to run `python -m cookbook bot post`.

2.  **Update Makefile**:
    *   Replace `make setup`, `make test`, etc., with the commands defined in `refactor.md`.
    *   Add `make build-calendar`, `make build-bot` targets that use the new `cookbook` CLI.

3.  **Deprecate Root Scripts**:
    *   Delete `data/rebuild.py` and `data/rebuild_calendar.py` once `cookbook calendar candidates` and `cookbook calendar snapshot` are verified replacements.

### Execution Order

1.  **Run Tests**: Ensure current state is passing (`pytest` if available, or run `cookbook bot validate`).
2.  **Move & Refactor Ingest**: Handle the WP fetch/enrich scripts first.
3.  **Move & Refactor Calendar**: Handle the generator scripts next.
4.  **Move Data**: Rearrange the `data/` folder and update `paths.py`.
5.  **Cleanup**: Delete loose `src/*.py` and `data/*.py` scripts.

