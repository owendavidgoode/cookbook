# Epilogue: How This Book Was Made

This is a book about a mathematician's blog, made by counting things. It seems only fair to explain how the counting was done.

---

## The Data

Everything derives from publicly available data. The blog at johndcook.com runs on WordPress, which means every post has structured metadata: title, date, categories, tags, word count. This metadata was extracted, cleaned, and stored in a few primary files (5,233 rows mapping dates to titles to word counts to tags).

The repository that produced this book holds 220 MB across 2,850 files. The data directory accounts for 73 MB; the book text and LaTeX compilation takes 24 MB; scripts total 300 KB. This scope reflects the scale of Cook's archive.

No private data was used. The blog is public; this work simply organized what was already there.

---

## The Tools

**Python 3.12** for all data processing—the same language Cook has written about extensively.

**pandas** for data manipulation. **matplotlib** and **seaborn** for visualization. Every chart in this book was generated programmatically. The code is reproducible.

**Pandoc** for document compilation. Markdown to PDF, with LaTeX for typesetting.

The choice to use Python was partly practical and partly fitting: analyzing a blog with tools the blogger helped people understand.

---

## The AI Assistance

This book was written with substantial assistance from Claude, an AI made by Anthropic. Not as a ghostwriter (every word was reviewed, edited, and approved by humans) but as a collaborator for exploration, drafting, and iteration.

The repository root contains a `CLAUDE.md` file with instructions that persist across sessions: coding conventions, file organization, project context. This is "spec-driven development": a specification document that compounds across sessions, each one starting with full context rather than a blank slate.

The rhythm was collaborative. The human provides direction and judgment. The AI provides speed and tirelessness. Neither could produce this book alone.

---

## The Irony

There's an irony worth naming.

This is a book celebrating seventeen years of one person's writing. Cook wrote 1.8 million words by hand, one post at a time. No shortcuts. Pure human persistence.

The irony is this: a book on human persistence, built with AI speed. Visualizations that would have taken hours appear in seconds. Drafts that would have taken days arrive in minutes.

Is this cheating? Is it homage?

Cook himself has written about AI: about automation and its limits, about the boundary between human and machine intelligence. He's not a Luddite. He's curious about tools.

---

## What the AI Can't Do

Certain things remained stubbornly human:

**Judgment.** The AI can generate twelve visualization types. It can't tell you which one serves the chapter's argument. That requires understanding what the book is *for*.

**Taste.** The first visual sampler was four pages and felt like a tech demo. A human said "this won't work." The AI couldn't have made that call.

**Structure.** The original outline had eighteen chapters. It was a data dump, not a book. A human recognized this.

**The prologue.** The AI wrote drafts. But the decision about what the prologue should *do* (establish significance, justify the book's existence, set the tone) was human.

This book is human-directed and AI-assisted. The shape, the purpose, the reason it exists: those are human.

---

## A Different Kind of Methodical

This project is the mirror image of the work it describes.

The blog was built slowly, one small post at a time, with no master plan beyond showing up and explaining something clearly. This book came together quickly once the data and tools were in place: a compressed burst made possible only because those seventeen years of methodical writing existed to analyze.

The contrast says something about human-generated content in an era of automation. As models improve, it becomes easier to synthesize and visualize what already exists. What does not get easier is producing the raw material worth summarizing: the careful explanations, original examples, and durable insights that give these tools anything meaningful to work with.

Cook's archive is a reminder that even in an era of AI, the slow accumulation of clear human work is what matters most.

---

## Closing Thoughts

Cook has written about the tools we use and how they shape our thinking. Python as a thinking tool. LaTeX as a writing environment. The way software encodes assumptions.

This book was made with tools he would recognize. Python, pandas, matplotlib: the same stack he's explained in dozens of posts. If there's a fitting tribute to a technical blogger, it might be this: the tools he taught others to use were turned back on his own work.

Whether that's homage or irony is left to the reader.

And whether the method transfers—whether you, too, can just do things, can build something useful by showing up day after day—that's left to you.

---

*This epilogue was drafted with AI assistance and edited by humans. The full editorial process—including assessments from four AI editors (Claude, Codex, Gemini, and Grok) and two revision passes—is documented in the `editorial/` folder.*
