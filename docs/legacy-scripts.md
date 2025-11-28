# Legacy scripts

The following legacy scripts remain for reference but are deprecated in favor of the Typer CLI under `python -m cookbook.cli`:

- `data/rebuild.py`
- `data/rebuild_calendar.py`
- `data/REBUILD_PLAN.md`
- `data/test.sh`
- `data/analyze_twitter.py`
- `scripts/generate_calendar_facts_opus.py` (superseded by `calendar candidates --version v4`)

Prefer the CLI equivalents:
- Calendar validation/snapshots/candidates: `python -m cookbook.cli calendar ...`
- Bot build/validate/post: `python -m cookbook.cli bot ...`
- Ingest/index: `python -m cookbook.cli ingest ...`

Do not delete the legacy files until all consumers have migrated.
