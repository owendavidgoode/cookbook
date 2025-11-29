# Epilogue: How This Book Was Made

This is a book about a mathematician's blog, made by counting things. It seems only fair to explain how the counting was done.

---

## The Data

Everything in this book derives from publicly available data. The blog at johndcook.com runs on WordPress, which means every post has structured metadata: title, date, categories, tags, word count. This metadata was extracted, cleaned, and stored in three primary files:

- **posts_metadata.csv**: 5,233 rows, one per post. Date, title, word count, categories, tags.
- **johndcook_posts_enriched.jsonl**: Full post content, including HTML, for deeper analysis.
- **johndcook_calendar_candidates_filtered.csv**: 1,599 curated facts derived from the metadata—statistical observations, curiosities, patterns.

No private data was used. No APIs were accessed. No scraping was performed against the author's wishes. The blog is public; this work simply organized what was already there.

---

## The Tools

The analysis and visualization pipeline is straightforward:

**Python 3.12** for all data processing. The language John D. Cook himself has written about extensively—207 posts tagged "Python" at last count.

**pandas** for data manipulation. Loading CSVs, filtering, grouping, aggregating. The workhorse of data science, unglamorous and essential.

**matplotlib** and **seaborn** for visualization. Every chart in this book was generated programmatically, not drawn by hand. The code is reproducible; run it again and you'll get the same images.

**Pandoc** for document compilation. Markdown to PDF, with LaTeX for typesetting. The same toolchain many technical writers use—including, occasionally, John D. Cook himself.

The choice to use Python was partly practical and partly poetic: it is the language the blog often discusses. There's something fitting about analyzing a blog with tools the blogger helped people understand.

---

## The Visualizations

This book contains roughly 25 distinct visualizations. Each one was chosen to answer a specific question, not to decorate a page. The philosophy:

**Chart type follows question.** A treemap shows proportions. A bump chart shows ranking changes. A connected scatterplot shows trajectory through two-dimensional space. Chart types were chosen for what they revealed, not for novelty.

