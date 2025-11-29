# Chapter 10: The Interviews

> "When someone tells me a general theorem I say that I want an example that is both simple and significant."
> — Sir Michael Atiyah, in conversation with John D. Cook (2013)

---

The blog isn't a monologue. Twenty-two times between 2008 and 2022, Cook handed the microphone to someone else.

The interviews are scattered across the archive—never a regular feature, never announced as a series. They appear when Cook encounters someone interesting and decides to ask questions. The subjects range from a Fields Medalist to a weather forecast entrepreneur, from the creator of VisiCalc to an Emacs enthusiast exploring early retirement.

What do these conversations reveal? Something about how a mathematician relates to the world outside mathematics.

---

## The Interview Count

| Year | Interview Posts |
|------|-----------------|
| 2008 | 1 |
| 2009 | 3 |
| 2010 | 2 |
| 2011 | 7 |
| 2012 | 2 |
| 2013 | 3 |
| 2014 | 1 |
| 2016 | 1 |
| 2017 | 1 |
| 2022 | 1 |

Twenty-two posts with "interview" in the title, but the count is misleading. Some are brief pointers—"New podcast interview" (33 words), "Seven interviews" (61 words), link collections rather than original conversations. Perhaps a dozen represent substantial original interviews conducted by Cook himself.

The peak year is 2011, with seven mentions, though several of those are compilations or references. The sustained original interviewing happened primarily in 2009-2013, then tapered off.

---

## The Subjects

Who gets interviewed?

**Sir Michael Atiyah** (September 2013, 1,926 words): The longest interview in the archive. Atiyah won the Fields Medal in 1966 and the Abel Prize in 2004. He was among the most decorated mathematicians alive when Cook spoke with him at the Heidelberg Laureate Forum.

**Robert Ghrist** (September 2010, 1,814 words): A mathematician and engineer at Penn, working in "applied topology"—a phrase that surprised Cook enough to prompt a phone call. Topology has always had applications to other mathematics; Ghrist was applying it directly to practical problems like sensor networks and data analysis.

**Cliff Pickover** (August 2009, 1,594 words): Prolific author of popular mathematics books, including *The Math Book*, which Cook reviewed. Pickover has written over forty books on mathematics, science, and the boundaries between.

**Sacha Chua** (March 2013, 1,243 words): An Emacs user and entrepreneur exploring "semi-retirement"—saving enough to spend five years experimenting with consulting, sketching, and writing. The conversation ranged from technical tools to life design.

**Eric Floehr** (April 2011, 1,241 words): Founder of ForecastWatch, a company that evaluates weather forecast accuracy. He built the business as a Python side project to satisfy personal curiosity about whether different forecasters actually differed in accuracy.

**Chris Toomey** (June 2016, 1,095 words): A developer at thoughtbot who came to Ruby through Rails. The conversation explored programming language preferences and the tension between expressiveness and strictness.

**Dan Bricklin** (June 2009, 1,028 words): Creator of VisiCalc, the first spreadsheet, which helped establish the personal computer as a business tool. By 2009, Bricklin was working on SocialCalc, a JavaScript-based open-source spreadsheet.

**Carl Franklin** (July 2009, 824 words): Podcaster, producer, and developer behind .NET Rocks and other technology podcasts. A musician first—piano since age four, programming since seventeen.

---

## The Atiyah Interview

The conversation with Sir Michael Atiyah deserves separate attention. It's the blog's longest interview, and it captures a mathematician at the summit of the profession reflecting on craft.

The setting was the Heidelberg Laureate Forum in 2013, a conference bringing together young researchers and mathematical laureates. Cook was covering the event for the conference blog, but this conversation went deeper than conference reporting.

Atiyah on mathematical exposition:

> "Too many people write papers that are very abstract and at the end they may give some examples. It should be the other way around. You should start with understanding the interesting examples and build up to explain what the general phenomena are."

This principle—particular before abstract—resonates through Cook's own blog. Post after post starts with a specific calculation, a concrete example, a number you can compute, before gesturing toward the general theory. Whether by conscious adoption or independent discovery, the blog embodies Atiyah's prescription.

On the relationship between simple and significant:

> "When someone tells me a general theorem I say that I want an example that is both simple and significant. It's very easy to give simple examples that are not very interesting or interesting examples that are very difficult. If there isn't a simple, interesting case, forget it."

This is a demanding standard. Most examples are either trivial (simple but not significant) or overwhelming (significant but not simple). The existence of a simple, significant example is a test of whether the general theorem matters. The blog's recurring challenge is to find such examples—numbers that illustrate principles, calculations that reveal structure.

On abstraction and the concrete:

> "Mathematics is built on abstractions. On the other hand, we have to have concrete realizations of them. Your brain has to operate on two levels. It has to have abstract hierarchies, but it also has to have concrete steps you can put your feet on."

The blog operates on both levels, but always returns to the concrete. Here's the formula—but also here's the Python code that computes it. Here's the theorem—but also here's the specific case where n = 7.

---

## Applied Topology

The Ghrist interview (2010) captures something different: Cook's encounter with an unexpected field.

> "When I ran across your website one thing that grabbed my attention was your research in applied topology. I've studied applied math and I've studied topology, but the two are very separate in my mind."

Ghrist's response:

> "Those two are separate in a lot of people's minds, but not for long. It's one of those things that the time has come and it's clear that the tools that were developed for very abstract, esoteric problems have really concrete value with respect to modern challenges in data, or systems analysis."

The interview proceeds to explain how algebraic topology—homology, cohomology, homotopy theory—can analyze data sets. Where traditional clustering finds connected components, topological methods find holes, voids, higher-dimensional structure. The abstract machinery of topology turns out to be practical.

This is a recurring theme in the blog's engagement with the world: the discovery that abstract tools have unexpected uses. The Ghrist interview documents one such discovery happening in real time, through the conversation itself.

---

## The Entrepreneurs

Several interviews feature people who built businesses from technical interests.

Eric Floehr (ForecastWatch) began by wondering whether weather forecasters actually differed in accuracy:

> "I wrote a little Python web scraper to pull forecasts from various places and compare it with observations. I kept doing that and realized there really were differences between the forecasters. I didn't start out for this to be a business. It just started out to satisfy personal curiosity."

Curiosity led to data; data led to insight; insight led to a business. The path is familiar to Cook's readers, who also start with curiosity and code.

Dan Bricklin reflected on what came after VisiCalc:

> "I wouldn't call it overshadowed, I'd call it added to and enhanced. Having done VisiCalc has opened many doors for me."

The creator of the first spreadsheet was, by 2009, working on an open-source JavaScript spreadsheet for the One Laptop Per Child project. The tools changed; the toolmaking continued.

Sacha Chua described her five-year experiment in alternative work:

> "At networking events, I like to shake people up a bit by telling them I'm semi-retired. I'm in this five-year experiment to see how awesome life can be."

Her integration of technical skills (Emacs, programming) with creative pursuits (sketching, illustration) paralleled Cook's own integration of mathematics with consulting.

---

## The Technology Angle

The interviews skew toward technology and programming, reflecting Cook's professional context.

Chris Toomey on programming language choice:

> "I chose Python over Ruby because of my engineering background. Python seemed more serious, while Ruby seemed more like a hipster language. Ruby sounded frivolous, but I kept hearing good things about it."

Carl Franklin on his path to programming:

> "I was singing in the Westerly Chorus from age 8. Piano since age 4. Guitar since age 10. ... Programming didn't come around till I was 17."

These are not mathematical interviews in the traditional sense. They're conversations about how technical people navigate careers, balance interests, choose tools. The mathematics appears at the edges—Python libraries, algorithm analysis, the occasional theorem—but the focus is on lives lived at the intersection of technology and curiosity.

---

## What the Interviews Reveal

The interview subjects share characteristics.

First: they all build things. Bricklin built VisiCalc and later SocialCalc. Floehr built ForecastWatch. Ghrist builds mathematical tools for applied problems. Even Atiyah, the pure mathematician, talks about building proofs, building understanding.

Second: they all cross boundaries. Ghrist crosses between mathematics and engineering. Chua crosses between programming and art. Franklin crosses between music and technology. The interviews feature people who refuse to stay in single categories.

Third: they all value the concrete. Atiyah wants simple, significant examples. Floehr wants actual forecast data. Bricklin wants working software. The abstract matters only when it touches the real.

These characteristics mirror the blog itself. Cook builds things (posts, code, explanations). He crosses boundaries (statistics, computing, music, typography). He values the concrete (code that runs, numbers you can check).

The interviews, then, are not departures from the blog's personality. They're conversations with kindred spirits—people who think and work the way Cook thinks and works.

---

## The Interview as Genre

Why interview at all? Why not just explain?

The interview format reveals something that exposition hides: the process of discovery. When Cook asks Ghrist about applied topology, the transcript preserves his surprise: "I was intrigued to hear you combine them." When Cook presses Atiyah for clarification, the exchange shows thinking in motion.

Exposition presents conclusions. Interviews present conversations. The former is more efficient; the latter is more human.

The blog's interviews humanize the technical world. These aren't abstractions—"topologists" or "entrepreneurs" or "developers." They're specific people with specific paths, specific surprises, specific tools. The interview format enforces specificity.

---

## The Fading Practice

The interviews fade after 2013. The late years of the blog contain brief pointers to external interviews (Cook being interviewed elsewhere) rather than original conversations. The sustained interviewing period was 2009-2013.

Why the change? Nothing in the metrics says. Perhaps the consulting work shifted. Perhaps the opportunity to attend conferences like the Heidelberg Laureate Forum ended. Perhaps the blog found other formats more suitable.

Whatever the reason, the interview archive represents a specific phase: a few years when the blog reached beyond monologue, engaging directly with other voices, other minds, other ways of bridging abstraction and application.

---

## The Lasting Questions

The best interview questions reappear across conversations.

To Bricklin: "What would your 30-second bio be without VisiCalc?" The question asks: who are you beyond your most famous achievement?

To Toomey: "What made you move toward stricter languages?" The question asks: how does experience change preferences?

To Floehr: "Did you start out intending this to be a business?" The question asks: how do side projects become central?

These are questions Cook might ask himself. What's the bio beyond the blog? How have seventeen years changed his approach? What started as curiosity and became something more?

The interviews don't answer these questions about Cook directly. But they circle around them, asking similar questions of others, gathering perspectives on how technical minds navigate long careers.

The blog is a conversation with readers. The interviews extend that conversation to include a few remarkable interlocutors who happened to pick up the phone.
