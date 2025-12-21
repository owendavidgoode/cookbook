# Chapter 7: The Mathematical Core

> "Think of the denominator of your fraction as something you have to buy. If you have enough budget to buy a three-digit denominator, then you're better off buying 355/113 rather than 314/100."
> — "10 best rational approximations for pi" (2018)

The blog that emerged from the crucible was focused. Two-thirds math. Deep posts. Interconnected references.

This chapter maps the mathematical core: the constants, functions, and obsessions that define seventeen years of thinking.

---

## The Constants

**Pi** dominates. 153 post titles mention it.

The fascination spans all seventeen years. The earliest pi post: "Computing pi with bc" (2008). The latest: a 2025 post on approximation formulas.

But Cook's pi isn't the circumference-to-diameter ratio of geometry class. His pi appears in probability (the chance of two random numbers being coprime involves pi). In statistics (the normal distribution's formula). In number theory (the distribution of primes). Pi is a bridge connecting domains that seem unrelated.

The 2018 post "10 best rational approximations for pi" exemplifies the approach:

> Think of the denominator of your fraction as something you have to buy. If you have enough budget to buy a three-digit denominator, then you're better off buying 355/113 rather than 314/100.

Mathematical intuition made tangible. The ratio 355/113 gives six correct decimal places of pi; 314/100 gives only two. Both have three-digit denominators. The "budget" metaphor makes the comparison memorable.

**Primes** follow with 103 post titles.

Primes connect the ancient to the modern. Euclid proved their infinitude around 300 BCE. In 2025, Cook writes about generating them for cryptography. The mathematical atoms have become security infrastructure.

**Randomness** appears in 95 post titles. Monte Carlo methods, random number generation, quasi-random sequences. This is applied mathematics: using chaos to solve order.

---

## The Special Functions

A special function is just a function useful enough to deserve a name. The blog returns to these named functions constantly.

**The Gamma Function** (18 posts) is "the most important function not on a calculator."

It extends the factorial to non-integers. Because factorials appear everywhere—combinatorics, probability, calculus—the gamma function appears everywhere too. Cook's explanation from "The most important function not on a calculator":

> The gamma function comes up all the time: gamma distributions, beta distributions, Bessel functions, etc. It's also important in physics. And yet it's not on a typical scientific calculator.

This observation—important but invisible—characterizes much of the blog's work. The gamma function matters, but unless you know to look for it, you won't find it.

**Bessel Functions** (12 posts) bridge physics and engineering. They describe vibrations on drums, heat in cylinders, electromagnetic waves in fibers. Cook's treatment is always concrete: here's the formula, here's Python code, here's when you'd use it.

**Fourier Transforms** (45 tagged posts) decompose signals into frequencies. The 2023 post "Fixed points of the Fourier transform" asks: which functions equal their own transform? This is the kind of question the blog loves—simple to state, revealing to explore.

[FIGURE: Timeline showing when major special functions first appeared in the blog]

---

## The Alphabet of Mathematics

The blog speaks in symbols. A frequency scan reveals the notation:

| Symbol | Posts |
|--------|-------|
| π | 404 |
| √ | 269 |
| ∞ | 136 |
| α | 108 |
| β | 83 |
| λ | 81 |
| ε | 70 |
| ζ | 38 |

This is a fingerprint. A blog about algebra would feature x and y. A blog about logic would feature ∀ and ∃. This blog features π, α, and ε—the symbols of analysis, probability, and approximation.

The symbol distribution reveals the blog's identity more precisely than any category system.

---

## The Web of Connection

The blog's power isn't in isolated explanations. It's in the connections.

A 2025 post about elliptic curves references:
- A 2019 post on Diffie-Hellman key exchange
- A 2020 post on finite fields
- A 2023 post on cryptographic pairings

A 2024 post about the gamma function references:
- The original 2009 explanation
- A 2021 post on approximations
- A 2023 post on connections to physics

These aren't random links. They're a curriculum. A reader who follows the references gets a structured education in the topic.

This is what seventeen years produces. Not just 5,233 posts, but 5,233 posts that reference each other, build on each other, form a navigable structure.

---

## The Recurring Obsessions

Some topics appear year after year:

| Topic | Years Active | Total Posts |
|-------|--------------|-------------|
| Pi | 2008-2025 | 153 |
| Primes | 2008-2025 | 103 |
| Bayesian | 2008-2025 | 100 |
| Fourier | 2008-2025 | 45 |
| Gamma | 2009-2025 | 18 |

These are the permanent fascinations. They didn't emerge from professional obligation; they persisted through career changes. They're what Cook wanted to think about, independent of what he was paid to think about.

The contrast with clinical trials (2008-2016, then extinct) is stark. Clinical trials was work. Pi is identity.

---

## The Mathematical Voice

The late-era posts share a characteristic structure:

1. **Hook**: A question or observation that seems simple
2. **Development**: The mathematical formulation
3. **Code**: Python implementation
4. **Connection**: Links to related posts

Example from "Fixed points of the Fourier transform" (2023):

> A function f is a fixed point of the Fourier transform if its transform equals itself... The Gaussian is a fixed point. So is the hyperbolic secant. So are Hermite functions...

The pattern repeats. Simple question, technical answer, code, context. This is the blog's mature voice: confident, substantive, integrated.

---

## What the Core Reveals

The mathematical core reveals what sustained seventeen years:

**Curiosity about fundamentals.** Not the latest algorithms, but the foundations: pi, primes, gamma, Fourier.

**Connection-seeking.** Not isolated topics, but relationships between topics. Why does pi appear in the prime counting function?

**Implementation focus.** Not just theory, but code. Every abstract concept gets a Python snippet.

**Teaching instinct.** Not showing off, but explaining. The posts assume an intelligent reader who needs a gap bridged.

This combination—fundamental, connected, implemented, explained—defines the blog's value. Not where you learn cutting-edge research. Where you learn to think mathematically.

---

*The mathematical core was established. The special functions mapped. The connections traced. But the blog wasn't just mathematics. There was cryptography, and it arrived with urgency.*
