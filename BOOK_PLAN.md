# Book Plan: "The Endeavour by the Numbers"

A technical companion book celebrating johndcook.com/blog through data-driven exploration.

## Concept

A nerdy, data-rich book that uses calendar facts as entry points into deeper analysis of the blog's 17+ years and 5,000+ posts. Gift for the author - should feel like a love letter from someone who read the data carefully.

## Source Materials

All in `/data/`:
- `johndcook_calendar_candidates_filtered.csv` - 1,599 curated facts (starting points)
- `johndcook_posts_enriched.jsonl` - Full post content with categories/tags
- `johndcook_text_index.jsonl` - Text analysis index
- `posts_metadata.csv` - Post metadata (dates, word counts, categories)
- `wp_taxonomies/` - Category and tag definitions

## Proposed Structure

### Part I: The Shape of the Blog (macro view)
- **Chapter 1: 17 Years in Numbers** - Timeline visualization, posting patterns, evolution of topics
- **Chapter 2: The Category Landscape** - How Math (2,378 posts) relates to Music (85), Clinical Trials (55), Typography (50)
- **Chapter 3: The Long Tail** - Tags used exactly once, posts that stand alone

### Part II: Threads Through Time (longitudinal stories)
- **Chapter 4: The Bayesian Thread** - From "Musicians, drunks, and Oliver Cromwell" (2008) to "You can't have everything you want" (2025)
- **Chapter 5: Crypto's Arc** - First mention of Bitcoin (2018) through Monero stealth addresses (2025)
- **Chapter 6: Where Math Meets Music** - 30 posts exploring the intersection
- **Chapter 7: The Interview Collection** - Atiyah, Ghrist, Pickover, Chua, and others

### Part III: Curiosities & Outliers (micro view)
- **Chapter 8: The Longest and Shortest** - 1,926-word interview vs 15-word "Oil on a parking lot"
- **Chapter 9: Rare Words** - Terms appearing exactly once (pickle, freelance, doofenschmertz)
- **Chapter 10: The Visual Posts** - 23 images in flag comparison, 19 in cellular automata
- **Chapter 11: Link Forests** - Posts with 20+ outbound links

### Part IV: The Constants (mathematical themes)
- **Chapter 12: Pi's 404 Appearances** - How the constant weaves through the blog
- **Chapter 13: Special Functions** - Bessel, Gamma, Zeta across the years
- **Chapter 14: The Mathematicians** - Euler (124 mentions), Gauss (55), Ramanujan (34)

### Appendix
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
