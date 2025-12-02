# Part II: The Obsessions

*What does a mathematician keep coming back to?*

---

# Chapter 4: The Numbers That Keep Appearing

> "Think of the denominator of your fraction as something you have to buy. If you have enough budget to buy a three-digit denominator, then you're better off buying 355/113 rather than 314/100."
> — "10 best rational approximations for pi" (2018)

---

Some numbers earn names. Others earn attention. And a few earn both—plus decades of continuous fascination from a mathematician who could be writing about anything else.

The blog's text contains repeated encounters with certain mathematical constants and concepts. Not assigned by curriculum or demanded by clients, but chosen. Returned to. Explored again and again from different angles, across seventeen years.

These are the fixed points of a mathematical imagination.

---

## Pi

153 posts contain "pi" in the title—the most of any constant. The fascination spans the blog's entire history:

- First appearance: January 17, 2008 ("Coping with exponential growth")
- Most recent: September 25, 2025 ("Conway's pinwheel tiling")

Seventeen years of continuous engagement with the same number.

The posts approach pi from every direction. Computational: "Computing pi with bc," "Five posts on computing pi," "Algorithm for pi world records." Approximational: "10 best rational approximations for pi," "Ramanujan pi approximation," "Very accurate pi approximation." Surprising: "The coupon collector problem and π," "Finding pi in the alphabet." And annual celebrations: multiple posts on March 14, Pi Day.

[FIGURE: Timeline with annotations showing pi posts from 2008-2025]

What sustains this fascination? Pi appears everywhere. It's the ratio of circumference to diameter, but also the value of certain infinite series, the normalization constant in Gaussian distributions, the period of the tangent function, a term in Euler's identity. Every encounter is a reminder that mathematics is connected.

A 2018 post captures the practical spirit: rather than just listing decimal digits, Cook asks which *fractions* best approximate pi, and at what cost. The answer—355/113 gives six decimal places with only three-digit numbers—is both ancient (known in China by the 5th century) and immediately useful. The post treats pi not as a mystical object but as a tool to be sharpened.

---

## Primes

103 posts engage with prime numbers.

- First appearance: February 13, 2010 ("Euclid's proof that there are infinitely many primes")
- Most recent: October 7, 2025 ("RSA with multiple primes")

Primes are the atoms of arithmetic—every integer breaks down into them uniquely. They've fascinated mathematicians since antiquity and remain central to modern cryptography. The blog tracks both the ancient and the modern.

The first post gives Euclid's proof in Twitter-compatible form: "If not, multiply all primes together and add 1. Now you've got a new prime." Short, elegant, 2,300 years old. The most recent post discusses using multiple primes in RSA encryption—the same fundamental objects, now securing digital infrastructure.

Between these endpoints: "Probability that a number is prime," "Twin prime conjecture and the Pentium division bug," "Limerick primes," "Memorable primes," "American Flag Prime." The playful and the serious interleaved.

The practical thread continues through primes. The blog doesn't just ask "what are primes?" but "how do we find them?" and "what can we do with them?" Posts on primality testing, prime generation for cryptography, the distribution of primes—these connect the ancient fascination to working code.

---

## Random

95 posts explore randomness.

- First appearance: April 1, 2008 ("Randomized trials of parachute use")
- Most recent: October 22, 2025 ("Generating random points in Colorado")

The first post is a joke—a satirical take on evidence-based medicine pointing out that we don't have randomized controlled trials for parachutes. The most recent is practical: how to generate uniformly distributed points within an arbitrary geographic boundary.

Between them: random number generation, random sampling, the philosophy of randomness, the appearance of randomness in deterministic systems, Monte Carlo methods, quasi-random sequences. The blog treats randomness not as chaos but as a tool—controllable, analyzable, useful.

The posts often include code. "Generate random points inside a sphere." "Random spherical coordinates." "Random samples from a tetrahedron." These are recipes, tested and shared. Someone searching at 2am for how to sample uniformly from a non-trivial shape will find answers here, with Python implementations.

Randomness sits at the boundary between mathematics and computation. Pure mathematics proves theorems about random variables; computing needs actual random numbers. The blog lives on this boundary, equally comfortable with probability theory and with `numpy.random`.

---

## Fibonacci

22 posts—smaller than pi or primes, but persistent.

- First appearance: April 23, 2008 ("Fibonacci numbers at work")
- Most recent: October 17, 2025 ("Turning trig identities into Fibonacci identities")

Fibonacci numbers are famously accessible: add the two previous numbers to get the next. 1, 1, 2, 3, 5, 8, 13, 21... The sequence appears in nature (spiral patterns in sunflowers, breeding patterns in rabbits), art (claims about the golden ratio in architecture), and mathematics (connections to linear algebra, continued fractions, number theory).

