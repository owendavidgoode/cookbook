# Legacy scripts

The following legacy scripts remain for reference but are deprecated in favor of the Typer CLI under `python -m cookbook.cli`. They were primarily used during the exploration phase of the Metastats calendar and are no longer part of the shipped 365‑day workflow:

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

The shipped Metastats calendar draws from `data/johndcook_calendar_365.csv` and `out/calendar-final/`. Use the CLI and print/cover specs under `docs/` for any future reprints or new editions. Do not delete the legacy files until all consumers have migrated.
