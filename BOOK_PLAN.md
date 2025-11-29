# Book Plan: "You Can Just Do Things"

> **Subtitle**: How to Become Internet Famous
>
> **Status**: Active working document. See `book/` for chapter drafts and figures.

A data-driven companion book celebrating johndcook.com/blog through 17 years of posts.

## Concept

A nerdy, data-rich book that explores the blog's 5,000+ posts through careful analysis. Gift for the author - should feel like a love letter from someone who read the data carefully.

## Source Materials

All in `/data/`:
- `posts_metadata.csv` - Post metadata (dates, word counts, categories)
- `johndcook_posts_enriched.jsonl` - Full post content with categories/tags
- `johndcook_text_index.jsonl` - Text analysis index
- `wp_taxonomies/` - Category and tag definitions

## Chapter Structure

1. **The Shape of Seventeen Years** - Timeline, posting patterns, volume over time
2. **The Topography of Interest** - Category landscape, Math's dominance, the long tail
3. **The Rhythm of a Working Mind** - Weekly patterns, productivity cycles
4. **The Numbers That Keep Appearing** - Pi, primes, mathematical constants
5. **A Bestiary of Functions** - Gamma, Bessel, Fourier, special functions
6. **The Mathematicians Behind the Theorems** - Euler, Gauss, Ramanujan mentions
7. **Languages as Thinking Tools** - Python's rise, PowerShell's fall, Mathematica
8. **Cryptography's Moment** - The 2019 spike, RSA to elliptic curves
9. **The Edges of the Map** - Music, typography, clinical trials - the outlier categories
10. **On Consulting** - The business thread woven through technical content
11. **The Evolution of a Blog** - Three eras: high volume → quiet → depth
12. **What Makes a Post Endure** - Analyzing the most-referenced posts

**Appendix A**: By the Numbers - Key statistics
**Appendix B**: A Reading List - Notable posts by category

## Appendix
- Full timeline of first/last mentions for key terms
- Category/tag frequency tables
- Methodology notes

## Production Notes

### Tone
- Technical and precise - this is for someone who writes about math professionally
- Data-forward - let the numbers tell stories
- Affectionate but not sycophantic - genuine appreciation through careful attention

### Visual Elements
- Timeline charts (posting frequency over years)
- Network graphs (category/tag relationships)
- Word clouds (but tasteful ones)
- Pull quotes from actual posts
- Code snippets where relevant

### Length Target
- ~150-200 pages
- Each chapter 10-15 pages
- Heavy on data visualizations

## Technical Approach

1. **Data extraction scripts** - Pull specific slices for each chapter
2. **Visualization pipeline** - Matplotlib/Seaborn for charts, export to PDF-ready format
3. **Markdown drafts** - Write chapters as .md, compile with Pandoc
4. **LaTeX for final** - Professional typesetting, good math support

## Next Steps for Book Agent

1. Read this plan and `CALENDAR_FACTS_BRIEF.md` for context
2. Explore data files to understand available information
3. Start with Part I (macro view) - most straightforward data work
4. Draft Chapter 1 as proof of concept
5. Generate key visualizations
6. Iterate based on feedback

## Files to Preserve

The calendar facts work is ongoing. Key files:
- `johndcook_calendar_candidates_filtered.csv` - Current curated set (1,599 facts)
- `johndcook_calendar_candidates_merged.csv` - Pre-filtering merged set
- `johndcook_calendar_candidates_v3.csv` - Original large candidate pool

Do not modify these files. Create new files for book-specific analysis.

## Timeline

Not urgent - this is a gift project. Quality over speed.