The blog engages with all these aspects. "Honeybee genealogy" (2008) connects to biology. "Power method and Fibonacci numbers" (2015) connects to linear algebra. "Pell is to silver as Fibonacci is to gold" (2024) connects to cousin sequences. The topic is inexhaustible because it touches so many other topics.

But 22 posts over seventeen years is roughly one per year—far less intense than the focus on pi or primes. Fibonacci is a recurring visitor, not a resident. It appears when connections arise, not as its own sustained obsession.

---

## Euler's Number

10 posts explicitly about e (Euler's number, approximately 2.71828).

- First appearance: 2012 ("Euler characteristic with dice")
- Most recent: 2025 ("Computing the Euler-Mascheroni Constant")

Wait—that first post is about Euler's characteristic, not Euler's number. And the Euler-Mascheroni constant is γ (gamma), not e. The constant e is harder to search for: a single letter shared with the most common vowel in English.

But e pervades the blog even when not named in titles. It's the base of natural logarithms, the constant in exponential growth and decay, the limit of compound interest. Every post about exponential functions implicitly involves e. Every post about probability distributions touches it.

The explicit posts about e tend toward the computational: "Rational approximations to e," "The 1/e heuristic." These are practical, like the pi posts. What matters is not the mystical significance of e but how to work with it—how to approximate it, when it appears, what it tells you.

---

## The Web of Connection

These constants don't exist in isolation. The blog repeatedly demonstrates their connections:

- Pi appears in the normal distribution's probability density function (alongside e)
- Prime numbers underlie the security of random number generators
- The golden ratio (connected to Fibonacci) appears in the distribution of prime numbers
- Euler's formula links pi, e, and the imaginary unit: e^(iπ) + 1 = 0

The posts trace these connections explicitly. "Ramanujan pi approximation" (2012) presents a formula involving square roots of small integers that mysteriously produces fifteen digits of pi. Why? Because of deep connections between pi, e, and algebraic numbers that Ramanujan intuited before they were fully understood.

The 2025 post "Very accurate pi approximation" makes this explicit: π ≈ 3 log(640320) / √163. The √163 hints at Heegner numbers and the theory of complex multiplication. The blog doesn't just share the formula—it notes the hint of deeper structure.

[FIGURE: Dumbbell chart showing first/last appearance of each constant (pi, primes, random, Fibonacci, e)]

---

## What the Constants Reveal

A working mathematician returns to certain constants not because they're assigned but because they're useful. And useful in two senses: they solve problems, and they connect domains.

Pi solves problems about circles, waves, probability, and number theory. Primes solve problems about factorization, encryption, and distribution. Randomness solves problems about simulation, sampling, and inference. Each constant is a tool, sharpened over millennia, ready for application.

But they also connect. A post about random number generation might invoke prime numbers (for cryptographic security), pi (for normalization), and e (for exponential distributions). The constants are not separate topics but a web of interconnected ideas.

The blog's treatment reflects this. Posts rarely introduce a constant from scratch, as a textbook might. Instead, they encounter constants in use—solving a specific problem, appearing in a specific formula, connecting two specific domains. The reader learns pi not as "the ratio of circumference to diameter" but as "the thing that appears when you calculate the probability of a random walk returning to the origin."

---

## Evolution of Treatment

How does one write about pi differently in 2008 versus 2025?

The early posts are shorter, more declarative: here is a fact about pi, here is a link to more. The later posts are longer, more exploratory: here is a formula, here is why it works, here is the code to verify it, here are the connections to other things I've written.

This evolution mirrors the blog's overall trajectory. As Chapter 1 noted, post length doubled over the seventeen years. The constants benefit from this expansion: room to explore, to connect, to code.

But the fascination itself doesn't change. The 2008 posts and the 2025 posts both treat pi with affection and utility. The approach matures; the interest persists.

---

## The Fixed Points

What are the fixed points of a mathematical imagination?

Not arbitrary choices. Not assigned topics. Not what's trending. The constants that recur across seventeen years are the ones that proved *genuinely useful*—solving problems, connecting ideas, appearing in unexpected places.

Pi appears everywhere because circles appear everywhere, and because calculus, probability, and number theory are deeply connected. Primes appear because factorization is fundamental and cryptography is urgent. Randomness appears because simulation works and uncertainty is unavoidable.

The blog's constants are not abstract. They're working tools. And the blog returns to them because work returns to them—because the problems keep requiring the same fundamental objects.

That's what a mathematical imagination orbits: not novelty, but fundamentals. The numbers that keep appearing are the numbers that keep being useful.
