# You Can Just Do Things

*A Data Portrait of John D. Cook's Blog*

---

## Current Status

**First draft PDF generated:** `latex/main.pdf` (76 pages, 2025-12-01)

**Next steps:** See `REVISION_PUNCH_LIST.md` for canonical task list.

---

## Manuscript Files

| File | Content |
|------|---------|
| `00-prologue.md` | Prologue: You Can Just Do Things |
| `01-the-shape-of-the-start.md` | Chapter 1: The Shape of the Start (ACT I) |
| `02-the-consultants-toolkit.md` | Chapter 2: The Consultant's Toolkit |
| `03-finding-the-rhythm.md` | Chapter 3: Finding the Rhythm |
| `04-the-quiet-year.md` | Chapter 4: The Quiet Year (ACT II) |
| `05-the-deepening.md` | Chapter 5: The Deepening |
| `06-the-shedding.md` | Chapter 6: The Shedding |
| `07-the-mathematical-core.md` | Chapter 7: The Mathematical Core (ACT III) |
| `08-adaptation-and-urgency.md` | Chapter 8: Adaptation and Urgency |
| `09-the-modern-translation-layer.md` | Chapter 9: The Translation Layer |
| `10-the-shape-of-persistence.md` | Chapter 10: The Shape of Persistence |
| `11-the-dark-matter.md` | Chapter 11: The Dark Matter |
| `appendix-a-by-the-numbers.md` | Appendix A: By the Numbers |
| `appendix-b-reading-list.md` | Appendix B: A Reading List |
| `99-epilogue.md` | Epilogue: How This Book Was Made |

## Project Management

| File | Purpose |
|------|---------|
| `REVISION_PUNCH_LIST.md` | **Canonical task list** — all remaining work |
| `REVISION_ACTION_PLAN.md` | Original revision checklist (historical) |

## LaTeX Output

| File | Purpose |
|------|---------|
| `latex/main.tex` | Master LaTeX document |
| `latex/chapters/` | Converted chapter files |
| `latex/main.pdf` | Current PDF output |
| `latex/convert_chapters.py` | Markdown → LaTeX converter |

## Figures

| Location | Contents |
|----------|----------|
| `figures/*.svg` | Vector figures (14 total) |
| `figures/*.png` | Raster figures at 300 DPI |
| `figures/figures_preview.pdf` | All figures in one PDF for QA |

## Editorial Materials

Located in `editorial/`:

| File | Purpose |
|------|---------|
| `editor.md` | System prompt for editorial AI |
| `claude_editor.md` | Claude's developmental edit |
| `codex_editor.md` | Codex's developmental edit |
| `grok_editor.md` | Grok's developmental edit |
| `gemini_editor.md` | Gemini's developmental edit |
| `editor_pass_1.md` | Pass 1: Structural surgery |
| `editor_pass_2.md` | Pass 2: Integration and polish |

## Archived Materials

Located in `archive/`:

- `backup_2025-11-29/` — Pre-revision manuscript backup
- `OUTLINE_V4.md` — Original detailed chapter specifications
- `PRODUCTION_SPEC.md` — Audience, style guide, print specs

---

## Build Commands

### Regenerate Figures

```bash
python scripts/generate_book_figures.py           # All figures
python scripts/generate_book_figures.py --chapter 3  # Single chapter
```

### Build PDF

```bash
cd book/latex
pdflatex main.tex && pdflatex main.tex  # Run twice for ToC
```

### Convert Chapters (if markdown changed)

```bash
python book/latex/convert_chapters.py
```

---

## Data Source

All statistics from `data/posts_metadata.csv` (5,233 posts through Nov 27, 2025).
