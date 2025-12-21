# John D. Cook: Forensic Evidence of Impact

**Consolidated:** 2025-12-02
**Sources:** deep_dive_findings.md, social_media_impact.md, additional_findings.md, hn_impact/, github_impact/, scholar_impact/

---

## Executive Summary

This document presents verified, forensic evidence that John D. Cook's blog (johndcook.com) is not merely popular—it is **infrastructure**. Cook's explanations and code:

1. Run in production systems serving millions of users (pandas, OpenTSDB)
2. Influenced the design of Python's standard library (PEP 450)
3. Appear in official documentation for Julia, TensorFlow, and Unity
4. Have been ported to 10+ programming languages
5. Are cited by AMS, SIAM, and academic textbooks

---

# Part I: The Person

## Academic Credentials

| Credential | Detail |
|------------|--------|
| Ph.D. | Mathematics, University of Texas (1992) |
| Specialization | Non-linear partial differential equations |
| Postdoc | Vanderbilt University |
| Google Scholar Citations | 5,881 |
| Peer-Reviewed Articles | 17+ |
| Technical Reports | 25+ |

### Key Academic Publications

1. **"Dose-finding based on efficacy-toxicity trade-offs"** (2004) — *Biometrics* — foundational clinical trial methodology
2. **"A Case for Robust Bayesian priors"** (2009) — *Bayesian Analysis*
3. **"Bayesian Design of Single-Arm Phase II Clinical Trials"** (2009) — *Clinical Trials*
4. **"How to test a random number generator"** (2009) — O'Reilly *Beautiful Testing*, Chapter 10

### Career Timeline

| Period | Role |
|--------|------|
| 1992 | PhD, UT Austin |
| 1992–1995 | Postdoc, Vanderbilt |
| 1995–2000 | Software developer, project manager |
| 2000–2013 | Research Statistician, MD Anderson Cancer Center |
| 2013–present | Full-time independent consultant (Singular Value Consulting) |
| 2008–present | Blogger (5,000+ posts) |

---

## Stack Exchange Presence (10+ Profiles Verified)

All profiles link to johndcook.com/blog and share identical bio.

| Site | Reputation | Notable |
|------|------------|---------|
| Stack Overflow | 30,245 | 5.7M reach, 10 gold badges |
| Mathematics | 7,188 | Top answer: determinant intuition (274 votes) |
| MathOverflow | 5,300+ | Research-level math |
| Cross Validated | 4,118 | Famous statistical quotations (241 votes) |
| TeX/LaTeX | 3,621 | |
| Computational Science | 259 | Monte Carlo, quadrature |
| Emacs | 231 | UTF-8/octal encoding |
| Unix & Linux | 101 | |
| Theoretical CS | 101 | |
| Signal Processing (DSP) | 101 | |

**Combined SE reputation:** 52,000+
**Stack Overflow reach:** 5.7 million users
**Member since:** 2008 (17 years)

### Top Stack Overflow Answers

1. "Most efficient way to calculate LCM of two integers" — 179 votes
2. "How do Trigonometric functions work?" — 156 votes
3. "Fastest way to determine if integer's square root is an integer" — 138 votes
4. "How does C compute sin() and other math functions?" — 81 votes

---

## Twitter/X Presence

| Metric | Value |
|--------|-------|
| Total accounts | 17 |
| Total followers | 500,000+ |
| Main account (@JohnDCook) | 55,000+ |
| Active since | November 2008 |

### Specialized Accounts

| Account | Topic |
|---------|-------|
| @ProbFact | Probability |
| @DataSciFact | Data science, statistics, ML |
| @CompSciFact | Computer science |
| @AnalysisFact | Real and complex analysis |
| @AlgebraFact | Algebra and number theory |
| @TopologyFact | Topology and geometry |
| @diff_eq | Differential equations |
| @NetworkFact | Networks and graphs |
| @FunctorFact | Category theory and FP |
| @SciPyTip | Scientific Python |
| @UnixToolTip | Unix command line |
| @RegexTip | Regular expressions |
| @TeXtip | TeX/LaTeX and typography |
| @LogicPractice | Logic |
| @dsp_fact | Digital signal processing |
| @ScienceTip | Miscellaneous science |

