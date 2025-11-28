# Calendar Facts Brief for johndcook.com Corpus

Goal: Produce a large candidate pool (aim ~800+) of fun, quirky, content-specific facts for a daily desk calendar (Social Print Studio). Facts should be grounded in the blog content (not just metadata), e.g., “Only one post uses ‘pickle’: Dec 14 2018 in ‘<title>’ — a crypto article.” Do NOT cull to 365 yet; keep the big pool for later selection.

## Source Data
- Posts (full content, categories, tags): `data/johndcook_posts_api.jsonl` and `data/johndcook_posts_enriched.jsonl` (same posts, enriched with category/tag names).
- Taxonomies: `data/wp_taxonomies/categories.json`, `data/wp_taxonomies/tags.json`.
- Metadata table: `data/posts_metadata.csv` (id/slug/title/link/date/year/month/day/doy/weekday/word_count/categories/tags).
- Current draft facts (for reference, not final): `data/johndcook_calendar_facts.csv` (365 items; mostly rollups; replace with new set).

## Deliverable (for now)
- A candidate CSV with ~800+ facts; DO NOT trim to 365. Columns: `id` (or `idx`), `type` (e.g., rarity/first/last/density/constant/otd/quirk), `fact`, `source_link`. You can add helper columns (date, slug) if useful.
- Facts: 1–2 sentences, calendar-friendly, longer than tweet length if needed.
- Ensure varied topics: math/stats, programming, constants, privacy/crypto, on-this-day, rare terms, code/links/images outliers, interviews, etc.
- If a file named `data/johndcook_calendar_facts.csv` exists, write to a new filename like `data/johndcook_calendar_candidates_v2.csv` (or higher).

## What “good” looks like
- Content-specific quirks:
  - Rare term appearances (once/few times) with date/title/link.
  - First/last occurrence of notable terms (Bayesian, Fortran, machine learning, crypto, HIPAA/GDPR, Unicode, regex, FFT, PDE, Fibonacci/golden ratio, prime).
  - Outliers: most math symbols, most links, most images, longest code block, longest/shortest post (globally and per theme).
  - Constants/special functions: posts mentioning π/e/φ/τ/ζ, prime counts, Fibonacci/golden ratio, Riemann zeta, elliptic curves, special functions.
  - On-this-day: pick interesting posts for many days of year (unique dates if possible).
  - Interviews/Q&A, “how to,” music/arts crossovers.
- Each fact should carry a `source_link` (post link or relevant page).

## Suggested Workflow
1) Preprocess (if needed):
   - Convert HTML `content` to plain text while keeping math symbols if present.
   - Compute per-post stats: word_count, link_count, image_count, math symbol flags (π, φ, Φ, ∞), term flags (Bayes, Markov, prime, Fibonacci, golden, Riemann, PDE, FFT, Monte Carlo, lambda, category, graph, topology, linear algebra, special function, crypto, privacy/HIPAA/GDPR/CCPA, ML/AI, regex, Unicode, music).
2) Mine candidates (aim for 800–1000):
   - Rarity: terms appearing once/few times; report date/title/link.
   - First/last occurrence for notable terms.
   - Outlier density: most math symbols; most links/images; longest code block; longest/shortest posts overall and per theme/tag.
   - Constants/symbols: posts mentioning π/e/φ/τ/ζ; prime-themed posts; Fibonacci/golden ratio.
   - On-this-day: for many days of year, pick a notable/longest/most-themed post.
   - Interviews/Q&A, “how to,” privacy/crypto one-offs.
3) Stop before final selection:
   - Keep the full candidate pool (~800+). Do NOT dedup aggressively or trim to 365 yet.
4) Output CSV:
   - Columns: `id`/`idx`, `type`, `fact`, `source_link` (add date/slug/type-specific fields if helpful).
   - Save to a new filename if an existing one is present.

## Existing Scripts (helpful)
- `src/fetch_wp_api.py` – pulls posts via REST (already done).
- `src/fetch_wp_taxonomies.py` – pulls categories/tags.
- `src/enrich_posts_with_taxonomy.py` – joins names.
- `src/generate_calendar_facts.py` – prior rollup-based facts (use structure but replace content).

## Notes
- Social Print Studio cards allow more than tweet length; 1–2 concise sentences are fine.
- Prefer concrete, “did you know” tone with dates and links.
- Preserve math/Greek symbols when present. Keep everything ASCII-compatible unless symbols are the point (π/φ/etc.).***
