# Book Proofing & Fact-Check Test Plan

Purpose: Give future agents a repeatable checklist to validate the manuscript before print. Run every item; log pass/fail with evidence (file, command, snippet).

## Sources and Tools
- Data: `data/posts_metadata.csv`, `data/johndcook_text_index.jsonl`, `data/new_analysis_facts.csv`, `data/gsc_exports/.../Pages.csv`, `data/hn_facts.csv`.
- Manuscript: `book/*.md`, `book/appendix-*.md`, `book/99-epilogue.md`, `book/README.md`.
- Tools: `python3`, `rg`, `csv` module, `pandas` optional. Keep commands ASCII and deterministic.

## Core Tests (run all)
1) **Canonical counts**  
   - Recompute posts, date range, mean/median word counts, longest/shortest posts from `posts_metadata.csv`; verify Appendix A table and any numeric claims in chapters 0–10.
   - Verify day-of-week and hour-of-day tables match recomputation.
   - Recompute longest gaps (inclusive days between first/last timestamps) and confirm Chapter 1 text.
2) **Year/era tables**  
   - Recompute per-year posts/words/mean/median; confirm Appendix A and Chapter 1 values.  
   - Recompute era aggregates (early/middle/recent) and ensure Chapter 1/App A match.
3) **Category counts**  
   - Count category membership in `posts_metadata.csv`; confirm Chapter 2 tables and Appendix A categories.  
   - Verify multi-category combinations (top 5) and the 621 multi-category posts claim.
4) **Tag counts & tails**  
   - Recompute tag frequency; confirm Appendix A Top 100 ordering and single-use tag count (79).  
   - Verify Chapter 10 single-use examples exist in the single-count set.
5) **Symbol frequencies**  
   - Scan `johndcook_text_index.jsonl` for posts containing π, √, ∞, α, β, λ, ε, ζ; confirm Chapter 4 numbers.  
   - Confirm title-based counts (e.g., 153 titles with “pi”, 103 with “prime”, 95 with “random”) match `posts_metadata.csv`.
6) **Topic timelines**  
   - Crypto/privacy: count posts tagged `Cryptography`/`Cryptocurrency` and `Privacy` by year; verify Chapter 6 tables and privacy mentions.  
   - PowerShell/Perl timelines: confirm post counts and last-occurrence years in Chapter 5.  
   - Fourier analysis tag count (≈45) and Math tag counts align with Chapter 4.
7) **Reading list integrity**  
   - Cross-check every Appendix B row (date + title) against `posts_metadata.csv` titles; fix any mismatches.  
   - Spot-check word counts in “Longest posts” and ensure listed word counts match metadata.
8) **Prologue/Epilogue external stats**  
   - Verify GSC claims: interpolation clicks and total clicks from `data/gsc_exports/.../Pages.csv`; ensure wording matches the latest export window.  
   - Verify Scholar/HN stats vs `data/hn_facts.csv` and `data/new_analysis_facts.csv` (if present) or the latest authoritative source.  
   - Confirm “244 countries” from `gsc_exports/Countries.csv`.
9) **Consistency between text and Appendix A**  
   - Ensure every numeric claim in chapters cites a number present in Appendix A (posts, words, percentages, medians, extremes). If not in Appendix A, add a note or adjust claim.
10) **Figures and references**  
   - Ensure every referenced [FIGURE] has a corresponding asset in `book/figures/` and filenames match `generate_book_figures.py` outputs.  
   - Regenerate figures if data changed; spot-check one figure per chapter for label correctness.
11) **Interviews**  
   - Count interviews (title contains “interview” or tag `Interview`); verify Chapter 8 language about clustering years and totals.
12) **Narrative cross-checks**  
   - Verify “morning/Tuesdays” claims against hour/day tables.  
   - Verify “weekday:weekend ratio” and “flat monthly distribution” language with recomputed ratios/CVs.

## Execution Notes
- Keep a scratch log with command outputs or summary numbers.
- If any number changes, update both the chapter text and Appendix A (and any derived chapter) together.
- After edits, rerun key recalcs for impacted areas to ensure no cascading inconsistencies.

## Sign-off Checklist
- [ ] All core tests above marked pass with evidence.
- [ ] Manuscript text updated for any discrepancies.
- [ ] Appendix A/B synchronized with data.
- [ ] Change noted in `ai_docs/archive/change-notes.md`.
- [ ] Figures verified or regenerated.
