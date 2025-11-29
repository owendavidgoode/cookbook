# Chapter 5: A Bestiary of Functions

> "The gamma function Γ(x) is the most important function not on a calculator. It comes up constantly in math."
> — "The gamma function" (2009)

---

A special function is just a function useful enough to deserve a name.

That's a loose definition, but it captures the pragmatic reality. Nobody legislates which functions get names. Names emerge from use: if enough mathematicians and engineers encounter the same function in enough different contexts, someone names it, and the name sticks. The named functions form a working vocabulary—tools that get reached for repeatedly.

The blog is populated by these named creatures. Some appear in titles. Others lurk in tags. All of them represent choices: when Cook writes about the gamma function instead of some other function, he's testifying that the gamma function is useful. That it solves problems. That it keeps appearing.

---

## Gamma: The Protagonist

18 posts have "gamma" in the title. The function spans the blog's entire history:

- First: 2008 (\"Random inequalities VI: gamma distributions\"), with a basic introduction in 2009 (\"The gamma function\")
- Most recent: 2025 ("Trigamma," "Dimensional analysis for gamma function values")

What makes the gamma function so important? It extends the factorial—the function n! = n × (n-1) × ... × 2 × 1—to non-integer values. Factorials appear everywhere: combinatorics (how many ways to arrange things), probability (binomial distributions, Poisson distributions), calculus (Taylor series coefficients). Extending the factorial means extending all of these.

The 2009 post "The gamma function" states it plainly: this is "the most important function not on a calculator." It comes up constantly, in probability, in statistics, in physics, in number theory. Yet standard calculators don't include it. The gap between importance and accessibility is one reason the blog explains it repeatedly.

The posts explore gamma from multiple angles:

- **Theoretical**: "Gamma function partial sums" (2017), exploring the convergence of its power series
- **Computational**: "Approximate inverse of the gamma function" (2017), with Python code using SciPy
- **Diagrammatic**: "Diagram of gamma function identities" (2010), mapping relationships visually
- **Asymptotic**: "Asymptotic series for gamma function ratios" (2020), for handling large values
- **Dimensional**: "Dimensional analysis for gamma function values" (2025), treating factorials as having units

This variety reflects how the gamma function is used. It's not one tool; it's a family of techniques, each applicable in different contexts.

---

## Fourier: The Workhorse

20 posts mention "Fourier" in titles. Another 45 carry the "Fourier analysis" tag, for 50 distinct posts across the blog when you account for overlap.

- First: 2011
- Most recent: 2023 ("Fixed points of the Fourier transform")

The Fourier transform decomposes a signal into frequencies. Any function of time can be expressed as a sum (or integral) of sine and cosine waves at different frequencies. This decomposition powers signal processing, image compression, audio engineering, and much of modern physics.

The blog treats Fourier not as abstract theory but as a working tool:

- "Reverse engineering Fourier conventions" (2022): Different textbooks use different conventions for the transform; the post sorts them out
- "Hilbert transform and Fourier series" (2022): Connecting Fourier to another transform
- "Fixed points of the Fourier transform" (2023): Which functions equal their own transform?

The last question is typical of Cook's approach. Most engineers learn the Fourier transform as a black box: feed it a signal, get out frequencies. But which functions are their own transform? The normal distribution is famous for this property. So, it turns out, is the hyperbolic secant. The question connects Fourier analysis to probability theory and to the Hermite functions of quantum mechanics.

[FIGURE: Stacked area chart showing special function mentions over time]

---

## Bessel: The Physicist's Tool

12 posts about Bessel functions.

- First: 2010
- Most recent: 2024 ("Bessel, Everett, and Lagrange interpolation")

Bessel functions solve Bessel's differential equation, which arises when you separate variables in the Laplace equation in cylindrical or spherical coordinates. In practice, this means Bessel functions appear in:

- Heat conduction in cylinders
- Vibrations of circular membranes (drumheads)
- Electromagnetic wave propagation
- Quantum mechanics

The blog posts reflect this physical motivation:

- "Bessel zero spacing" (2024): The zeros of Bessel functions determine resonant frequencies
- "Sinc approximation to Bessel function" (2022): Simple approximations for practical use
- "Bessel, Everett, and Lagrange interpolation" (2024): Connections to numerical methods

Bessel functions are less famous than sine and cosine, but they're equally fundamental for curved geometries. A physicist working with cylindrical symmetry reaches for Bessel as naturally as a high school student reaches for sine.

---

## Laplace: Transforming the Problem

12 posts about Laplace transforms or Laplace's equation.

- First: 2011
- Most recent: 2024 ("Moments with Laplace," "Laplace transform inversion theorems")

The Laplace transform is another tool for transforming problems—in this case, converting differential equations into algebraic equations. Engineers use it constantly because differential equations describe physical systems, and algebraic equations are easier to solve.

The posts reflect engineering applications:

- "Solving Laplace's equation in the upper half plane" (2022): A classic boundary value problem
- "Laplace transform inversion theorems" (2024): How to get back from the transformed domain

Where Fourier decomposes into frequencies, Laplace handles systems with exponential growth or decay. The two transforms are cousins, related mathematically but suited to different problems. The blog explains both.

---

## Zeta: Number Theory's Function

9 posts about the Riemann zeta function.

- First: 2014
- Most recent: 2025 ("Brownian motion and Riemann zeta")

The zeta function is the bridge between continuous and discrete. Its definition involves an infinite sum; its properties encode the distribution of prime numbers. The Riemann hypothesis—that all non-trivial zeros of zeta lie on a specific line—is one of mathematics' most famous unsolved problems.

The blog approaches zeta with appropriate caution:

- "Zeta sum vs zeta product" (2023): Two different ways to express the function
- "Mellin transform and Riemann zeta" (2024): How zeta connects to other transforms
- "Brownian motion and Riemann zeta" (2025): Surprising connections to probability

Zeta is advanced material. The posts assume readers who already know why they might care about prime distribution or analytic continuation. But for those readers, the blog provides working connections—not just definitions, but relationships to other tools.

---

## The Supporting Cast

Smaller roles, but persistent:

**Hypergeometric functions** (9 posts, 2016-2024): A vast generalization that includes many other functions as special cases. "Hypergeometric" is less a single function than a framework—the hypergeometric series can represent Bessel functions, Legendre polynomials, and many others. The posts explain how to recognize hypergeometric form and why you'd want to.

**Legendre polynomials** (4 posts, 2019-2025): Solutions to Legendre's equation, which arises in spherical harmonics. Important in physics (gravitational fields, quantum angular momentum) but also in numerical methods (Gaussian quadrature). The posts span theory and application.

---

## The Tag: "Special Functions"

Beyond individual function names, 140 posts carry the "Special functions" tag. This includes posts about:

- Error functions and normal distributions
- Elliptic integrals and elliptic functions
- Orthogonal polynomials
- Hypergeometric and confluent hypergeometric functions
- Bessel and Bessel-related functions
- Beta functions (related to gamma)

The tag marks territory: here be functions with names, functions that recur, functions worth knowing. 140 posts over seventeen years is roughly eight per year—a steady engagement with the named tools of mathematical work.

[FIGURE: Bump chart showing which function dominated which era]

---

## Why Names Matter

A name creates a handle. Once the gamma function has a name, you can say "use the gamma function" instead of describing the integral from scratch. You can look it up. You can find software that computes it. You can connect your problem to everyone else who's encountered the same function.

The blog's engagement with special functions is partly about education—explaining what gamma or Bessel or zeta means—and partly about advocacy. These are useful tools. They should be known. The calculator that lacks the gamma function is missing something important.

Cook wrote in 2021: "I find simple approximations more interesting than highly accurate approximations." This captures the blog's approach to special functions. The goal isn't to list every identity and asymptotic expansion. It's to show that these functions are *usable*—that you can approximate them, compute them, apply them to actual problems.

---

## The Bestiary Evolves

The special functions appearing in the blog shift over time.

Gamma appears across all seventeen years—it's fundamental, unavoidable. Bessel and Laplace appear steadily through the middle and recent eras, reflecting ongoing engagement with physics and engineering problems.

Zeta appears later (2014 onward), perhaps as the blog's number-theoretic interests deepened. Hypergeometric functions also appear in the later years—they require more mathematical machinery to appreciate, and the blog's audience may have grown more sophisticated.

The evolution isn't dramatic—no function appears and vanishes like PowerShell in Chapter 2. But there's gradual deepening: from the fundamental functions (gamma, Fourier) to the more specialized ones (hypergeometric, zeta).

---

## Inside the Bestiary

A bestiary catalogs creatures. The medieval bestiaries described lions and unicorns, real and imagined animals that populated the world. A mathematician's bestiary catalogs named functions—the creatures that populate mathematical space.

The blog's bestiary is weighted toward the applied. Gamma and Fourier appear constantly because statistics and signal processing require them. Bessel and Laplace appear because physics and engineering require them. Even zeta, the most number-theoretic of the group, gets connected to probability (Brownian motion) and transforms (Mellin).

This is a working mathematician's bestiary. The functions that recur are the functions that solve problems. The names that appear are the tools that get used.

And the blog teaches these tools not as abstractions but as instruments. Here is the gamma function. Here is why you need it. Here is Python code that computes it. Here is how it connects to the other functions you already know.

That's what a bestiary is for: not just to catalog, but to enable the hunt.
