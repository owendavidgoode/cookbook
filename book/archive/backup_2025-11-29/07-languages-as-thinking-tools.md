# Part III: The Bridge

*Where mathematics meets the machine*

---

# Chapter 7: Languages as Thinking Tools

> "I'd rather do math in a general language than do general programming in a mathematical language."
> — "New introduction to SciPy" (2013)

---

The blog's second audience isn't mathematicians—it's programmers.

The comments that generate the most engagement aren't proofs; they're code snippets. The posts that get shared most widely aren't abstract theorems; they're implementations. When someone finds the blog through a search engine at 2am, they're usually looking for code that works, not theory to contemplate.

This chapter explores why. What makes a mathematician's blog so useful to people who write software? The answer lies in the intersection: languages as thinking tools, not just implementation details.

---

## Python: The Workhorse

207 posts carry the "Python" tag. 67 have "Python" in the title. Python is the lingua franca of the blog's code examples.

The dominance isn't accidental. Python emerged in the 1990s as a "readable" language, designed to make code look almost like pseudocode. For someone explaining mathematical concepts, this is invaluable. A Python snippet explaining the gamma function can be read by anyone with basic programming literacy:

```python
from scipy.special import gamma
print(gamma(5))  # prints 24.0, which is 4!
```

The code is almost English. Import the gamma function. Print its value at 5. The mathematical content shines through without getting lost in syntax.

The Python posts span the blog's entire history (2008-2025), but the intensity varies:

| Period | Python Posts (tag) |
|--------|-------------------|
| 2008-2012 | 77 |
| 2013-2017 | 62 |
| 2018-2022 | 53 |
| 2023-2025 | 15 |

Peak intensity was 2012 (23 posts), when Python was consolidating its position as the default language for scientific computing. By the 2020s, Python is so established that it barely needs mentioning—it's assumed.

---

## The SciPy Ecosystem

80 posts carry the "SciPy" tag. SciPy (Scientific Python) is the library that gives Python its mathematical teeth—special functions, integration, optimization, linear algebra, statistics.

The blog documents the ecosystem in detail:

- "Getting started with SciPy" (2009)
- "Probability distributions in SciPy" (2009)
- "Using SciPy with IronPython" (2012)
- "SciPy integration misunderstanding" (2012)
- "Bug in SciPy's erf function" (2010)

That last title is telling. The blog doesn't just explain how to use SciPy—it documents where it breaks. A bug in the error function for complex arguments with imaginary part near 5.8. This is operational knowledge, the kind you gain only by actually using the tools.

The 2013 post "New introduction to SciPy" makes the case explicitly:

> "The Python approach has its advantages—I'd rather do math in a general language than do general programming in a mathematical language—but it takes longer to learn."

This is the thesis of the bridge: Python plus SciPy lets you do mathematics without abandoning general programming capability. You can read files, process data, call APIs, and compute integrals in the same language. The cost is learning which libraries do what; the benefit is not being trapped in a specialized environment.

[FIGURE: Stacked area chart showing language mentions over time]

---

## Mathematica: The Symbolic System

74 posts carry the "Mathematica" tag. 43 have "Mathematica" in the title.

Mathematica is different from Python. It's a commercial product, created by Stephen Wolfram, designed specifically for mathematical computation. Where Python evaluates expressions numerically by default, Mathematica manipulates them symbolically:

```mathematica
Integrate[Sin[x]^2, x]  (* returns x/2 - Sin[2x]/4 *)
```

The output is a formula, not a number. This matters when you need exact results, when you need to simplify expressions, when the computation is the mathematics itself.

The blog uses Mathematica for exploration:

- "How Mathematica Draws a Dragonfly" (2025)
- "Constellations in Mathematica" (2023)
- "DFT conventions: NumPy vs Mathematica" (2023)

The last title shows the bridge in action: comparing how Python and Mathematica handle the same operation, documenting the different conventions, helping readers who work in both environments.

Mathematica posts appear steadily across the years, without the dramatic trajectory of Python. It's a mature tool that remains useful for specific purposes.

---

## PowerShell: The Fossil

47 posts carry the "PowerShell" category. All of them are from 2008-2012.

| Year | PowerShell Posts |
|------|-----------------|
| 2008 | 29 |
| 2009 | 13 |
| 2010 | 1 |
| 2011 | 1 |
| 2012 | 3 |
| 2013-2025 | 0 |

This is extinction in the data.

