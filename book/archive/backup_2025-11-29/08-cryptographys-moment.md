# Chapter 8: Cryptography's Moment

> "Number theory was once the purest of pure mathematics—no applications, no use cases, beloved precisely because it was useless. Then it became the foundation of digital privacy."
> — Adapted from G. H. Hardy's *A Mathematician's Apology*

---

G. H. Hardy famously defended number theory on the grounds of its uselessness. In *A Mathematician's Apology* (1940), he wrote that number theory "has never been 'useful' in the sense in which that word is commonly employed." He meant this as praise: pure mathematics should be pursued for beauty, not application.

Hardy died in 1947, three decades before RSA encryption turned prime numbers into the foundation of digital security. The purest of pure mathematics became urgently practical. The blog tracked this transformation in real time.

---

## The Shape of the Spike

Look at cryptography posts by year:

| Year | Crypto Posts | Privacy Posts |
|------|--------------|---------------|
| 2009 | 1 | 1 |
| 2014 | 1 | 0 |
| 2016 | 1 | 1 |
| 2017 | 5 | 7 |
| 2018 | 12 | 19 |
| **2019** | **38** | **27** |
| 2020 | 6 | 6 |
| 2021 | 6 | 2 |
| 2022 | 3 | 3 |
| 2023 | 18 | 24 |
| 2024 | 14 | 10 |
| 2025 | 23 | 2 |

From 2009 to 2016: essentially nothing. One or two posts per year at most.

Then 2017: five cryptography posts, seven privacy posts. Something shifted.

Then 2018: twelve and nineteen. The ramp-up continues.

Then 2019: **thirty-eight cryptography posts**. In a single year. More than all previous years combined.

[FIGURE: Line chart with annotations showing crypto and privacy posts over time, with world events marked]

---

## Why 2019?

The counts alone don't explain the spike. The timing suggests context.

2019 was peak "techlash." Facebook's Cambridge Analytica scandal broke in 2018. GDPR (Europe's data protection regulation) went into effect in May 2018. High-profile security breaches filled the news. Election security concerns spiked. The question of who controls our digital lives became urgent.

Into this context, a mathematician who had been writing about number theory for a decade suddenly found his expertise relevant to the news. Elliptic curves aren't just beautiful—they secure Bitcoin. Prime factorization isn't just a puzzle—it's why your passwords work. The blog had the tools to explain.

The 2019 spike represents a mathematician responding to his moment. The mathematics was already known; the blog had touched on it before. But the world's attention turned to cryptography, and the blog turned with it.

---

## RSA: The Foundation

18 posts have "RSA" in the title, spanning 2018-2025.

RSA encryption, named for its inventors Rivest, Shamir, and Adleman (1977), works because factoring large numbers is hard. You can multiply two large primes quickly; you cannot find the factors of their product quickly (as far as anyone knows). This asymmetry powers secure communication.

The blog explains RSA at multiple levels:

**The basic mechanism** (2023): "At its core, RSA encryption is modular exponentiation." The encrypted form of message *m* is *m^e* mod *n*, where *n* is a product of two large primes.

**Implementation details** (2018): "The encryption exponents are mostly all the same." In practice, *e* = 65537 for almost everyone. Why? The post explains the tradeoffs.

**Vulnerabilities** (2019): "RSA implementation flaws." The mathematics of RSA is sound; the implementations often aren't. The blog documents what can go wrong.

**Variants** (2025): "RSA with multiple primes." What if you use three or four primes instead of two? The post explores the tradeoffs.

The RSA posts span the blog's cryptographic arc, from early mentions (2009) through the 2019 peak to recent developments (2025). The topic is inexhaustible because the applications keep evolving.

---

## Elliptic Curves: The Modern Foundation

25 posts carry the "Elliptic curves" tag. The curve *y² = x³ + 7*, over a finite field, secures Bitcoin and Ethereum.

Why elliptic curves? Because they provide the same security as RSA with much shorter keys. A 256-bit elliptic curve key offers security comparable to a 3072-bit RSA key. For mobile devices, for fast transactions, for cryptocurrency—this efficiency matters.

The blog's elliptic curve posts cluster in two periods:

- **2018-2019** (9 posts): When Bitcoin and cryptocurrency drove public interest
- **2025** (13 posts): Renewed interest, perhaps driven by post-quantum cryptography concerns

The 2018 post "Bitcoin key mechanism and elliptic curves over finite fields" explains the connection directly: Bitcoin uses the secp256k1 curve, and understanding Bitcoin requires understanding the mathematics.

---

## Bitcoin: The Specific Case

9 posts have "Bitcoin" in the title. They span 2018-2025.

The earliest: "Bitcoin key mechanism and elliptic curves over finite fields" (2018). The most recent: "Why and how Bitcoin uses Merkle trees" (2025).

The posts don't advocate for or against cryptocurrency. They explain the mathematics:

- How public-key cryptography generates Bitcoin addresses
- Why Base58 encoding is used (to avoid visually confusing characters)
- What the "proof of work" problem actually is
- How Merkle trees enable efficient verification

This is the blog's characteristic approach: not commentary, not opinion, but technical explanation. Whatever you think about cryptocurrency's social implications, the mathematics is interesting. Here's how it works.

The cluster of Bitcoin posts in 2025 (31 posts with the "Cryptocurrency" tag that year alone) suggests renewed engagement—perhaps spurred by Bitcoin's price movements, perhaps by the emergence of new cryptographic concerns.

