# Scope: Autonomous X Bot for John D. Cook Blog Facts

## Project Overview

Build a fully autonomous X (Twitter) account that posts interesting facts derived from John D. Cook's blog posts. Zero ongoing maintenance after initial setup.

---

## Content Inventory

| Metric | Value |
|--------|-------|
| Published blog posts | 698 |
| Total words | 93,123 |
| Avg words/post | 133 |
| Source | WordPress SQL dump (2024-07-05) |

### Content Gap Analysis

**Do we need more content?** No - we have plenty.

| Posting Frequency | Facts Needed | Years of Runway (est.) |
|-------------------|--------------|------------------------|
| 4x/day | 1,460/year | ~1.4 years (with 2 facts/post) |
| 2x/day | 730/year | ~2.8 years |
| 1x/day | 365/year | ~5.7 years |

**Estimate: 2-3 tweetable facts per post = 1,400-2,100 facts**

At 2 posts/day, that's **2-3 years of content** before repeating.

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ facts.json  │  │ state.json  │  │ .github/workflows/  │  │
│  │ (all facts) │  │ (posted IDs)│  │   post-fact.yml     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                    GitHub Actions (cron)
                              │
                              ▼
                    ┌─────────────────┐
                    │  post_fact.py   │
                    │  - Pick fact    │
                    │  - Post to X    │
                    │  - Update state │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │    X API v2     │
                    │  (Free Tier)    │
                    └─────────────────┘
```

---

## Deliverables

### Phase 1: Fact Generation (One-time)
- [ ] Script to extract tweetable facts from blog posts using Claude API
- [ ] Output: `facts.json` with 1,500-2,000 facts
- [ ] Each fact: `{ id, text, source_post_slug, source_post_title }`
- [ ] Constraint: max 260 chars (leave room for link)

### Phase 2: Bot Infrastructure
- [ ] `post_fact.py` - Core posting script
- [ ] `state.json` - Track posted fact IDs (avoid repeats)
- [ ] `.github/workflows/post-fact.yml` - Cron trigger
- [ ] GitHub Secrets: `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET`

### Phase 3: User Setup (Manual)
- [ ] Create X Developer account (free tier)
- [ ] Create X app with read/write permissions
- [ ] Add API credentials to GitHub Secrets
- [ ] Enable GitHub Actions

---

## Costs

| Item | Cost |
|------|------|
| GitHub Actions | $0 (2,000 min/month free) |
| X API Free Tier | $0 (1,500 posts/month) |
| Claude API (one-time fact generation) | ~$2-5 |
| **Total ongoing cost** | **$0/month** |

---

## Constraints & Risks

### X API Risks
- Free tier limited to 1,500 posts/month (50/day max)
- X could change/remove free tier at any time
- Rate limits: 50 posts per 24 hours

### Content Risks
- Some posts may not condense well to standalone facts
- Need human review of generated facts before launch
- No automatic engagement/replies (fully robotic feel)

### Mitigation
- Generate facts conservatively (quality > quantity)
- Include link to original post for context
- Consider occasional manual engagement to humanize

---

## Timeline

| Phase | Effort | Notes |
|-------|--------|-------|
| Fact generation script | 1-2 hours | Claude API batch processing |
| Generate & review facts | 2-3 hours | Run script, manually review output |
| Bot infrastructure | 1-2 hours | Python script + GitHub Action |
| X API setup | 30 min | Developer account, app creation |
| Testing & launch | 1 hour | Verify posting works |
| **Total** | **6-8 hours** | Then zero ongoing effort |

---

## Example Output

**Input post:** "Honeybee genealogy" (224 words about Fibonacci in bee family trees)

**Generated facts:**
1. "Male honeybees have only a mother (born from unfertilized eggs), while females have both parents. The number of ancestors at each generation follows the Fibonacci sequence."

2. "The Fibonacci sequence appears in honeybee genealogy: count a male bee's ancestors at each generation level and you get 1, 1, 2, 3, 5, 8..."

3. "Unlike the famous rabbit problem, honeybee genealogy is a real-world example of Fibonacci numbers in nature."

---

## Decision Points

1. **Posting frequency?** Recommend: 2x/day (sustainable, not spammy)
2. **Include links?** Recommend: Yes, link to original blog post
3. **Account branding?** Need: Name, bio, profile image
4. **Review process?** Recommend: Human review of all facts before launch

---

## Next Steps

1. Confirm posting frequency and branding decisions
2. Generate facts using Claude API
3. Human review of fact quality
4. Set up X Developer account
5. Deploy GitHub Action
6. Launch
