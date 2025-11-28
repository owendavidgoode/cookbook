# Cookbook Workspace

Utilities for extracting content from the downloaded `johndcook.com` site into reusable datasets for books, calendars, or other compilations.

## Quick Start
- Requirement: `python3` (stdlib only; no extra packages needed).
- Run extraction from this folder:
  - `python3 src/extract_johndcook.py --source ../johndcook/app/public --output data/johndcook_posts.jsonl`
- Output: JSONL with `slug`, `canonical_url`, `title`, `heading`, `summary`, `word_count`, `blocks` (tag + text), and combined `content`.

## Notes
- Treat `../johndcook` as read-only; this folder is the workspace for generated artifacts.
- Adjust `--limit` to preview a subset while testing.
- Content includes Unicode symbols from the original posts (e.g., Greek letters) to preserve fidelity.
