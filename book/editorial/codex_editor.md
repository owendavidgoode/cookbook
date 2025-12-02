# You Can Just Do Things — Editorial Report (Codex)

*Note: This report was written when the working title was "Methodical." The book has since been retitled "You Can Just Do Things: How to Become Internet Famous."*

This report treats the material under `book/` as a near‑final draft of
*You Can Just Do Things: How to Become Internet Famous* and responds
in three layers:

- Level 1: Big‑picture editorial letter
- Level 2: Chapter‑by‑chapter notes (purpose, strengths, risks)
- Level 3: Line‑level sample edits to demonstrate fixes

Throughout, the goal is to protect the existing voice while tightening
structure, sharpening the core promise, and reducing repetition.

---

## Level 1 — Big‑Picture Editorial Letter

### Core Promise and Transformation

- **Promise:** A data‑driven portrait of johndcook.com/blog as a
  "quiet institution" — influence without fame — told through counts,
  charts, and narrative that reveal what seventeen years of mathematical
  blogging actually look like.
- **Transformation for the reader:** Move from "I know John Cook writes
  a lot of good math posts" to "I see the architecture, obsessions, and
  evolution of his work, and I can place his blog in a larger story
  about persistence, craft, and tools."
- **What’s unique:** The combination of rigorous data work (counts,
  distributions, timelines) with a humane, essayistic voice that never
  lapses into academic dryness. This is not a fan zine or a dry
  analytics report; it reads like a serious nonfiction book about an
  unfashionable kind of influence.

### Ideal Reader and Shelf

- **Primary reader:** John D. Cook. The book should feel like a
  thoughtful, clear‑eyed gift that illuminates his own work without
  fawning.
- **Secondary readers:** Long‑time blog readers; mathematically literate
  programmers; data‑viz / blogging enthusiasts who admire deliberate,
  long‑term projects.
- **Shelf neighbors:** Oliver Burkeman’s *Four Thousand Weeks* (for the
  meditation on time and practice), James Gleick’s *The Information*
  (for big‑picture technical narrative), Ben Fry’s *Visualizing Data*
  (for the visual craft angle), and gift‑able data books like *Dear
  Data*.
- **Positioning:** "A data portrait of a mathematician’s blog" is
  strong, but the emotional hook is persistence and usefulness. Lean
  the positioning copy toward *methodical work in public* rather than
  *one more tech book with charts*.

### Overall Strengths

