# Revision Punch List

**Status:** Active
**Created:** 2025-12-01
**Last Updated:** 2025-12-01

This is the canonical list of remaining work for the book manuscript.

---

## Priority 1: LaTeX/Technical Fixes

### 1.1 Layout Issues
- [x] Fix paragraph spacing — Increased to 1.0 baselineskip with flex ✅
- [x] Fix margins and text block proportions — Text block 7.5x4.5in, better ratios ✅
- [x] Page overflow: pg57 runs off bottom — Added raggedbottom, emergencystretch ✅
- [x] Page overflow: pg60, 62, 63, 64, 65 run off right margin — Added microtype, sloppy ✅
- [x] Fix figure/quote right-justification — Reduced widths (0.9→0.85, 0.7→0.65) ✅
- [ ] Reduce figure caption verbosity ("overtitling")

### 1.2 Code Blocks
- [x] Add syntax highlighting — Full listings config with Python/Java/R colors ✅
- [x] Improve code block styling — Reduced margins, added line break indicators ✅

### 1.3 Proofing Errors (from proofing-results-2025-12-01.md)
- [x] Appendix A: Change "6,531" to "6,533" days ✅
- [x] Appendix B word counts: ✅
  - "Fixed points of the Fourier transform": 460 → 271
  - "Elliptic curve pairings in cryptography": 671 → 807
  - "LaTeX command frequencies": 514 → 567
- [x] Search all chapters for "6,531" and update ✅

---

## Priority 2: Content Verification

### 2.1 Fake/Unverified Quotes
- [x] **Chapter 2 epigraph** — Now marked "(Editorial observation)" ✅
- [x] Audit all other chapter epigraphs for authenticity ✅

### 2.2 Factual Errors
- [x] **Chapter 8 RSA timeline** — Fixed to: "The blog didn't witness this original transformation—RSA predates it by three decades—but it explained the legacy." ✅

### 2.3 Figure Issues
- [x] **Chapter 7 typography network** — RESOLVED: Diagram is technically correct (Typography has 2 edges), but it's orphaned due to book restructure. Old Ch7 "Edges of the Map" was replaced with "The Mathematical Core" which doesn't reference this diagram. Diagram can be removed or repurposed. ✅

---

## Priority 3: Content Revision (Significant Rewriting)

### 3.1 Style Problems
- [ ] Reduce em-dash overuse (AI writing tell)
- [ ] Reduce hyperbole and dramatic phrasing
- [ ] Reduce repetitive phrasing patterns
- [ ] Expand vocabulary (overuse of certain words)
- [ ] Increase sentence structure variation (more creative writing)
- [ ] Make tone more academic/restrained

### 3.2 Missing Content
- [ ] More quotes from the blog itself throughout
- [x] More about the first post — Already reproduced in full in Chapter 1 ✅
- [x] Section on reader impact — Testimonials integrated into Ch 9 and Ch 10 ✅
- [ ] "This is not a bio" statement appears above the "this is not" section — restructure

### 3.3 Epilogue Issues
- [x] Reduce self-congratulation about Claude — Cut extended AI sections ✅
- [x] Give proper credit to Codex and Gemini editors — Equal credit given ✅
- [x] Add information about repo size and project scope — Added all stats ✅

---

## Priority 4: New Research

### 4.1 Reader Testimonials — COMPLETE
- [x] Scrape HN comments via Algolia API for reader testimonials
- [x] Curate best quotes showing reader impact
- [ ] Add "Reader Voices" section or integrate into Chapter 10

### 4.2 Additional Data
- [ ] Consider adding the first blog post in full (or substantial excerpt)