PowerShell is Microsoft's shell scripting language, introduced in 2006. In 2008, when the blog launched, PowerShell was new and Cook was working in Windows environments. Twenty-nine posts in the first year—nearly one every two weeks—explored what PowerShell could do.

Then the posts stopped. Completely. From 2013 onward, not a single PowerShell post.

What happened? The blog doesn't announce "I'm done with PowerShell." There's no explanation or farewell. The topic simply fades, overwhelmed by Python's rise and perhaps by changes in Cook's working environment.

PowerShell remains a footnote in the blog's history—evidence that early interests don't always persist, that the data captures not just what lasted but also what didn't.

---

## The Supporting Cast

**Perl** (20 posts): Another language that peaked early (5 posts in 2008) and faded (0 after 2021). Perl was the "Swiss Army chainsaw" of scripting in the 1990s and 2000s. Python gradually absorbed its niche.

**C++** (37 posts): For performance-critical code. When Python is too slow, when you need to call optimized libraries, C++ appears. The posts are often about interfacing—how to call C++ from Python, how to wrap existing code.

**Haskell** (15 posts): Functional programming, category theory in code. Haskell posts tend to be more abstract, connecting programming patterns to mathematical structures.

**R** (roughly 40 posts under tags like "Rstats," plus a couple of one-off variants): surprisingly modest for a statistics blog. R is the traditional language of academic statistics, but Cook clearly prefers Python for most purposes.

---

## The Translation Layer

Why do programmers care what a mathematician thinks?

Because mathematics provides abstractions that code needs. The gamma function isn't just a mathematical curiosity—it's required for computing probabilities, normalizing distributions, working with combinatorics. A programmer who needs the gamma function can either:

1. Look up the mathematical definition in a textbook
2. Find a library that computes it
3. Read a blog post that explains what it is, why you'd need it, and how to call it in code

Option 3 serves both mathematicians (who want to implement things) and programmers (who want to understand what they're implementing). The blog sits at this intersection.

A typical post bridges both worlds:

- Here's the mathematical concept (gamma extends factorial)
- Here's when you'd need it (normalizing beta distributions)
- Here's the code (`scipy.special.gamma(n)`)
- Here's a pitfall (the function has singularities at non-positive integers)

This is translation work: mathematics to code, theory to practice, formulas to functions.

---

## Code as Verification

Many posts include code not just for implementation but for verification. "Let me check this numerically" is a recurring pattern.

From "10 best rational approximations for pi" (2018):
> Here are the 10 best rational approximations to π, found via continued fractions.

The post includes a table of fractions and their accuracy—not because readers can't compute 355/113 themselves, but because seeing the numbers builds confidence. The code runs. The approximations work. The theory is correct.

This empirical verification characterizes the blog's approach. Mathematics provides proofs; code provides evidence. Both matter.

---

## Evolution of the Toolbox

The programming languages in the blog reflect the evolution of scientific computing:

**Early era (2008-2012):** Python is rising but not yet dominant. PowerShell gets significant attention. SciPy is being explored and documented. The toolbox is unsettled.

**Middle era (2013-2017):** Python consolidates. PowerShell disappears. Mathematica maintains its niche. The ecosystem stabilizes.

**Recent era (2018-2025):** Python is assumed. Posts include Python code without commenting on the choice. The question of "which language" has been answered.

This evolution mirrors the broader field. In 2008, scientific computing was fragmented across MATLAB, Mathematica, R, and various scripting languages. By 2025, Python with NumPy/SciPy has become the default for most purposes. The blog documents this transition through its changing emphases.

[FIGURE: Bar chart showing total posts per language]

---

## The Thesis

Languages are thinking tools because they shape what's easy to express.

In Python, numerical computation is easy: loop over arrays, call library functions, plot results. In Mathematica, symbolic manipulation is easy: simplify expressions, compute exact derivatives, solve equations analytically. Each language makes certain thoughts natural and others awkward.

The blog succeeds because it chooses tools that match the content. Mathematical explanations need code that looks almost like mathematics. Numerical examples need efficient array operations. Symbolic derivations need computer algebra.

And then, crucially, the blog explains the translations. When Python and Mathematica use different conventions for the same operation, the blog documents the difference. When a SciPy function has a bug, the blog reports it. The tools are not transparent; they have quirks and limitations. Understanding the tools is part of understanding the mathematics they implement.

This is why programmers read a mathematician's blog. Not because they want proofs—they want working code. And not because they want pure code—they want to understand what the code does, mathematically. The blog provides both: mathematics you can run, and code you can trust because you understand the mathematics behind it.