- **Voice and tone are already strong.**
  - Third‑person, calm, and confident.
  - Avoids second‑person address and direct flattery.
  - Uses metaphor and comparison ("climax species", "infrastructure
    without brand") without over‑indexing on cleverness.
- **Structure is thought through.**
  - Parts and chapter questions are clear and coherent.
  - Chapter titles are specific and rooted in the material.
  - The outline and manuscript mostly agree, which is rare at this
    stage.
- **Data is integrated, not dumped.**
  - Tables are well chosen and legible.
  - Visual placeholders ("[FIGURE: …]") are purposeful, not decorative.
  - Quantitative beats support narrative claims instead of replacing
    them.
- **Appendix A and B earn their keep.**
  - Appendix A provides trustworthy reference tables, so the main
    chapters can stay narrative.
  - Appendix B’s curated reading list is an excellent way to make the
    book immediately useful to technical readers who want to dive into
    the blog.

### Primary Risks

1. **Repetition of core statistics across the book.**
   - The 5,233 posts / 1.8 million words / 17‑year span appear in the
     prologue, Chapter 1, Appendix A, and sprinkled elsewhere.
   - The inverse relationship between quantity and depth is described in
     multiple places (Chapter 1, Chapter 3, Appendix A).
   - Risk: the early chapters start to feel like different angles on the
     same chart rather than distinct arguments.
   - Recommendation: Decide where each key number "belongs" and let
     other chapters reference it lightly instead of re‑explaining.

2. **Part boundaries blur in practice.**
   - Part I (architecture) and Appendix A both cover global statistics.
   - Part II (obsessions) and Part III (languages/tools) sometimes feel
     like variations on the same topic: what he writes about and how.
   - Chapters 8 and 9 both live at the "edge" of traditional math —
     cryptography and frontier topics — and could be more tightly
     differentiated in what they promise the reader.
   - Recommendation: Add one‑sentence "Part briefs" at the top of each
     Part in the manuscript itself (not just in the outline) and ensure
     each chapter leads with a promise that clearly advances that Part’s
     distinct job.

3. **Meta‑commentary on AI and tooling risks overshadowing Cook.**
   - The epilogue’s reflection on AI assistance and tooling is
     interesting and honest, but currently long enough to feel like a
     parallel subject.
   - Risk: the last taste in the reader’s mouth is "how this book was
     made with AI" rather than "what Cook’s persistence means."
   - Recommendation: Tighten the AI/tooling sections by ~30–40%, keep
     the best concrete details about the stack, and end on Cook and the
     blog, not on the tools.

4. **The "written to John" brief is only partially realized.**
   - The production spec says "Write it to John, let others overhear."
   - The current manuscript reads as if it is written *about* John for a
     general audience, not *to* John with others listening.
   - Recommendation: Decide firmly whether you want the "to John"
     conceit. If yes, weave in a handful of moments (per Part, not per
     chapter) where the narration tips gently toward him ("For Cook,
     this meant…", "You can see, John, how…") while maintaining third
     person in the bulk of the prose. If not, update the production spec
     to match the book you are actually writing.

5. **Some chapters are very data‑dense without enough story breaks.**
   - Chapter 2 (categories) and Chapter 8 (cryptography’s moment) in
     particular carry long stretches of tables and quantitative
     exposition.
   - Risk: non‑technical readers will glaze; technical readers will
     retain the gist but not the specific numbers.
   - Recommendation: Add 2–3 short, concrete anecdotes or cameo posts
     per dense chapter — specific posts that embody the pattern — and
     foreground them as mini‑stories that interrupt the data flow.

6. **Time‑sensitive numbers will age quickly.**
   - The text is precise about "through November 27, 2025". That’s good
     scholarship, but it also dates the book.
   - Recommendation: Add a short, explicit note early ("Data snapshot
     as of November 27, 2025; counts and URLs may have changed") and
     then avoid repeating the exact date in every chapter unless it is
     central to that chapter’s point.

### Priority Fixes (If You Do Nothing Else)

1. **Unify the role of Chapter 1 vs. Appendix A.**
   - Let Chapter 1 own the *narrative* of the big numbers — how the blog
     evolved over time.
   - Let Appendix A be the *reference table* for readers who want every
     breakdown.
   - Trim any full tables from Chapter 1 that are already present, in
     more detail, in Appendix A.

2. **Trim and sharpen the epilogue.**
   - Cut 20–30% of the material on AI/tooling and focus on:
     - Why this book exists.
     - What Cook’s practice says about human work in an automated era.
     - How to read and reuse the repo.

3. **Make each chapter’s opening explicitly answer its guiding
   question.**
   - The outline’s questions are excellent ("What does sustained
     intellectual output actually look like?", "What are the fixed
     points of a mathematical imagination?").
   - Many chapters begin with strong quotes and then ease into the topic
     without explicitly restating the question.
   - Add a sentence in each opener that rephrases the question in plain
     language and sets up what the reader will know by the end.

---

## Level 2 — Chapter‑by‑Chapter Notes

These notes assume the outline in `book/OUTLINE_V4.md` as the structural
source of truth and the drafted chapters in `book/*.md` as the current
text.

### Front Matter

**Foreword (planned, not drafted yet)**

- **Job:** Deliver a concise, warm, and credible endorsement of Cook and
  of this project, anchoring why the book matters now.
- **Risks to avoid:**
  - Don’t summarize the whole book; let the prologue do that.
  - Don’t over‑index on AI/tooling; keep the focus on Cook and the
    blog’s quiet influence.
- **Suggestion:** Aim for ~800–1,000 words. One page should be personal
  story (how you discovered the blog), one page should be why a book
  about it is worth anyone’s time.

**Prologue — `book/00-prologue.md`**

- **Purpose:** Establish scale (5,233 posts; 1.8M words), historical
  context (2008 web vs. now), and the thesis of "influence without
  fame."
- **What’s working:**
  - The opening number hook is excellent.
  - The historical comparison (App Store, Twitter’s early question) is
    concrete and helps situate non‑technical readers.
  - The "climax species" metaphor is vivid and memorable.
  - Tone is appreciative but not gushy.
- **Risks / opportunities:**
  - The prologue currently does a lot of work that Chapter 1 will redo
    with more data. Look for paragraphs that are essentially previews of
    Chapter 1’s tables and either cut or compress them to one sentence.
  - Consider ending one beat earlier, closer to the question "What does
    it look like when someone just keeps going?" The later material
    about what the book is not is useful but might be shorter.
  - Watch for a few generalized claims about "the internet" that could
    be tightened or specified with a concrete example.

### Part I — The Architecture (Chapters 1–3)

**Chapter 1: The Shape of Seventeen Years —
`book/01-shape-of-seventeen-years.md`**

- **Purpose:** Show the macro‑shape of output over time: counts,
  word‑length evolution, eras.
- **Strengths:**
  - The "Launch Year" vs. "Quiet Year" contrast is a clear narrative
    spine.
  - The connected scatterplot concept is strong and well described in
    prose.
  - The "trade‑off" section (quantity vs. depth) is a compelling
    insight.
- **Risks / tweaks:**
  - The opening currently reprises the prologue’s first post vs. latest
    post motif. Consider tightening this or referencing the prologue
    instead of re‑staging it.
  - The year‑by‑year table is long; since Appendix A repeats and extends
    it, you can shorten the in‑chapter table (e.g., show every other
    year or highlight a few anchor years) and direct the reader to the
    appendix for full detail.
  - Consider adding one or two specific cameo posts that embody each era
    (e.g., an early short note, a mid‑period in‑depth analysis, a late
    long post) to keep the chapter from feeling like pure aggregate
    data.

**Chapter 2: The Topography of Interest —
`book/02-topography-of-interest.md`**

- **Purpose:** Map what Cook’s mind organizes around via categories and
  tags.
- **Strengths:**
  - The "Math is the territory west of the Mississippi" metaphor is
    vivid and accurate.
  - The breakdown of "Overwhelming center / Practical layer / Surprising
    corners / Uncategorized mystery" gives the chapter a clear arc.
  - The use of tags within Math to reveal substructure works well.
- **Risks / tweaks:**
  - This chapter is table‑heavy. Readers will get the gist of the
    distribution without needing every count. Consider trimming one of
    the longer tables or moving some of the detail to Appendix A.
  - The "Uncategorized" section is intriguing; right now it gestures at
    mystery but could go one step further with a specific example of a
    post that ended up Uncategorized and what that suggests about Cook’s
    mental taxonomy.
  - The "Practical layer" section risks repeating themes that will show
    up later in the languages chapter; make sure the emphasis stays on
    *what* he writes about, not *which language he uses to do it*.

**Chapter 3: The Rhythm of a Working Mind —
`book/03-rhythm-of-a-working-mind.md`**

- **Purpose:** Show temporal rhythms — day of week, time of day, and
  seasonality — and what they reveal about practice.
- **Strengths:**
  - "This is a morning person" is a strong, human sentence that lands
    the data.
  - The contrast between flat monthly distribution and strong daily
    rhythm is interesting and non‑obvious.
  - The connected scatterplot reprise that ties rhythm to evolution
    works conceptually.
- **Risks / tweaks:**
  - Watch for over‑explaining obvious patterns (e.g., that Monday is
    meeting‑heavy) unless you can tie them to a specific anecdote about
    Cook’s known schedule.
  - Consider a small visual or anecdotal beat about "2 AM debugging
    sessions" as a *reader* rhythm, even if the posting rhythm is
    morning. You touch this well later in Chapter 12; you might
    cross‑reference.

### Part II — The Obsessions (Chapters 4–6)

**Chapter 4: The Numbers That Keep Appearing —
`book/04-numbers-that-keep-appearing.md`**

- **Purpose:** Highlight recurring numerical fascinations: pi, primes,
  randomness, Fibonacci, e.
- **Strengths:**
  - The "fixed points of a mathematical imagination" framing is
    excellent.
  - Using first/last appearance plus total counts gives a clear sense of
    persistence.
  - The planned dumbbell chart and timelines are exactly the right level
    of sophistication.
- **Risks / tweaks:**
  - The chapter could lean more on *how* treatment evolves (tone, depth,
    applications) rather than just *how often* topics appear.
  - Add at least one extended close reading of a single pi post and a
    single primes post to make the abstraction concrete.

**Chapter 5: A Bestiary of Functions —
`book/05-bestiary-of-functions.md`**

- **Purpose:** Show which special functions earn names and command
  repeated attention.
- **Strengths:**
  - The loose definition of "special function" is reader‑friendly and
    on‑brand.
  - The gamma / Fourier / Bessel sections are strong and grounded in
    specific posts.
  - The chapter does a good job connecting abstract functions to
    physical or computational contexts.
- **Risks / tweaks:**
  - Be careful not to let this become a mini‑textbook of special
    functions. The reader doesn’t need full definitions; they need to
    understand *why Cook* keeps returning to them.
  - Consider a brief comparison to which special functions *don’t* show
    up much, and what that implies about his practical interests.

**Chapter 6: The Mathematicians Behind the Theorems —
`book/06-mathematicians-behind-theorems.md`**

- **Purpose:** Use named mathematicians (Ramanujan, Erdős, Knuth, etc.)
  as a way into Cook’s intellectual lineage.
- **Strengths:**
  - The Ramanujan section is especially strong, combining admiration
    with honest acknowledgment of difficulty.
  - The Erdős material nicely balances biography and the blog’s concrete
    engagements with his theorems.
  - Knuth as a "bridge" figure between mathematics and computing is
    exactly right for this project.
- **Risks / tweaks:**
  - Ensure each mathematician’s section ties back explicitly to how
    Cook uses their work (not just who they were).
  - Consider whether any mathematician can be cut or combined to reduce
  - sprawl; prioritize those who appear across multiple chapters or
    topics.

### Part III — Languages as Thinking Tools (Chapters 7–8)

**Chapter 7: Languages as Thinking Tools —
`book/07-languages-as-thinking-tools.md`**

- **Purpose:** Track the evolution of Cook’s programming and tool
  choices, and what that reveals about his work.
- **Strengths:**
  - The treatment of Python’s rise vs. PowerShell’s extinction is
    clear, concrete, and narratively satisfying.
  - The "translation layer" section (math to code) is particularly good
    at explaining why programmers care what a mathematician thinks.
  - The chapter does a nice job tying back to specific posts ("10 best
    rational approximations for pi", etc.).
- **Risks / tweaks:**
  - Ensure consistency with Chapter 2’s "practical layer" so you’re not
    repeating the same story with a different lens. Here the focus
    should be on languages as *tools for thought*, not on categories.
  - The "PowerShell: The Fossil" section is fun but could be trimmed
    slightly; the point is made quickly.

**Chapter 8: Cryptography’s Moment —
`book/08-cryptographys-moment.md`**

- **Purpose:** Show how a long‑standing interest (number theory) became
  urgently practical via cryptography and privacy.
- **Strengths:**
  - The Hardy setup is excellent; it links pure math to applied crypto
    in a way any reader can follow.
  - The 2019 spike is a compelling data story with a clean visual.
  - RSA and elliptic‑curve sections are clear and technically sound at
    the narrative level.
- **Risks / tweaks:**
  - This chapter runs long and, at times, reads like a survey course in
    applied crypto. Trim definitions that could live in endnotes and
    keep the focus on Cook’s trajectory and choices.
  - Consider ending one section earlier and leaving some details for
    Appendix B’s reading list or for figure captions.

### Part IV — Edges of the Map (Chapters 9–10)

**Chapter 9: Edges of the Map —
`book/09-edges-of-the-map.md`**

- **Purpose:** Explore the frontier topics and unexplored territory that
  the data cannot fully capture.
- **Strengths:**
  - The "territory vs. map" distinction is clear and thematically
    important.
  - The sections on deleted comments and invisible influence are
    strong; they acknowledge limits without hand‑wringing.
- **Risks / tweaks:**
  - Be careful not to restate the same "limits of data" thesis too
    often. Each section should bring a distinct angle (students,
    comments, 2 AM debugging, etc.).
  - Consider pulling one or two of the most evocative examples earlier
    into the book and cross‑referencing here rather than debuting them
    all in Chapter 9.

**Chapter 10: Interviews —
`book/10-interviews.md`**

- **Purpose:** Use the long interview posts as lenses into Cook’s
  curiosity and range.
- **Strengths:**
  - The curated interview list in Appendix B is strong source material
    for this chapter.
  - The high word counts of interviews justify treating them as their
    own "form" within the blog.
- **Risks / tweaks:**
  - Make sure this chapter does not just summarize the interviews. Use
    them to show how Cook listens, what he asks, what he chooses to
    highlight.
  - One or two extended passages of close reading (a particular
    question, a surprising answer) will do more work than broad
    overview.

### Part V — Evolution and Meaning (Chapters 11–12, Epilogue, Appendices)

**Chapter 11: Evolution of a Blog —
`book/11-evolution-of-a-blog.md`**

- **Purpose:** Synthesize earlier patterns into a coherent story of how
  the blog changed over time.
- **Strengths:**
  - The era breakdown (early / middle / recent) matches Appendix A and
    provides a good frame.
  - The material on shifts in average post length, topic mix, and
    tooling belongs here and largely works.
- **Risks / tweaks:**
  - This chapter risks feeling like a recap of Chapters 1–3 and 7–8.
    To avoid that, emphasize *why* the evolution matters (what it says
    about sustained practice, about mid‑career change) rather than
    re‑listing how metrics moved.
  - Consider moving any new data tables introduced here into Appendix A
    and letting this chapter narrate the implications instead.

**Chapter 12: What the Numbers Miss —
`book/12-what-the-numbers-miss.md`**

- **Purpose:** Articulate the limits of quantitative analysis and gesture
  toward the unmeasurable impact of the blog.
- **Strengths:**
  - The 2 AM debugging and graduate‑student sections are excellent;
    they finally bring the reader’s own experience explicitly into the
    frame.
  - The "territory vs. map" move here pairs well with Chapter 9 and
    the epilogue.
- **Risks / tweaks:**
  - Ensure this chapter is not simply a more lyrical restatement of
    Chapter 9. It should focus on the *reader journey* and the nature
    of influence, not on data limitations per se.
  - Consider ending this chapter on a concrete, modest claim about what
    the book *can* do for readers, rather than on abstract
    epistemology.

**Epilogue — `book/99-epilogue.md`**

- **Purpose:** Explain how the book was made, reflect on AI assistance
  and tooling, and close with a meditation on human work and methodical
  practice.
- **Strengths:**
  - The honesty about AI use is refreshing and will age well.
  - The sections on judgment, taste, and structure underline why Cook’s
    practice still matters in an automated era.
  - The toolchain list is catnip for technically inclined readers.
- **Risks / tweaks:**
  - The epilogue currently tries to do three things—making‑of notes,
    AI reflection, and a final statement about Cook—and risks
    over‑staying.
  - Recommendation:
    - Compress the "Reproducing this book" instructions into either a
      short section here or into `book/README.md` plus a cross‑reference.
    - Tighten the AI commentary by replacing some abstractions with one
      or two memorable, concrete anecdotes about tools changing a
      decision.
    - Ensure the very last paragraphs land on Cook, the value of his
      archive, and what this book hopes to add — not on the tools.

**Appendix A — By the Numbers —
`book/appendix-a-by-the-numbers.md`**

- **Purpose:** Serve as the canonical reference for all statistics used
  in the book.
- **Strengths:**
  - Tables are clean, comprehensive, and clearly sourced.
  - The era breakdown is particularly helpful.
- **Risks / tweaks:**
  - Make sure every number that appears in the main text can be traced
    here; if you introduce a new metric, add it.
  - Consider a short introductory paragraph to remind readers that this
    appendix is where to go if they want to verify or reuse any
    numbers.

**Appendix B — A Reading List —
`book/appendix-b-reading-list.md`**

- **Purpose:** Offer a curated starting point for exploring the blog.
- **Strengths:**
  - The structure by theme (Interviews, Longest posts, Pi, Primes,
    Gamma, Fourier, Cryptography, etc.) is excellent.
  - Word counts are a nice touch for readers who want to skim vs. dive.
- **Risks / tweaks:**
  - Verify that every post referenced in the main chapters appears here
    or is consciously omitted; inconsistencies will frustrate motivated
    readers.
  - Consider a brief note in the introduction about how this list was
    chosen (e.g., word count, topic importance, cross‑disciplinarity).

---

## Level 3 — Line‑Level Sample Edits

These examples illustrate the kind of tightening that would make the
manuscript more potent without changing voice. They are not prescriptive
line‑edits for every instance, but patterns to apply.

### Sample 1 — Tightening Repetition in the Prologue

**Context:** Early in the prologue you give the 5,233 posts / 1.8M words
counts and then explain at length that the internet rewards novelty and
outrage rather than persistence.

**Current pattern (paraphrased):**

- You state the counts and span.
- You describe the changed internet (App Store, Twitter’s early days).
- You explain that algorithms reward novelty and outrage.
- You then repeat, in different words, that a blog like this cannot
  compete with that attention economy.

**Suggested revision pattern:**

- Keep the historical comparison and one sharp sentence about the
  modern internet’s incentives.
- Cut the second general paragraph about algorithms and novelty.
- Use the recovered space to foreshadow one concrete pattern that the
  book will unpack (e.g., the quiet 2014 dip or the morning rhythm).

This will make the prologue feel more like a controlled slide into the
book rather than a miniature essay on "what the internet rewards."

### Sample 2 — Sharpening Chapter Openers (Chapter 2)

**Context:** Chapter 2 currently opens with a strong quote and then a
paragraph explaining WordPress categories.

**Current first move (paraphrased):**

> WordPress requires categories; many bloggers treat this as a chore.

This is accurate but abstract.

**Suggested alternative:**

> The blog’s twenty‑six categories are the closest thing Cook has to a
> table of contents for his own mind. WordPress may force the choice,
> but the way those choices accumulate reveals what matters to him.

You can keep the existing explanation about WordPress as a supporting
sentence, but lead with what’s at stake for the reader: we’re about to
see how a mathematician files his thoughts.

### Sample 3 — Trimming Meta in the Epilogue

**Context:** In the epilogue’s AI section, you make several overlapping
points about what AI can and cannot do (judgment, taste, structure).

**Current pattern (paraphrased):**

- Paragraphs on judgment, taste, and structure individually.
- Paragraphs on "what the AI can’t do."
- Paragraph on "what the AI did do" (e.g., speed up drafting).

Some of these sentences say the same thing in different words.

**Suggested consolidation:**

- Combine judgment, taste, and structure under one concrete anecdote:
  for example, the moment a human looked at the first visual sampler and
  said "this won’t blow anyone’s socks off."
- Follow that with one specific example of a decision the AI *could*
  make well (e.g., proposing alternative framings for a chapter) and
  one it could not (e.g., deciding that eighteen chapters was too many).
- Close the section by explicitly tying back to Cook: his archive exists
  because of long‑term human judgment; the tools are simply a way of
  seeing it.

This will keep the epilogue’s tone confident and grounded, rather than
drifting into general AI commentary.

---

### Closing Note

The manuscript is already unusually coherent for this stage. The work
ahead is not reinventing structure but pruning repetition, reinforcing
each Part’s distinct job, and tightening a few overlong sections so that
the core story — a mathematician who quietly built a useful corner of
the internet over seventeen years — remains in sharp focus.

---

## Revision 2 — Alignment with `editor_pass_2_plan`

This section tracks how the Pass 2 integration plan in
`book/editorial/editor_pass_2_plan.md` lines up with Codex feedback, and
notes small adjustments.

### Items Fully Aligned

- **Ch 9 overhaul (Item 1):** Strongly endorsed. Cutting recap tables
  and focusing on *why* the evolution matters is exactly what I
  recommended.
- **Ch 1 vs. Ch 3 disentangling (Item 2):** Moving the connected
  scatterplot / trajectory into Chapter 1 and letting Chapter 3 own
  rhythm is the right conservative fix.
- **Cameo posts in dense chapters (Item 3):** This implements the prior
  request for concrete examples in data‑heavy sections. Keep each cameo
  brief (2–4 sentences) and tightly tied to the nearby table so
  chapters don’t re‑bloat.
- **Appendix B “Start Here” + curation note (Item 4):** Directly
  addresses the overwhelm risk of the 50‑post list and adds useful
  selection transparency.
- **Appendix A intro (Item 5):** Matches the suggestion to mark it as
  canonical reference and state the data snapshot explicitly.
- **Data snapshot note in Prologue (Item 6):** Correct place to anchor
  the “as of 2025‑11‑27” detail without repeating it everywhere.
- **Pull‑quote audit (Item 8):** Good polish; agree especially that
  Chapter 1 should have a quote that directly supports its explicit
  argument.
- **Chapter transitions (Item 9):** One‑sentence bridges are a good idea
  as long as they stay light and do not turn into mini previews.

### Items to Shape Carefully

- **Reflection prompts (Item 7):** The proposed light‑touch approach is
  acceptable if prompts stay limited:
  - One in the Prologue (for example: “What would the shape of your own
    work look like?”).
  - One in Chapter 10 (“What influence have you had that no metric
    captured?”).
  - Avoid extending prompts to every chapter so the book does not drift
    toward workbook tone.

### One Item to Reconsider

- **Keeping “Shortest Posts” in Chapter 10:** The plan currently lists
  “Move ‘Shortest Posts’ from Ch 10 to Appendix” under “Not Included.”
  From my side, I’d still lean toward:
  - Moving the full “Shortest Posts” table (and similar micro‑tables)
    into Appendix A, where they fit the reference function.
  - Leaving, at most, a single short illustrative example in Chapter 10
    to preserve texture without pulling that chapter back into a
    data‑dump mode.

If the rest of the plan is executed as written, plus this one tweak on
“Shortest Posts,” Pass 2 should close nearly all remaining structural
and density issues I’ve flagged.

---

## Revision 3 — Post–Pass 2 Notes

After reviewing the manuscript with Pass 2 edits applied:

- **Reflection prompts are at the right density.** They now appear only
  in the Prologue and Chapter 10, and both land well; I’d keep it at
  this level and resist adding prompts elsewhere.
- **Epilogue editorial note is slightly narrow.** It currently points
  only to `editorial/editor_pass_1.md`. To match `book/README.md` and
  reflect actual process, consider broadening to the whole
  `editorial/` folder or explicitly mentioning both
  `editor_pass_1.md` and `editor_pass_2.md`.
- **Title/subtitle consistency is the last global decision.** The
  working book identity is now “You Can Just Do Things: How to Become
  Internet Famous,” while many internal editorial docs still use
  *Methodical*. Before freezing a PDF or front‑matter, choose the final
  title/subtitle pair and make it consistent across `book/README.md`,
  cover/spine copy, and any title pages.
