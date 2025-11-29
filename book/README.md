# Methodical Book Project

## Overview

This folder contains the in-progress manuscript and supporting material for:

**Methodical: One Blog, Seventeen Years, 1.8 Million Words**  
*A Data Portrait of John D. Cook's Blog*

The book is a data-driven tribute to johndcook.com/blog as a long-running, quietly influential mathematical blog. Primary audience is John D. Cook; secondary audiences are his readers and data-viz / blogging enthusiasts.

The narrative voice is third person throughout (about Cook), with no direct address to the author.

## Start Here (for Agents and Collaborators)

When picking up work on the book:

1. **Read the canonical outline**
   - `book/OUTLINE_V4.md` — defines the Parts, chapters, key questions, and proposed visuals.
   - Treat this as the source of truth for structure (it supersedes `BOOK_PLAN.md`).

2. **Review the production spec**
   - `book/PRODUCTION_SPEC.md` — audience, tone, visual design, print/format decisions.
   - Pay particular attention to the style guide and page-count targets.

3. **Check data notes**
   - `book/data-notes.md` (if present) — chapter-by-chapter pointers to data tables and scripts.
   - Use this to understand which CSVs / JSONL files and scripts power each chapter’s visuals.

4. **Skim existing manuscript pages**
   - `book/00-prologue.md` — drafted prologue, sets frame and stakes.
   - `book/99-epilogue.md` — drafted epilogue about how the book was made (subject to trims).

5. **Confirm the current task**
   - The human should describe what needs doing (e.g., “Draft Chapter 4 narrative,” “Regenerate Chapter 2 visuals,” “Tighten epilogue”).
   - The agent then:
     - Re-reads the relevant sections of `OUTLINE_V4.md` and `PRODUCTION_SPEC.md`.
     - Checks `book/data-notes.md` and any chapter-specific scripts under `scripts/` or `src/`.

## Working Guidelines

- **Voice**
  - Third-person narrative about Cook (“Cook” predominantly, “John” occasionally for warmth).
  - No direct address (“you”) to the author or reader.
  - Technical but concise: one clause of context for any specialized term; keep the story moving.

- **Structure**
  - Stick to the Parts and chapter questions defined in `OUTLINE_V4.md`.
  - Use visuals to serve narrative beats, not as a catalogue of every possible chart.
  - Part V is synthetic: avoid repeating raw stats already explained in Parts I–IV.

- **Data and Scripts**
  - Treat files under `data/` as read-only inputs.
  - New analysis for the book should live in:
    - `scripts/` (one-off or chapter-specific generators), and/or
    - `src/cookbook/` modules when it’s reusable.
  - Export figures for the book under a dedicated subfolder (for example, `book/figures/part-01/`), keeping file names stable once they’re referenced in manuscript.

- **Documentation**
  - When you make a substantial change (new chapter draft, new set of visuals, major structural adjustment), record:
    - What you did
    - Which files/scripts changed
    - How to regenerate any artifacts
  - These notes can live in a dated entry in `ai_docs/archive/change-notes.md` at the repo root.

## File Map (Book-Specific)

### Reference Documents
- `book/OUTLINE_V4.md` — Canonical outline (Parts, chapters, beats, visuals).
- `book/PRODUCTION_SPEC.md` — Audience, style, print/production decisions.
- `book/README.md` — This start-here guide.
- `book/data-notes.md` — Mapping from chapters to data sources and scripts.

### Manuscript Files (All Drafted)
| File | Content | Status |
|------|---------|--------|
| `00-prologue.md` | Prologue | Drafted |
| `01-shape-of-seventeen-years.md` | Chapter 1: The Shape of Seventeen Years | Drafted |
| `02-topography-of-interest.md` | Chapter 2: The Topography of Interest | Drafted |
| `03-rhythm-of-a-working-mind.md` | Chapter 3: The Rhythm of a Working Mind | Drafted |
| `04-numbers-that-keep-appearing.md` | Chapter 4: The Numbers That Keep Appearing | Drafted |
| `05-bestiary-of-functions.md` | Chapter 5: A Bestiary of Functions | Drafted |
| `06-mathematicians-behind-theorems.md` | Chapter 6: The Mathematicians Behind the Theorems | Drafted |
| `07-languages-as-thinking-tools.md` | Chapter 7: Languages as Thinking Tools | Drafted |
| `08-cryptographys-moment.md` | Chapter 8: Cryptography's Moment | Drafted |
| `09-edges-of-the-map.md` | Chapter 9: The Edges of the Map | Drafted |
| `10-interviews.md` | Chapter 10: The Interviews | Drafted |
| `11-evolution-of-a-blog.md` | Chapter 11: The Evolution of a Blog | Drafted |
| `12-what-the-numbers-miss.md` | Chapter 12: What the Numbers Miss | Drafted |
| `appendix-a-by-the-numbers.md` | Appendix A: By the Numbers | Drafted |
| `appendix-b-reading-list.md` | Appendix B: A Reading List | Drafted |
| `99-epilogue.md` | Epilogue: How This Book Was Made | Drafted |

### Supporting Materials
- `book/visual_sampler_v2/` — Sample visualizations and PDF demonstrating design capabilities.

## Manuscript Status (November 2025)

**First draft complete.** All 12 chapters and 2 appendices drafted on November 29, 2025.

### What's Done
- All chapters drafted (~24,000 words total new prose)
- Each chapter has opening pull quote from actual blog posts
- Data tables throughout based on `posts_metadata.csv` analysis
- `[FIGURE: description]` placeholders marked for visualization pass
- Third-person voice maintained throughout

### What's Next
| Task | Owner | Notes |
|------|-------|-------|
| Foreword | Owen | Not part of agent drafting scope |
| ~~Visualization pass~~ | ~~Claude~~ | ✅ **DONE** - 19 figures in `book/figures/` |
| Editorial review | Owen | Tighten prose, verify accuracy |
| Figure polish | Editor/Designer | SVG/PNG drafts may need style refinement |
| Epilogue update | TBD | References V3 outline; update to V4 |
| Part intro bylines | Optional | Single epigraph per Part if desired |

### Generated Figures
All 19 figures generated via `scripts/generate_book_figures.py`:
- Output: `book/figures/` (SVG + PNG at 300 DPI)
- Regenerate: `python scripts/generate_book_figures.py`
- Single chapter: `python scripts/generate_book_figures.py --chapter 3`

### Data Notes
- All statistics verified against `posts_metadata.csv` (5,233 posts through Nov 27, 2025)
- Pull quotes sourced from `johndcook_text_index.jsonl`
- Some HTML entities appear in titles (e.g., `&#8217;` for apostrophe) — clean during final edit

