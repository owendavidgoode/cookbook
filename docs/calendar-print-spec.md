# Print Export Spec for the 365 Facts

Goal: hand the curated 365 facts to a print vendor as a finished, intentional design—one card per day. Use this spec to build the exporter/PDF; keep the canonical CSV intact.

## Physical Format
- Size: 4.25" x 6.25" (includes 0.125" bleed on all sides for a 4" x 6" trim). If the vendor differs, adjust artboard + bleed but keep proportions.
- Resolution: 300 DPI minimum.
- Color: sRGB, but favor high contrast; avoid light text on light backgrounds.
- Output: single PDF with 365 pages (one per day), or per-page PNG/JPG if the vendor demands images. PDF is preferred.

## Layout
- Safe area: keep text within a 3.5" x 5.5" rectangle centered on the page to avoid trim risk.
- Fact block: primary content, top/mid-aligned; max 5–6 lines; avoid widows/orphans. Centered or left-aligned consistently across all pages.
- Date: bold footer, pinned to bottom (e.g., bottom-right) with generous margin; format `MM/DD/YYYY`.
- Category badge: small, optional, near the top (or top-left) using a consistent palette; keep it subtle so it doesn’t fight the fact.
- Optional secondary text: slug or title if available; small, muted (optional per fact).
- No external links on the card.

## Typography
- Use embedded, open fonts. Example stack:
  - Fact: Source Serif 4 (or Source Sans 3) Regular/Bold, 18–24 pt (adjust to fit).
  - Date: Source Sans 3 Bold, 48–60 pt depending on layout.
  - Badge/labels: Source Sans 3 Bold, 18–24 pt.
- Line length: target 55–70 characters; adjust font size and leading to fit.
- Leading: 1.2–1.3x font size; ensure clean wrap.
- Contrast: dark text on light or light text on dark, but be consistent across the set.

## Styling & Visuals
- Keep backgrounds clean and solid; if using color, use a restrained palette. Avoid busy patterns.
- Accents by category (suggested):
  - otd: #7c3aed, quirk: #22c55e, stats: #0ea5e9, rarity: #f97316, density: #10b981, constant: #f59e0b, span: #06b6d4, code: #38bdf8, gsc: #14b8a6, hn: #ef4444, tone: #a855f7, crypto: #6366f1, mathematician: #e11d48, tools: #0ea5e9, evergreen: #22c55e, engagement: #f59e0b, meta: #94a3b8.
- Visual variety: optional mini-charts (sparklines, tiny bars) on facts that have numeric context (stats, HN, word counts). Keep them minimal and consistent height; do not overpower text. If not feasible quickly, ship text-only but balanced.

## Data Mapping
- Source: `data/johndcook_calendar_365.csv` (id, type, fact, source_link, date, slug).
- Date per card: map day index 1–365 to calendar dates (start at Jan 1 of target year), ignore the CSV `date` field unless you want to reuse it in a subtitle. Use MM/DD/YYYY display.
- Fact text: primary content.
- Category: used for badge/color only; do not show raw type names if they clutter.
- Slug/title: optional small subtitle; omit if empty.
- No URLs on card.

## Export Requirements
- Deterministic: the exporter should produce the same PDF given the same CSV.
- Overflow guard: auto-scale font down a notch for long facts; refuse to render if it still overflows the safe area (fail the build).
- Embedding: ensure fonts are embedded in the PDF; no missing glyphs.
- Naming: if exporting images, use zero-padded filenames matching day numbers (`card_001.png` …).
- Validation: script should assert 365 pages rendered; check that no page has text outside safe bounds.

## Tooling Suggestion
- Use HTML→PDF (WeasyPrint/Prince) or a Python library (ReportLab) to lay out pages with absolute positioning and embedded fonts.
- Input: the frozen 365 CSV; do not rewrite or resort facts—order is the CSV order (or by day index if specified).
- CLI target (example): `python -m cookbook.cli calendar export-pdf --year 2026 --output out/calendar.pdf`.

## Review Checklist
- All 365 pages present and ordered.
- Text fits within safe area; no clipped descenders.
- Date consistent size/placement.
- Category badge present but unobtrusive; colors consistent.
- No links; optional slug/title only when available.
- PDF opens with embedded fonts; colors look consistent on screen.
