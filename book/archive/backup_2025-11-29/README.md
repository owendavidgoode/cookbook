# Methodical

**One Blog, Seventeen Years, 1.8 Million Words**
*A Data Portrait of John D. Cook's Blog*

---

## Manuscript Files

| File | Content |
|------|---------|
| `00-prologue.md` | Prologue: The Quiet Institution |
| `01-shape-of-seventeen-years.md` | Chapter 1: The Shape of Seventeen Years |
| `02-topography-of-interest.md` | Chapter 2: The Topography of Interest |
| `03-rhythm-of-a-working-mind.md` | Chapter 3: The Rhythm of a Working Mind |
| `04-numbers-that-keep-appearing.md` | Chapter 4: The Numbers That Keep Appearing |
| `05-bestiary-of-functions.md` | Chapter 5: A Bestiary of Functions |
| `06-mathematicians-behind-theorems.md` | Chapter 6: The Mathematicians Behind the Theorems |
| `07-languages-as-thinking-tools.md` | Chapter 7: Languages as Thinking Tools |
| `08-cryptographys-moment.md` | Chapter 8: Cryptography's Moment |
| `09-edges-of-the-map.md` | Chapter 9: The Edges of the Map |
| `10-interviews.md` | Chapter 10: The Interviews |
| `11-evolution-of-a-blog.md` | Chapter 11: The Evolution of a Blog |
| `12-what-the-numbers-miss.md` | Chapter 12: What the Numbers Miss |
| `appendix-a-by-the-numbers.md` | Appendix A: By the Numbers |
| `appendix-b-reading-list.md` | Appendix B: A Reading List |
| `99-epilogue.md` | Epilogue: How This Book Was Made |

## Supporting Files

| File | Purpose |
|------|---------|
| `REVISION_ACTION_PLAN.md` | Prioritized revision checklist from editorial review |
| `figures/` | Generated visualizations (SVG + PNG) |

## Archived Materials

Reference documents and early drafts moved to `archive/`:

- `OUTLINE_V4.md` — Original detailed chapter specifications
- `PRODUCTION_SPEC.md` — Audience, style guide, print specs
- `data-notes.md` — Chapter-to-data mapping (skeleton)
- `visual_samples/` — Early visualization sampler and PDF

Editorial assessments in `editorial/`:

- `editor.md` — System prompt for editorial AI
- `claude_editor.md` — Claude's developmental edit
- `codex_editor.md` — Codex's developmental edit

## Regenerating Figures

```bash
python scripts/generate_book_figures.py           # All figures
python scripts/generate_book_figures.py --chapter 3  # Single chapter
```

Output: `book/figures/` (SVG + PNG at 300 DPI)

## Data Source

All statistics from `data/posts_metadata.csv` (5,233 posts through Nov 27, 2025).