**Recognition:** Scientix Blog (EU Science Education) lists multiple accounts among "best Twitter accounts for science geeks"

---

## Consulting Practice: Singular Value Consulting

**Founded:** 2013 (consulting since 1992)
**Name meaning:** Allusion to SVD—"getting to the core of a problem"

### Fortune 100+ Clients

| Client | Project |
|--------|---------|
| Google | Network analysis of enormous data set |
| Amazon Prime Air | Applied math problems relating to drones |
| Microsoft | Scientific computing in Python on Azure |
| Facebook | Statistical analysis and data privacy |
| AMD | Numerical algorithms for microcode |
| Amgen | Mathematical modeling |
| Merck | Statistical software development |
| Hitachi Data Systems | Cost/benefit analysis of massive storage |
| Edward Tufte | Literate programming recommendations |
| U.S. Army Corps of Engineers | Finite element error estimation |

### Expert Witness Work

- Forensic Expert Witness Association member
- Listed on LexVisio, HG Experts, JurisPro
- Cases: IP, personal injury, class action (plaintiff and defendant)
- Deposed/testified in 2+ cases in past 4 years

---

## Interviews & Press

### Legends Interviewed by Cook

| Person | Credentials | Venue |
|--------|-------------|-------|
| Sir Michael Atiyah | Fields Medal, Abel Prize | Heidelberg Laureate Forum 2013 |
| Frederick Brooks | Turing Award, *Mythical Man-Month* | Email interview 2010 |
| John Tate | Abel Prize | Heidelberg Laureate Forum |

### Press Credentials

- **Scientific American:** Guest blogger (2+ articles on HLF)
- **Heidelberg Laureate Forum:** Official blogger 2013–2014 (10+ articles)
- **SIAM News:** Feature interview (June 2022)
- **CodeProject:** Coder Interview
- **MAA Reviews:** Book reviewer (6+ reviews)

### Speaking Engagements (20+)

| Year | Event | Location | Topic |
|------|-------|----------|-------|
| 2019 | Houston Security Conference | Houston | Anonymous data identification |
| 2016 | GOTO Conference | Copenhagen | Mixing R with other languages |
| 2014 | Amazon.com | Seattle | The Infinite as a Guide to the Big |
| 2014 | KeenCon | San Francisco | Bayesian Statistics |
| 2012 | YOW! Conference | Melbourne/Brisbane | R: Good, Bad, Ugly |
| 2012 | Microsoft Research Lang.NEXT | Redmond | Why and How People Use R |

---

## Other Platforms

| Platform | Detail |
|----------|--------|
| Substack | 2,300+ subscribers |
| GitHub | johndcook, standalone code repos |
| Ham Radio | Call sign KI5TUZ (Extra class) |
| LinkedIn | Recommendations from Brian Beckman and others |

### Identity Verification Note

**Goodreads lists a DIFFERENT John D. Cook** (occupational psychologist, author of "The Experience of Work"). This is NOT the mathematician/blogger.

---

# Part II: Production Code Impact

## Tier 1: Foundational Infrastructure (10M+ users)

### pandas (47,223★)

**File:** `pandas/_libs/groupby.pyx`
```python
# Running stats update based on RunningStats::Push from
# https://www.johndcook.com/blog/skewness_kurtosis/
```
**Impact:** Every data scientist using pandas groupby statistics runs Cook's algorithm.

---

### Python Standard Library (PEP 450)

**File:** `peps/pep-0450.rst`
**Citation:** Cook's post on computing standard deviation cited as rationale for adding `statistics` module.
**Impact:** Influenced design of module used by millions of Python developers.

---

### OpenTSDB (5,060★)

**File:** `src/core/Aggregators.java`
```java
/**
 * This implementation is based upon a paper by John D. Cook,
 * which itself is based upon a method that goes back to a 1962
 * paper by B. P. Welford
 */
```
**Impact:** Every OpenTSDB installation computing variance runs Cook's algorithm.

---

## Tier 2: Official Documentation

