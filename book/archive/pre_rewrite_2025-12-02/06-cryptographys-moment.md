# Chapter 6: Cryptography's Moment

> "Number theory has traditionally been the purest of pure mathematics. People study number theory for the joy of doing so, not to make money. At least that was largely true until the advent of public key cryptography."
> — John D. Cook, "Surprising applications of math" (2011)

---

Hardy died in 1947. Three decades later, RSA encryption turned prime numbers into the foundation of digital security. The purest mathematics became urgently practical.

The blog didn't witness this original transformation—RSA predates it by three decades—but it tracked what came next: the world's growing awareness that number theory now underpins daily life.

---

## The Spike

Look at cryptography posts by year:

| Year | Crypto Posts |
|------|--------------|
| 2009-2016 | ~1/year |
| 2017 | 5 |
| 2018 | 12 |
| **2019** | **38** |
| 2020-2024 | ~10/year |
| 2025 | 47 (through November) |

From 2009 to 2016: essentially nothing.
Then 2017: the ramp begins.
Then 2019: **thirty-eight posts**. In a single year.

[FIGURE: Line chart with annotations showing crypto and privacy posts over time, with world events marked]

[FIGURE: Dumbbell chart showing first and last appearance of cryptography topics]

---

## Why 2019?

2019 was peak "techlash." Cambridge Analytica (2018). GDPR (2018). The world woke up to the reality of data surveillance.

Into this context, a mathematician who had been writing about number theory for a decade suddenly found his expertise urgent. Elliptic curves aren't just beautiful—they secure Bitcoin. Prime factorization isn't just a puzzle—it's why your passwords work.

The blog met the moment.

One post captures the tone: "Why RSA Works" (2019). It opens: "The security of RSA rests on the assumption that factoring large integers is hard." Then, in 600 words, it walks through the proof. No hand-wringing about privacy. Just: here is why the math works. The world was panicking; the blog offered clarity.

---

## RSA: The Foundation

RSA encryption relies on the fact that multiplying primes is easy, but factoring the result is hard.

The blog explains RSA at every level:
- **Theory:** Modular exponentiation.
- **Practice:** Why *e* = 65537 is the standard exponent (it's 2^16 + 1, making it fast to compute).
- **Failure:** How implementation flaws break the security.

The RSA posts span the blog's history, but they intensify when the world pays attention.

---

## Elliptic Curves: The Modern Engine

25 posts tag "Elliptic curves."

The curve *y² = x³ + 7* secures Bitcoin. Elliptic curves offer the same security as RSA with much shorter keys—essential for mobile devices and blockchains.

The blog's coverage clusters in two periods:
- **2018-2019:** The crypto-currency boom.
- **2025:** Post-quantum concerns.

The 2018 post "Bitcoin key mechanism and elliptic curves" explains the math behind the money. It doesn't offer investment advice. It explains the group law on the curve.

---

## Privacy: The Parallel Track

Privacy posts (27 in 2019) run parallel to the crypto posts.

But while crypto is about math, privacy is about law and logic.
- **GDPR:** How to comply.
- **HIPAA:** How to de-identify data.
- **Anonymization:** Why removing names isn't enough.

This connects directly to Cook's consulting work. The "19th rule of HIPAA Safe Harbor" (2023) explains the catch-all clause that trips up compliance. This is where the mathematician meets the lawyer.

---

## Pure and Applied

The blog resolves Hardy's dichotomy. Pure mathematics *is* applied mathematics waiting for its moment.

The 2018 post on RSA exponents illustrates this merger. It discusses properties of primes (pure) to explain why your bank connection is secure (applied). The distinction collapses.

When cryptography became urgent, the blog was ready. Not because Cook predicted the future, but because he had spent a decade explaining the foundations. When the spotlight turned to number theory, the stage was already set.
