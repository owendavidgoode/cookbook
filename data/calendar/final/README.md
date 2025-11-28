# Calendar Final Assets

- Canonical daily calendar: `data/johndcook_calendar_365.csv`
- Checksum file: `data/calendar/final/canonical.sha256`
- Do **not** edit the canonical CSV directly; regenerate via an explicit `--update-calendar` flow and update the checksum file in the same change.
- Validate at any time with `python -m cookbook.cli calendar validate`.