### Julia Language (48,023★)

**File:** `doc/src/manual/integers-and-floating-point-numbers.md`

> "For a brief but lucid presentation of how floating-point numbers are represented, see John D. Cook's article..."

**Impact:** Official Julia docs recommend Cook for floating-point understanding.

---

### TensorFlow Documentation (6,275★)

**File:** `site/en/guide/advanced_autodiff.ipynb`
```markdown
Note: [Don't actually invert the matrix](https://www.johndcook.com/blog/2010/01/19/dont-invert-that-matrix/).
```
**Impact:** Official TensorFlow guide links to Cook's canonical matrix post.

---

### Unity Perception (ML Training)

**File:** `SamplerUtility.cs`
**Citations:** Cook's C# implementations of normal CDF and inverse CDF.
**Impact:** Unity's ML training randomization uses Cook's statistical functions.

---

## Tier 3: Cross-Language Implementations

Cook's gamma function has been ported to 10+ languages, all citing johndcook.com:

| Language | Repository |
|----------|------------|
| C# | ghewgill/picomath |
| Java | raharrison/MathEngine |
| JavaScript | AndreasMadsen/mathfn |
| C++ | Vaa3D/vaa3d_tools |
| PHP | MatiasNAmendola/php-nlp-tools |
| PowerShell | gravejester/Communary.ToolBox |
| Scheme | shirok/Gauche |
| TypeScript | roualdes/distributions |
| Rust | Eh2406/quadrature |
| D | p0nce/turtle |

### Picomath Project

Greg Hewgill created picomath (hewgill.com/picomath/) as a multi-language port of Cook's standalone code.
**Attribution:** "John D. Cook is the original author of most of the functions themselves."

---

## Tier 4: Specialized Systems

| System | File | Impact |
|--------|------|--------|
| Betaflight (drone controllers) | `stats.c` | Real-time flight telemetry |
| NCO (climate tools) | `nco_rth_flt.c` | NetCDF data processing |
| Pioneer (space sim) | `WinMath.h` | Physics calculations |
| BayesFactor (R package) | `logMean.R` | Bayesian inference |
| Math.NET Numerics | `CONTRIBUTORS.md` | .NET numerics library |

---

## GitHub Citation Summary

| Metric | Value |
|--------|-------|
| Repos citing johndcook.com | 160+ |
| Combined stars of citing repos | 500,000+ |
| Languages with gamma implementation | 10+ |
| PEP citations | 1 |
| Official language doc citations | 2 (Julia, TensorFlow) |

### Most-Cited Posts on GitHub (Tim Hopper's 2016 analysis)

| Mentions | Post |
|----------|------|
| 377 | Accurately computing running variance |
| 58 | Stand-alone code for numerical computing |
| 52 | A Bayesian view of Amazon Resellers |
| 47 | Main blog page |
| 44 | Distance calculation between Earth coordinates |

---

# Part III: Community Recognition

## Institutional Recognition

### American Mathematical Society (AMS)

**Blog on Math Blogs** features Cook multiple times.

> "I've been having fun reading John D Cook's Blog... I always walk away feeling like I learned something." — Anna Haensch, AMS

---

### SIAM (Society for Industrial and Applied Mathematics)

**SIAM News** published full interview: "A Conversation with Mathematical Consultant John D. Cook" (June 2022)

Key quotes:
> "Academics are often disappointed if a solution is too simple because that means it might not be publishable, but private sector clients are delighted with simple solutions."

> "Clients often need to have a conversation with someone who thinks like a mathematician—carefully defining terms, making implicit assumptions explicit, and knowing when an approximation is or is not good enough."

---

### Academic Textbook Citations

| Source | Citation |
|--------|----------|
| *Think Bayes* (Allen Downey) | Generator expression post |
| Michigan Journal of Economics | Bayesian Amazon post |

---

## R Community

Cook's work cited on R-bloggers.com:
- "Two interesting facts about high-dimensional random projections" (2019)
- "Why has R, despite quirks, been so successful?" (2015) — cites Cook's lecture

---

## Hacker News Impact

### High-Engagement Threads

