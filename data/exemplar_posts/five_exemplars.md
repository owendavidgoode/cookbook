# Five Exemplar Posts: The Translation Layer in Action

**Purpose:** Demonstrate Cook's "textbook → Cook → bridge" methodology
**Selection Criteria:** Posts with documented real-world impact (GitHub citations, HN testimonials, production use)

---

## Exemplar 1: "Don't Invert That Matrix"

**Post URL:** https://www.johndcook.com/blog/2010/01/19/dont-invert-that-matrix/
**Published:** January 19, 2010

### Evidence of Impact

- **TensorFlow docs** (6,275★) cites in advanced autodiff guide
- **QuantEcon lectures** use as teaching reference
- **HN testimonials:** Multiple users cite as correction to common misconception
- **GitHub:** 25+ repos reference in code comments, tutorials, and documentation

### The Three-Step Analysis

**Step 1: The Problem (Textbook)**
Linear algebra textbooks define solving Ax = b as x = A⁻¹b. This is mathematically correct but computationally disastrous—matrix inversion is O(n³), numerically unstable, and rarely needed.

**Step 2: The Cook Translation**
> "If you need to solve Ax = b, don't compute A⁻¹ and multiply it by b. Instead, use a factorization or solver designed for that purpose."

Cook provides concrete alternatives: LU decomposition, Cholesky factorization, and library functions. He explains *why* in 500 words.

**Step 3: The Bridge**
Cook translates a nuance that textbooks assume readers know. The gap: mathematicians write A⁻¹b as shorthand; students read it literally. Cook bridges this by naming the problem explicitly and providing the working solution.

---

## Exemplar 2: Gamma Function Approximation

**Post URL:** https://www.johndcook.com/blog/2012/09/25/gamma-function-approximation/
**Related:** https://www.johndcook.com/blog/cpp_gamma/

### Evidence of Impact

- **pandas** (47,223★) uses interpolation methods citing Cook
- **10+ language implementations** directly reference Cook's gamma approximation
- **Azure/Accord-NET**, **Microsoft/BuildXL**, **pioneer** game engine all cite
- **HN testimony:** Log-gamma used as teaching example

### The Three-Step Analysis

**Step 1: The Problem (Textbook)**
The gamma function Γ(z) is defined as an improper integral:
```
Γ(z) = ∫₀^∞ t^(z-1) e^(-t) dt
```
This definition is useless for computation. Textbooks derive properties (Γ(n+1) = n!) but rarely address implementation.

**Step 2: The Cook Translation**
Cook provides Lanczos approximation code in multiple languages, explains the numerical stability concerns, and shows how to handle edge cases. He explains *when* to use log-gamma vs gamma.

**Step 3: The Bridge**
The gap: special functions exist in libraries (scipy.special.gamma) but without understanding, users misuse them. Cook explains numerical overflow, recommends log-gamma for large values, and provides copy-pasteable implementations.

---

## Exemplar 3: Kumaraswamy Distribution

**Post URL:** https://www.johndcook.com/blog/2017/11/06/kumaraswamy-distribution/

### Evidence of Impact

- **HN Tier 1 Testimonial (abhgh):** "I was looking for ways to sample quickly from a mixture of Beta distributions when I stumbled upon his post on the Kumaraswamy distribution... The [CDF] property makes generating samples from it convenient and fast."
- Direct production code application

### The Three-Step Analysis

**Step 1: The Problem (Textbook)**
Beta distributions are essential in Bayesian statistics but expensive to sample from—no closed-form inverse CDF means using rejection sampling or numerical methods.

**Step 2: The Cook Translation**
> "The Kumaraswamy distribution is a lot like the beta distribution, but it has a simple closed-form CDF and inverse CDF."

Cook provides:
- Mathematical comparison to beta distribution
- Closed-form expressions
- Code for sampling
- Visual comparison

**Step 3: The Bridge**
The gap: practitioners need fast sampling from beta-like distributions; academics publish the Kumaraswamy result but it doesn't reach practitioners. Cook's post is literally the bridge—the HN commenter found it by searching for "sample from Beta fast."

---

## Exemplar 4: Running Statistics (Welford's Algorithm)

**Post URL:** https://www.johndcook.com/blog/standard_deviation/
**Related:** Accurately computing running variance

### Evidence of Impact

- **pandas** `groupby.pyx` cites Cook's interpolation work
- **OpenTSDB** (5,060★) Aggregators.java references
- **Multiple time-series libraries** cite

### The Three-Step Analysis

**Step 1: The Problem (Textbook)**
Computing variance naively: var = E[X²] - E[X]². This is numerically unstable—catastrophic cancellation for large datasets.

**Step 2: The Cook Translation**
Cook explains Welford's 1962 algorithm for online computation of mean and variance in a single pass, with numerical stability. He provides code and explains *why* the naive formula fails.

**Step 3: The Bridge**
The gap: Welford's paper is behind academic paywalls and written in 1962 notation. Cook's explanation is Google-able, copy-pasteable, and explains the *why* alongside the *how*.

---

## Exemplar 5: RGB to Grayscale Conversion

**Post URL:** https://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/

### Evidence of Impact

- **HN Testimonial (chmod775):** "I just googled 'RGB to grayscale' and this was the first result... I recommend reading it"
- SEO authority / canonical reference status
- Demonstrates Cook's reach beyond pure mathematics

### The Three-Step Analysis

**Step 1: The Problem (Textbook/Documentation)**
Image processing libraries provide grayscale conversion but documentation rarely explains *which* algorithm is used. Common approaches:
- Average: (R + G + B) / 3
- Luminosity: 0.21R + 0.72G + 0.07B
- Lightness: (max(R,G,B) + min(R,G,B)) / 2

**Step 2: The Cook Translation**
Cook explains:
- Why simple averaging is wrong (perceptual luminance)
- The coefficients come from human vision research
- When each method is appropriate
- Code examples

**Step 3: The Bridge**
The gap: practitioners copy formulas without understanding them. Cook explains the perceptual science behind the magic numbers. A 3-minute read saves hours of debugging "why does my grayscale look wrong?"

---

## Summary: The Pattern

All five exemplars follow the same structure:

1. **Academic source exists** but is inaccessible (paywalls, notation, assumed knowledge)
2. **Cook's post** explains the *why*, provides working code, and addresses practical concerns
3. **Evidence of impact** proves the bridge was crossed (production code, testimonials, citations)

### Common Traits

| Trait | Evidence |
|-------|----------|
| Explains the *why* not just the *how* | All five posts |
| Provides working code | All five posts |
| Addresses numerical/practical concerns | Gamma, Matrix, Running Stats |
| Makes obscure techniques discoverable | Kumaraswamy, Welford |
| First Google result for topic | RGB grayscale |

---

## Integration Notes for Manuscript

These exemplars should be integrated into **Act III, Chapter 9: The Modern Translation Layer** per brutal_editor.md.

Each exemplar demonstrates the mature Cook voice:
- Mathematical rigor (PhD credibility)
- Practical focus (industry experience)
- Clear explanation (communication ability)

The three-step analysis format can be used directly in the book chapter, with code blocks and visual comparisons where appropriate.