**Consistency over variety.** The same color palette throughout: deep navy (#1a365d) as primary, warm orange (#ed8936) as accent. Serif fonts for all text. 300 DPI for print quality. The goal was a unified visual language, not a showcase of techniques.

**Annotations matter.** A chart without context is just shapes. Every visualization includes titles, axis labels, and—where useful—callouts highlighting what to notice.

The visual sampler in Chapter 0 (not shown here) catalogs twelve visualization types we considered. Not all made it into the final book. The waffle chart of fact types was cut for being too meta. The fake tweet mockup was cut for being too cute. What remains is what served the story.

---

## The Repository

This book was developed in a Git repository called `cookbook/`. The structure:

```
cookbook/
├── data/                    # Source data files
│   ├── posts_metadata.csv
│   ├── johndcook_posts_enriched.jsonl
│   └── johndcook_calendar_candidates_filtered.csv
├── book/                    # Manuscript files and current outline
│   ├── 00-prologue.md
│   ├── 01-shape-of-seventeen-years.md
│   ├── ...
│   ├── 99-epilogue.md
│   └── OUTLINE_V4.md
├── scripts/                 # Visualization generators
│   ├── generate_visual_sampler_v2.py
│   └── ...
├── BOOK_PLAN.md             # Original outline (superseded)
└── CLAUDE.md                # Instructions for AI assistants
```

The repository is the book's source of truth. Every draft, every visualization script, every outline revision is version-controlled. Nothing is lost; everything can be traced.

---

## The CLAUDE.md File

Here's where things get interesting.

This book was written with substantial assistance from Claude, an AI assistant made by Anthropic. Not as a ghostwriter—every word was reviewed, edited, and approved by humans—but as a collaborator. A tool for exploration, drafting, and iteration.

The `CLAUDE.md` file in the repository root contains instructions for the AI. It specifies coding conventions, file organization, commit message formats, and project context. When a new session begins, the AI reads this file and understands how to contribute to the project.

This is a technique called "spec-driven development." Instead of giving instructions one at a time, you write a specification document that persists across sessions. The instructions compound. Each session starts with full context, not a blank slate.

A sample from the actual CLAUDE.md:

```markdown
## Project Structure & Module Organization
- `src/` for primary modules/CLI; keep one concern per folder.
- `recipes/` for runnable examples/snippets with brief READMEs.
- `tests/` mirrors `src/`.
- `scripts/` for repeatable automation; keep idempotent.
```

Simple rules, but they add up. Over dozens of sessions, the AI learned the project's shape and could contribute meaningfully.

---

## The Sessions

The book developed over multiple working sessions, each documented. A file called `book.md` served as a running log—context that could be passed to a new session when the previous one ended.

This is the strange reality of AI-assisted work in 2025: the AI has no persistent memory. Each session starts fresh. But with good documentation, the *project* has memory, even if the tool doesn't.

A typical session might look like:

1. Human: "Read book.md and regain context from the previous session."
2. AI: [Reads file, summarizes status, asks clarifying questions]
3. Human: "Generate visualizations for Chapter 4."
4. AI: [Writes Python script, runs it, presents results]
5. Human: "The dumbbell chart needs better labels."
6. AI: [Revises script, regenerates image]
7. Human: "Good. Update book.md with what we did."
8. AI: [Appends session summary to the log]

The rhythm is collaborative. The human provides direction and judgment. The AI provides speed and tirelessness. Neither could produce this book alone.

---

## The Irony

There's an irony here worth naming.

This is a book celebrating seventeen years of one person's writing. John D. Cook wrote 1.8 million words by hand, one post at a time, over nearly two decades. No shortcuts. No automation. Pure human persistence.

And here is the irony: a book about one person's sustained human effort, assembled with AI assistance. Visualizations that would have taken hours to draw now appear in seconds. Drafts that would have taken days to produce arrive in minutes. Tools that did not exist when the blog started are now being applied to the story of that earlier era.

Is this cheating? Is it homage? Is it something else entirely?

There is no clean answer. But John D. Cook himself has written about AI—about what computers can and can't do, about automation and its limits, about the boundary between human and machine intelligence. He's not a Luddite. He's curious about tools.

If he reads this book, it's easy to imagine him being more interested in how it was made than bothered by the making.

---

## A Different Kind of Methodical

In that sense, this project is the mirror image of the work it describes. The blog was built slowly, one small, self-contained post at a time, with no master plan beyond showing up and explaining something clearly. This book, by contrast, came together quickly once the data and tools were in place—a compressed burst made possible only because those seventeen years of methodical writing existed to analyze.

The contrast says something about the future of human-generated content. As models improve, it becomes easier to synthesize, summarize, and visualize what already exists. What does not get easier is producing the raw material worth summarizing: the careful explanations, original examples, and small, durable insights that other people will someday mine for patterns. Cook's archive is a reminder that even in an era of automation, the slow, steady accumulation of clear human work is what gives these tools anything meaningful to work with.

There is also a different kind of effort embedded here: the work of leaving things out. Compressing 5,233 posts into a short book is not simply a matter of scale; it is an exercise in restraint, in deciding which patterns are representative and which fascinations have to be mentioned only in passing. That editorial labor—the discipline to say less about more—is a quieter cousin of Cook's own methodical practice, and just as dependent on human judgment.

---

## What the AI Can't Do

For all the AI assistance, certain things remained stubbornly human:

**Judgment.** The AI can generate twelve visualization types. It can't tell you which one actually serves the chapter's argument. That requires understanding what the chapter is *for*, which requires understanding what the book is for, which requires understanding why anyone would make a gift like this in the first place. The AI doesn't have that context. Humans do.

**Taste.** The first visual sampler was four pages and felt like a tech demo. A human looked at it and said "this won't blow anyone's socks off." The AI couldn't have made that call.

**Structure.** The original outline had eighteen chapters. It was a data dump, not a book. A human recognized this and demanded a revision. The AI generated options, but the human chose.

**The prologue.** The AI wrote drafts. But the decision about *what the prologue should do*—establish the blog's historical significance, justify the book's existence, set the emotional tone—that was human. The AI can execute a vision. It can't originate one.

This book is human-directed and AI-assisted. The proportions vary by section—some passages are more heavily AI-drafted, others are almost entirely human-written. But the shape, the purpose, the reason it exists: those are human.

---

## The Stack

For the technically curious, the full toolchain:

| Layer | Tool |
|-------|------|
| Language | Python 3.12 |
| Data manipulation | pandas 2.x |
| Visualization | matplotlib 3.x, seaborn 0.13 |
| Document compilation | Pandoc 3.x with pdflatex |
| Version control | Git |
| AI assistance | Claude (Anthropic) |
| Repository hosting | Local (not published) |

Total lines of Python written for visualizations: ~800.
Total markdown words in the manuscript files: ~33,000.
Total sessions with AI assistance: ~15.

---

## Reproducing This Book

The repository contains everything needed to regenerate this book from scratch:

1. Clone the repository
2. Install Python dependencies (`pip install pandas matplotlib seaborn`)
3. Run visualization scripts (`python scripts/generate_*.py`)
4. Compile with Pandoc (`pandoc book/*.md -o book.pdf`)

The data is included. The code is included. The instructions are included. Anyone with basic technical skills could rebuild this book—or fork it, modify it, improve it.

This is intentional. A book about open, public intellectual work should itself be open. The blog is free to read. The book about the blog should be free to inspect.

---

## Closing Thoughts

John D. Cook has written about the tools we use and how they shape our thinking. He's written about Python as a thinking tool, about LaTeX as a writing environment, about the way software encodes assumptions.

This book was made with tools he would recognize. Python, pandas, matplotlib—the same stack he's explained in dozens of posts. If there's a fitting tribute to a technical blogger, it might be this: the tools he taught others to use were turned back on his own work.

Whether that's homage or irony is left to the reader.

---

*This epilogue was drafted with AI assistance and edited by humans. The repository, including all code and drafts, is available upon request.*
