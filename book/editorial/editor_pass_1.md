# Editor Pass 1: Structural Revision

**Date:** November 29, 2025
**Status:** Complete
**Backup:** `archive/backup_2025-11-29/`

---

## Overview

This document summarizes the first structural editing pass on *You Can Just Do Things: How to Become Internet Famous*. The revisions were informed by two independent editorial assessments (see `claude_editor.md` and `codex_editor.md`).

---

## Major Changes

### 1. Title Update
- **Old title:** Methodical: One Blog, Seventeen Years, 1.8 Million Words
- **New title:** You Can Just Do Things: How to Become Internet Famous
- **Rationale:** The new title better captures the tertiary reader appeal—the method transfers beyond Cook specifically

### 2. Parts Structure Removed
- **Change:** Removed all Part I/II/III/IV/V headers
- **Result:** Flat chapter structure (Prologue + 10 chapters + Appendices + Epilogue)
- **Rationale:** Both editors noted Parts boundaries blurred in practice; the distinction didn't add value

### 3. Chapters 4 & 5 Merged
- **Old:** Chapter 4 (Numbers That Keep Appearing) + Chapter 5 (Bestiary of Functions)
- **New:** Chapter 4 (The Mathematical Obsessions)
- **Rationale:** The distinction between constants and functions didn't warrant separate chapters; both followed identical repetitive structure

### 4. Chapter 6 Cut
- **Old:** Chapter 6 (Mathematicians Behind the Theorems)
- **Disposition:** Cut entirely; Ramanujan material redistributed to Chapter 4
- **Rationale:** Both editors identified this as the weakest chapter—tallied mentions without answering its guiding question

### 5. Interviews Chapter Rewritten
- **Old:** Chapter 10 (The Interviews) — catalog-heavy, listed all interview subjects
- **New:** Chapter 8 (The Interviews) — focuses on 3 interviews in depth (Atiyah, Ghrist, entrepreneurs)
- **Rationale:** Editors flagged "tells what happened but not what it means"

### 6. Epilogue Trimmed
- **Change:** Cut ~25% of AI/tooling material
- **Removed:** Detailed "Reproducing This Book" instructions, stack table, excessive session details
- **Added:** Final callback to "you can just do things" theme
- **Rationale:** Codex editor specifically warned epilogue's AI material risked overshadowing Cook

---

## Chapter-Level Fixes

| Chapter | Change |
|---------|--------|
| Prologue | Added explicit tertiary reader hook ("why should you care?"); added "You Can Just Do Things" subtitle |
| Chapter 1 | Trimmed opening to reduce overlap with prologue; changed epigraph to Cook's own quote |
| Chapter 2 | Changed epigraph to stronger hook about categories as "table of contents for his mind" |
| Chapter 3 | Reordered to lead with Anti-Pattern insight; added observation about gap between perceived and actual rhythm |
| Chapter 5 | Moved thesis to opening instead of burying at end |
| Chapter 7 | Expanded Clinical Trials mystery as most biographical moment |
| Chapter 10 | Trimmed closing to protect emotional register |

---

## New Chapter Structure

| File | Title |
|------|-------|
| `00-prologue.md` | Prologue: You Can Just Do Things |
| `01-shape-of-seventeen-years.md` | Chapter 1: The Shape of Seventeen Years |
| `02-topography-of-interest.md` | Chapter 2: The Topography of Interest |
| `03-rhythm-of-a-working-mind.md` | Chapter 3: The Rhythm of a Working Mind |
| `04-mathematical-obsessions.md` | Chapter 4: The Mathematical Obsessions |
| `05-languages-as-thinking-tools.md` | Chapter 5: Languages as Thinking Tools |
| `06-cryptographys-moment.md` | Chapter 6: Cryptography's Moment |
| `07-edges-of-the-map.md` | Chapter 7: The Edges of the Map |
| `08-interviews.md` | Chapter 8: The Interviews |
| `09-evolution-of-a-blog.md` | Chapter 9: The Evolution of a Blog |
| `10-what-the-numbers-miss.md` | Chapter 10: What the Numbers Miss |
| `appendix-a-by-the-numbers.md` | Appendix A: By the Numbers |
| `appendix-b-reading-list.md` | Appendix B: A Reading List |
| `99-epilogue.md` | Epilogue: How This Book Was Made |

---

## Files Removed

- `04-numbers-that-keep-appearing.md` (merged into 04-mathematical-obsessions.md)
- `05-bestiary-of-functions.md` (merged into 04-mathematical-obsessions.md)
- `06-mathematicians-behind-theorems.md` (cut; material redistributed)
- `10-interviews.md` (replaced by new 08-interviews.md)

---

## Outstanding Items for Future Passes

1. **Figure placeholders:** All `[FIGURE: ...]` markers need actual visualizations
2. **Appendix A alignment:** Verify numbers in chapters can be traced to appendix
3. **Appendix B curation:** Consider adding "Start Here: 10 Essential Posts" section
4. **Cross-references:** Update any chapter references that now point to wrong numbers
5. **Line-level polish:** Individual sentence tightening, word choice, rhythm

---

## Validation

- [x] No chapter follows identical structure to the one before it
- [x] Each chapter has distinct opening and closing moves
- [x] Key statistics appear once with authority, not repeated
- [x] Tertiary reader has explicit reason to care by end of prologue
- [x] Epilogue ends on Cook/method, not on tools
- [x] Chapter 10's emotional register protected

---

*This pass was executed by Claude with human direction. See `editor.md` for the original editorial prompt.*