### 4.3 Five Exemplar Posts — COMPLETE
- **Location:** `data/exemplar_posts/five_exemplars.md`
- **Selected posts demonstrating textbook→Cook→bridge:**
  1. "Don't Invert That Matrix" — TensorFlow docs, 25+ repos
  2. Gamma Function Approximation — 10+ language implementations
  3. Kumaraswamy Distribution — HN testimonial with production use
  4. Running Statistics (Welford's Algorithm) — pandas, OpenTSDB
  5. RGB to Grayscale — First Google result, canonical reference
- **Integration:** Chapter 9 (The Modern Translation Layer) per brutal_editor.md

---

## Page Count Investigation

Current: 76 pages
Original estimate: ~175 pages

Reasons for discrepancy:
- Aggressive editing cuts during revision passes
- Tight LaTeX spacing (needs loosening)
- Figures currently inline (could be full-page)
- Missing content noted above

Expected after fixes: 100-120 pages (still short of 175)

Options to expand:
- Add reader testimonials section
- Reproduce select blog posts in full
- Add more figures
- Loosen spacing significantly

---

## Files to Update

| File | Changes Needed | Status |
|------|----------------|--------|
| `book/02-the-consultants-toolkit.md` | Epigraph marked as editorial | ✅ Done |
| `book/08-adaptation-and-urgency.md` | RSA timeline fixed | ✅ Done |
| `book/appendix-a-by-the-numbers.md` | Day count already correct | ✅ Done |
| `book/appendix-b-reading-list.md` | Word counts fixed | ✅ Done |
| `book/99-epilogue.md` | Balance AI editor credits, add repo info | ✅ Done |
| `book/latex/main.tex` | Fix spacing, margins, code highlighting | ✅ Done |
| `scripts/generate_book_figures.py` | Ch7 network verified (orphaned, not broken) | ✅ Done |

---

## Completed Items

- [x] Initial LaTeX setup (memoir class, 7x10, Montserrat)
- [x] Convert all chapters to LaTeX
- [x] Generate first draft PDF
- [x] Proofing test execution
- [x] Figure generation (14 figures)

---

## Decision Points — ALL RESOLVED

1. ~~**Scope of style revision** — Light touch or significant rewrite?~~ → **DECIDED: Full restructure per brutal_editor.md**
2. ~~**Reader testimonials** — Add new section or skip?~~ → **DECIDED: Yes, integrate where they strengthen (not a separate section)**
3. ~~**Page count target** — Accept shorter book or expand content?~~ → **DECIDED: Accept ~100-120 pages. No bloat.**
4. ~~**First post reproduction** — Include in full?~~ → **DECIDED: Yes, in Chapter 1.**
5. **Audience framing** → **DECIDED: Written *about* John for general audience.**

**Constraint:** Add valuable content, keep it restrained. No scope creep.

---

## Forensic Impact Data Collection

### DEEP DIVE COMPLETE — Multiple Reports

1. **`data/deep_dive_findings.md`** — Verified production code citations
2. **`data/social_media_impact.md`** — Twitter/Reddit/institutional recognition
3. **`data/additional_findings.md`** — Stack Exchange, presentations, clients, interviews, publications

### KEY NEW FINDINGS (Latest Round)
- **Interviewed legends:** Michael Atiyah (Fields Medal), Fred Brooks (Turing Award), John Tate (Abel Prize)
- **Scientific American contributor:** 2+ articles for guest blog
- **Heidelberg Laureate Forum official blogger:** 10+ articles (2013-2014)
- **O'Reilly book chapter:** "How to test a random number generator" in *Beautiful Testing* (2009)
- **Stack Overflow verified:** 30,245 rep, 5.7M reach, links to johndcook.com
- **Substack:** 2,300+ subscribers
- **LinkedIn recommendation:** Brian Beckman praised "breadth and depth of knowledge"
- **Identity verification:** Goodreads "John D. Cook" is DIFFERENT person (occupational psychologist)

### HN Comments — COMPLETE
- **Location:** `data/hn_impact/`
- **Results:** 507 comments scraped, 44 testimonials identified, 15 curated
- **High-engagement threads analyzed:** 742pts (Organizing complexity), 667pts (Lego blocks), 575pts (Rule of Three)
- **Key findings:**
  - Kumaraswamy distribution used in production (HN testimonial)
  - "Don't invert that matrix" cited to correct misconceptions in multiple threads
  - Concepts adopted: "bicycle skills," "leaky abstractions," FP vs OOP definition
  - Rule of Three used for performance testing validation

### GitHub Citations — COMPLETE (DEEP VERIFIED)
- **Location:** `data/github_impact/`
- **Results:** 160 unique repositories, **code directly inspected** for top citations
- **VERIFIED PRODUCTION CODE:**
  - **pandas** `groupby.pyx`: Running stats for skewness/kurtosis cite Cook's blog
  - **Python PEP 450**: Cook's post cited as rationale for statistics module design
  - **OpenTSDB** `Aggregators.java`: StdDev implementation "based upon paper by John D. Cook"
  - **Julia docs**: Official floating-point documentation recommends Cook's articles
  - **TensorFlow docs**: Links "Don't invert that matrix" in autodiff guide
  - **Unity Perception**: Normal CDF functions cite Cook's C# implementations
  - **Betaflight**: Drone flight controller stats.c uses Cook's running statistics
  - **Gauche Scheme**: Poisson RNG "ported from John D Cook's C++ implementation"
  - **NCO climate tools**: Cites Cook's math.h compatibility reference
  - **Pioneer space sim**: Gamma functions from Cook's standalone code
  - **BayesFactor R pkg**: Numerical stability methods cite Cook
  - **picomath**: Gamma implementation directly from Cook's standalone code
- **Cross-language implementations:** 10+ (C#, Java, JS, C++, PHP, PowerShell, Scheme, TypeScript, Rust, D)

### Google Scholar / Academic Profile — COMPLETE
- **Location:** `data/scholar_impact/`
- **Results:** Academic profile documented with publication list
- **Summary file:** `data/scholar_impact/academic_profile.md`
- **Key findings:**
  - PhD Mathematics (UT Austin 1992), Vanderbilt postdoc
  - 5,881 Google Scholar citations (primarily clinical trial methodology)
  - 16+ peer-reviewed journal articles, 25+ technical reports
  - Key paper: "Dose-finding based on efficacy-toxicity trade-offs" (Biometrics, 2004)
  - Blog represents "translation" work—making academic knowledge accessible
  - Unique position: academic credentials + industry experience + communication ability
- **Academic citations of blog:**
  - Think Bayes textbook (Allen Downey) cites generator expression post
  - Michigan Journal of Economics cites Bayesian Amazon post
  - Math.NET Numerics CONTRIBUTORS.md credits Cook's standalone code

### Social Media & Institutional — COMPLETE (NEW)
- **Location:** `data/social_media_impact.md`
- **Twitter/X findings:**
  - 17 specialized accounts (@ProbFact, @CompSciFact, etc.)
  - 500,000+ total followers across accounts
  - 55,000+ on main @JohnDCook account
  - Active since November 2008
  - Featured in Scientix Blog as "best Twitter accounts for science geeks"
- **Reddit findings:**
  - Cook's top 10 Reddit posts differ from HN top 10 (distinct audiences)
  - Tim Hopper analysis: 377 GitHub mentions for "running variance" post alone
- **Institutional recognition:**
  - **AMS (American Mathematical Society)**: Featured on Blog on Math Blogs
    - "I always walk away feeling like I learned something" — Anna Haensch
  - **SIAM**: Full interview published June 2022
    - "private sector clients are delighted with simple solutions"
  - **Carnival of Mathematics**: Featured in issue 162
- **Reader testimonials (new):**
  - "one of the most valuable pieces of the Internet" — xpil
  - "one of my favorite blogs" — Daniel Zoran
  - "best two advanced software engineering blogs ever" — dustingetz (HN)
  - "John's writings have shaped many aspects of my trajectory" — Tim Hopper

---

## Repo Stats (for Epilogue)

- Total repo size: 221 MB
- Total files: 2,711
- Data directory: 71 MB
- Book directory: 21 MB
- Scripts: 148 KB