| Points | Title | Comments |
|--------|-------|----------|
| 742 | Organizing complexity is the most important skill | 276 |
| 667 | Software reuse is more like an organ transplant | 228 |
| 637 | 987654321 / 123456789 | 107 |
| 575 | Rule of Three (statistical estimation) | 150 |
| 357 | Database join with CSV files | 111 |

**Total HN submissions:** 1,200+
**Front page hits (100+ points):** 50+

### Top Reddit Posts (distinct from HN)

1. Why programmers are not paid in proportion to productivity
2. Selection bias and bombers
3. Automate to save mental energy, not time
4. The most important skill in software development
5. Golden powers are nearly integers

**Key insight:** Only 3 overlap with HN top 10—distinct audiences.

---

# Part IV: Reader Testimonials

## Tier 1: Direct Production Use

### abhgh — Kumaraswamy Distribution
> "I have personally benefited from it; I was looking for ways to sample quickly from a mixture of Beta distributions when I stumbled upon his post on the Kumaraswamy distribution... makes generating samples convenient and fast."

### mavam — Project Naming
> "John D Cook's blog post actually inspired me to rename this work from cheatsheet to cookbook."

*(Influenced the Probability & Statistics Cookbook)*

### cperciva — Rule of Three
> "If all three measurements of X are smaller than all three measurements of Y, you have X < Y with 95% confidence."

*(Applied to performance testing)*

---

## Tier 2: Educational Impact

### an1sotropy — Leaky Abstractions
> "I first learned about 'leaky abstractions' from John Cook, who describes IEEE 754 floats as a leaky abstraction of the reals."

### dustingetz — FP vs OOP
> "OO makes code understandable by encapsulating moving parts. FP makes code understandable by minimizing moving parts."

### wenc — Bicycle Skills
> "I think you're referring to 'bicycle skills'—skills that you need to pre-learn so that you can call upon them when you need to."

---

## Tier 3: Professional Recommendations

### tom_b
> "I have read John Cook's blog for some time and think he might be a good fit as a consultant... I suspect it would be worth your time to get a consultant like him to come in for a week..."

### RcouF1uZ4gsC
> "If I was looking for a consultant in these matters, he would be at the top of my list."

### wenc — Business Model
> "John D Cook's business is doing well... built reputation through insightful blog posts over years, establishing credibility in the applied mathematics community."

---

## Tier 4: Quality Recognition

### xpil
> "Your blog is **one of the most valuable pieces of the Internet.**"

### dustingetz
> "best two advanced software engineering blogs ever"

### Daniel Zoran
> "This is one of my favorite blogs, there's always something interesting to learn."

### Tim Hopper
> "John's writings have shaped many aspects of my trajectory from being an operations research grad student to a practicing data scientist."

### Anna Haensch (AMS)
> "I always walk away feeling like I learned something."

### chmod775 — SEO Authority
> "I just googled 'RGB to grayscale' and this was the first result... I recommend reading it."

---

# Part V: Five Exemplar Posts

These demonstrate Cook's "textbook → Cook → bridge" methodology.

## 1. "Don't Invert That Matrix" (2010)

**Impact:** TensorFlow docs, QuantEcon lectures, 25+ GitHub repos, HN teaching canon

**The Gap:** Textbooks write x = A⁻¹b (mathematically correct but computationally disastrous). Students read it literally.

**The Bridge:** Cook names the problem explicitly, provides alternatives (LU, Cholesky), explains *why* in 500 words.

---

## 2. Gamma Function Approximation

**Impact:** pandas, 10+ language implementations, Azure/Accord-NET, Microsoft/BuildXL

**The Gap:** Γ(z) defined as improper integral—useless for computation. Textbooks don't address implementation.

**The Bridge:** Cook provides Lanczos approximation code, explains when to use log-gamma, handles edge cases.

---

## 3. Kumaraswamy Distribution (2017)

**Impact:** HN testimonial with direct production use

**The Gap:** Beta distributions expensive to sample (no closed-form inverse CDF). Kumaraswamy published but doesn't reach practitioners.

**The Bridge:** Cook explains the comparison, provides closed-form expressions and code. HN commenter found it searching "sample from Beta fast."