---

## Privacy: The Parallel Track

Privacy posts run parallel to cryptography posts, with the same 2019 peak (27 posts).

The topics overlap but aren't identical. Cryptography is about the mathematics of secure communication. Privacy is about the social and legal frameworks around data. Posts tagged "Privacy" might discuss:

- GDPR compliance
- Phone number hashing
- Anonymization techniques
- Safe harbor regulations

The 2019 spike in both tags suggests a unified concern: as the world worried about data protection, the blog provided both the mathematical foundations (cryptography) and the practical implications (privacy).

---

## HIPAA: Where Theory Meets Practice

The privacy posts aren't academic exercises. They connect directly to Cook's consulting work through Kingwood Data Privacy, where HIPAA de-identification is a core service.

HIPAA—the Health Insurance Portability and Accountability Act—governs how healthcare data can be used and shared. Its Safe Harbor provision lists 18 categories of identifiers that must be removed or transformed before data qualifies as "de-identified." Cook has written about the nuances:

**"The 19th rule of HIPAA Safe Harbor"** (2023): Safe Harbor has 18 explicit rules, but there's an implicit 19th—you must also have no actual knowledge that the remaining information could identify someone.

**"Why are dates of service prohibited under HIPAA's Safe Harbor provision?"** (2019): Dates seem innocuous, but combined with other information, they can re-identify patients. The post explains the statistical reasoning behind the rule.

**"Why HIPAA matters even if you're not a 'covered entity'"** (2020): HIPAA technically only binds healthcare providers and their business associates. But the post argues that its principles matter more broadly—anyone handling sensitive data faces similar concerns.

**"Covered entities: TMPRA extends HIPAA"** (2019): Texas law extends HIPAA-like protections beyond federal requirements. State variations add complexity to compliance.

The blog's HIPAA posts, appearing mostly 2016-2025, represent mathematical privacy concepts made operational. The same person writing about elliptic curves and number theory is also navigating the specific requirements of healthcare data regulation.

This is consulting work made visible. The theoretical posts explain *why* certain techniques protect privacy. The HIPAA posts explain *how* to satisfy specific regulatory requirements. The two threads converge in practice: understanding the mathematics of re-identification risk informs the practical work of compliant de-identification.

---

## The Evolution

The cryptographic arc reveals a transformation:

**Before 2017:** Number theory for its own sake. Primes are interesting. Modular arithmetic is elegant. The occasional mention of cryptographic application, but not a focus.

**2017-2019:** The world discovers that number theory matters. The blog responds with sustained attention. Thirty-eight cryptography posts in 2019—nearly one per week.

**2020-2022:** The spike subsides but doesn't disappear. Sustained engagement at a lower level.

**2023-2025:** Renewed intensity, now focused on post-quantum cryptography (what happens when quantum computers can factor large numbers?) and cryptocurrency implementation details.

The blog didn't become a cryptography blog. Math remains the dominant category throughout. But cryptography emerged as a major theme where it had barely existed before—responding to the world, using tools the blog had developed over years.

[FIGURE: Dumbbell chart showing first/last appearance of crypto topics (RSA, elliptic curves, Bitcoin, etc.)]

---

## What Changed

Hardy was wrong about number theory's uselessness, but he was right about something else: mathematicians don't know in advance what will become applicable.

In 2008, when the blog launched, cryptography was a specialized topic. By 2019, it was urgent. The transformation happened not because the mathematics changed—RSA dates to 1977, elliptic curves to the 1980s—but because the world changed. Digital communication became ubiquitous. Privacy became contested. Security became everyone's concern.

The blog tracked this shift through its posting patterns. The mathematics was ready; it had been developed decades earlier. The explanation was ready; the blog had tools for making abstract concepts accessible. What changed was the audience: suddenly, people needed to understand.

---

## Pure and Applied

The blog embodies a resolution to Hardy's dichotomy. Pure mathematics *is* beautiful. Number theory *does* have intrinsic interest. But also: pure mathematics can become devastatingly practical, sometimes overnight.

The 2018 post on RSA exponents illustrates this merger. It explains that *e* = 65537 is standard because it's 2^16 + 1, which makes computation efficient, and because it's prime, which avoids certain vulnerabilities. This is simultaneously:

- Number theory (properties of primes)
- Computer science (efficient computation)
- Security engineering (avoiding implementation flaws)
- Practical guidance (what to do in real systems)

The blog doesn't choose between pure and applied. It does both, in the same post, because the distinction collapses when number theory secures your bank account.

---

## The Mathematician's Role

When cryptography became urgent, the blog was ready.

Not because Cook predicted the techlash or planned a pivot. But because years of writing about number theory, modular arithmetic, elliptic curves, and prime factorization had built a foundation. The 2019 spike represents not new learning but new attention—taking existing expertise and directing it at newly relevant questions.

This is what sustained practice provides. When the moment comes, the preparation is already done. The blog didn't scramble to learn cryptography in 2019; it had been learning for a decade. It simply turned its accumulated knowledge toward what the moment required.

Hardy thought pure mathematics was safe from application. He was wrong about the safety. But he was right that mathematical beauty matters independent of use—and also that when use arrives, the beauty remains.

The cryptography posts are some of the blog's most practical. They're also some of its most mathematical. The categories aren't opposed; they're the same thing, viewed from different angles.
