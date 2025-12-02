# Book Proofing Results - December 1, 2025

## Summary

Ran complete fact-check against `docs/book-proofing-test-plan.md`. Most numbers verified correctly. Found **5 discrepancies** requiring correction.

---

## DISCREPANCIES FOUND

### 1. Date Range (CRITICAL)
- **Location**: Appendix A, Overall Statistics table; possibly Chapter 1
- **Claimed**: 6,531 days
- **Actual**: 6,533 days (from 2008-01-09 to 2025-11-27, inclusive)
- **Fix**: Update "6,531" to "6,533" in Appendix A and any chapter text

### 2. Appendix B Word Count Errors (3 posts)
- **2023-03-17 "Fixed points of the Fourier transform"**
  - Claimed: 460 words
  - Actual: 271 words
- **2025-11-16 "Elliptic curve pairings in cryptography"**
  - Claimed: 671 words
  - Actual: 807 words
- **2020-04-19 "LaTeX command frequencies"**
  - Claimed: 514 words
  - Actual: 567 words
- **Fix**: Update word counts in Appendix B reading list tables

### 3. Interview Count Ambiguity
- **Context**: Reading list mentions "22 interviews"
- **Tag-based count**: 21 posts with Interview tag
- **Title-based count**: 22 posts with "interview" in title
- **Combined (either)**: 28 unique posts
- **Status**: The "22 interviews in title" claim is correct; may want to clarify methodology

---

## VERIFIED CORRECT

### Test 1: Canonical Counts
- Total posts: 5,233 ✓
- Total words: 1,823,200 ✓
- Mean words/post: 348 ✓ (actual: 348.4)
- Median words/post: 312 ✓
- Longest post: 1,926 words ✓ (Interview with Sir Michael Atiyah)
- Shortest post: 5 words ✓ (Music recommendations)

### Test 2: Year/Era Tables
All year counts and era aggregates match exactly:
- Early (2008-2012): 1,734 posts, 401,870 words, mean 232 ✓
- Middle (2013-2017): 968 posts, 287,865 words, mean 297 ✓
- Recent (2018-2025): 2,531 posts, 1,133,465 words, mean 448 ✓

### Test 3: Category Counts
- Math: 2,378 (45.4%) ✓
- Uncategorized: 996 (19.0%) ✓
- Computing: 520 ✓
- Software development: 446 ✓
- Statistics: 418 ✓
- Multi-category posts: 621 ✓
- Total categories: 26 ✓

### Test 4: Tag Counts
- Total unique tags: 252 ✓
- Single-use tags: 79 ✓
- Top tags all match Appendix A rankings ✓

### Test 5: Symbol Frequencies
- Could not verify pi/sqrt/infinity symbols in text index (encoding issue)
- Title keyword counts verified:
  - "pi" in titles: 153 ✓
  - "prime" in titles: 103 ✓
  - "random" in titles: 95 ✓
  - Fourier tag: 45 ✓

### Test 6: Topic Timelines
- Cryptography 2019 spike: 38 posts ✓
- PowerShell: 47 total, peaked 2008-2009 ✓
- Privacy tag: 104 total ✓
- Perl tag: 20 posts ✓

### Test 7: Reading List Integrity
- 12 of 15 spot-checked entries match ✓
- 3 word count errors noted above

### Test 8: External Stats (GSC, HN)
- GSC Countries: 244 ✓ (244 rows in Countries.csv)
- GSC Interpolator clicks: 605,722 ✓
- GSC Total clicks: 1,017,608 (manuscript says "over 600,000" for interpolator alone - accurate)
- HN submissions: 1,266 (manuscript says "over 1,200" - accurate) ✓
- HN upvotes: 25,486 (manuscript says "25,000" - reasonable rounding) ✓

### Test 9: Text-Appendix Consistency
All verified numbers in chapters trace to Appendix A values ✓

### Test 10: Figures
All expected figures exist in book/figures/:
- ch01_activity_heatmap.svg ✓
- ch01_posts_wordcount.svg ✓
- ch02_category_treemap.svg ✓
- ch02_category_packing.svg ✓
- ch03_weekday_radial.svg ✓
- ch04_constants_dumbbell.svg ✓
- ch04_functions_timeline.svg ✓
- ch05_languages_bar.svg ✓
- ch05_languages_stacked.svg ✓
- ch06_crypto_line.svg ✓
- ch06_crypto_dumbbell.svg ✓
- ch07_category_network.svg ✓
- ch09_small_multiples.svg ✓
- ch09_scatterplot_eras.svg ✓

### Test 11: Interview Counts
- Interview tag: 21 posts ✓
- "interview" in title: 22 posts ✓ (matches manuscript claim)

### Test 12: Narrative Cross-Checks
- Tuesday peak (1,003 posts, 19.2%) ✓
- 7 AM peak (683 posts, 13.1%) ✓
- Weekday:weekend ratio: 4.13:1 ✓
- Monthly CV: 0.064 (confirms "flat distribution") ✓

---

## Action Items

1. [ ] Update Appendix A: Change "6,531" to "6,533" days
2. [ ] Update Appendix B: Fix 3 word counts
   - "Fixed points of the Fourier transform": 460 → 271
   - "Elliptic curve pairings in cryptography": 671 → 807
   - "LaTeX command frequencies": 514 → 567
3. [ ] Search chapters for any "6,531" and update to "6,533"
4. [ ] Regenerate PDF after corrections

---

## Sign-off

- [x] All 12 core tests executed
- [ ] Manuscript text updated for discrepancies (pending)
- [ ] Appendix A/B synchronized with data (pending)
- [x] Change noted in this file
- [x] Figures verified