---

## 4. Running Statistics (Welford's Algorithm)

**Impact:** pandas `groupby.pyx`, OpenTSDB, multiple time-series libraries

**The Gap:** Naive variance formula (E[X²] - E[X]²) is numerically unstable. Welford's 1962 paper behind paywall.

**The Bridge:** Cook explains the algorithm, provides code, explains *why* naive formula fails.

---

## 5. RGB to Grayscale Conversion (2009)

**Impact:** First Google result, HN testimonial

**The Gap:** Libraries provide conversion but don't explain which algorithm or why coefficients exist.

**The Bridge:** Cook explains perceptual luminance, the vision science behind magic numbers, when each method is appropriate.

---

# Part VI: Quantified Impact Summary

| Metric | Value |
|--------|-------|
| **Blog** | |
| Blog posts | 5,000+ (as of May 2025) |
| Years blogging | 17+ (since Jan 2008) |
| Posting frequency | ~1 post every 1.2 days |
| **Social Media** | |
| Twitter accounts | 17 |
| Twitter followers (total) | 500,000+ |
| Substack subscribers | 2,300+ |
| **Stack Exchange** | |
| SE profiles (verified) | 10+ |
| Combined SE reputation | 52,000+ |
| Stack Overflow reach | 5.7 million users |
| **GitHub** | |
| Repos citing johndcook.com | 160+ |
| Combined stars of citing repos | 500,000+ |
| Languages with gamma implementation | 10+ |
| **Academic** | |
| Google Scholar citations | 5,881 |
| Peer-reviewed articles | 17+ |
| O'Reilly book chapter | 1 |
| MAA book reviews | 6+ |
| **Professional** | |
| Fortune 100 clients | 5+ |
| Speaking engagements | 20+ |
| Countries spoken in | 5+ |
| Expert witness cases | 2+ |
| Legends interviewed | 3 |
| **Recognition** | |
| Scientific American articles | 2+ |
| HLF blog articles | 10+ |
| SIAM interview | 1 |
| AMS features | 3+ |
| HN front page hits (100+ pts) | 50+ |

---

# Part VII: Key Quotes for Book

## On Practical Value
> "Private sector clients are delighted with simple solutions." — Cook, SIAM interview

## On Communication
> "If you're a genius programmer but you cannot or will not write English prose, your influence will be limited." — Cook, CodeProject

## On the Blog's Value
> "Your blog is one of the most valuable pieces of the Internet." — xpil

## On Learning
> "I always walk away feeling like I learned something." — Anna Haensch, AMS

## On Career Impact
> "John's writings have shaped many aspects of my trajectory." — Tim Hopper

## On Quality
> "Best two advanced software engineering blogs ever." — dustingetz

## On Work Ethic
> "Hardly any effort goes into overhead. It all goes into getting things done." — Cook, Bunker Spotlight

## On Statistics
> "Applied statistics may be closer to epistemology than mathematics. You have to question what you know, why you think you know it, and how confident you are in that knowledge." — Cook, SIAM interview

---

# Part VIII: The Translation Layer Thesis

## The Pattern

Cook's unique position enables a rare form of knowledge transfer:

1. **Academic credibility** — PhD, postdoc, 12+ years at MD Anderson, 5,881 citations
2. **Industry experience** — Software development, consulting since 1992, Fortune 100 clients
3. **Communication ability** — 5,000+ posts, 17 Twitter accounts, 500k+ followers

## The Evidence

| Source | Destination | Example |
|--------|-------------|---------|
| Welford (1962) paper | pandas core code | Running statistics |
| Lanczos approximation | 10+ language implementations | Gamma function |
| Numerical stability theory | Python standard library | PEP 450 |
| Academic publishing | Production systems | Kumaraswamy distribution |

## The Conclusion

johndcook.com is not merely a popular blog—it is **infrastructure**. Cook's explanations become canonical references that practitioners trust more than official documentation. His code runs in production systems worldwide.

The blog operates at the intersection academia rarely reaches: production code and practical implementation.

---

*Last updated: 2025-12-02*
