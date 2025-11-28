# @jdc_facts Twitter Bot

Autonomous bot that posts John D. Cook blog facts to [@jdc_facts](https://x.com/jdc_facts) on X (Twitter).

## How It Works

1. **GitHub Actions** runs on a cron schedule (8am + 6pm UTC)
2. **`post_fact.py`** picks a random unposted fact from `facts.json`
3. Posts to X via the Twitter API
4. Updates `state.json` to track what's been posted
5. Commits the state change back to the repo

Once all facts are exhausted, the state resets and it starts over.

## Files

| File | Purpose |
|------|---------|
| `facts.json` | 427 tweetable facts (auto-generated) |
| `state.json` | Tracks posted fact IDs (auto-updated by bot) |
| `post_fact.py` | Main bot script |
| `build_facts.py` | Regenerates `facts.json` from CSV sources |
| `requirements.txt` | Python dependencies (tweepy) |

## Fact Sources

Facts are pulled from these CSVs in `/data/`:

| Source | Count | Content |
|--------|-------|---------|
| `johndcook_calendar_365.csv` | 365 | Stats about the blog (posting patterns, word counts, etc.) |
| `hn_facts.csv` | 10 | Hacker News impact stats |
| `new_analysis_facts.csv` | 37 | Google Search Console & analysis facts |
| `additional_phd_facts.csv` | 15 | PhD-level statistical observations |

**Total: 427 facts** (~7 months at 2 posts/day)

## Regenerating Facts

If you add new facts to the CSV files:

```bash
python3 bot/build_facts.py
git add bot/facts.json
git commit -m "chore: regenerate facts"
git push
```

## Schedule

Configured in `.github/workflows/post-fact.yml`:

```yaml
schedule:
  - cron: '0 8,18 * * *'  # 8am and 6pm UTC
```

To change frequency, edit the cron expression and push.

## Manual Trigger

To post immediately:
1. Go to GitHub → Actions → "Post Fact to X"
2. Click "Run workflow"

Or via CLI:
```bash
gh workflow run post-fact.yml --repo owendavidgoode/cookbook
```

## Credentials

Stored as GitHub Secrets (Settings → Secrets → Actions):

| Secret | What |
|--------|------|
| `X_API_KEY` | Twitter API Key (Consumer Key) |
| `X_API_SECRET` | Twitter API Secret (Consumer Secret) |
| `X_ACCESS_TOKEN` | Access Token for @jdc_facts |
| `X_ACCESS_TOKEN_SECRET` | Access Token Secret for @jdc_facts |

These are tied to the [@jdc_facts](https://x.com/jdc_facts) account. To change which account posts, regenerate the Access Token/Secret while logged into the desired account.

## X Developer App

- **App Name**: JohnDCook Facts
- **App ID**: 31900498
- **Permissions**: Read and Write (OAuth 1.0a)

Developer portal: https://developer.twitter.com/en/portal/projects-and-apps

## Adding More Facts

1. Add rows to one of the CSVs in `/data/` with format:
   ```csv
   type,fact,source_link
   stats,"Your fact here (max 260 chars)",https://johndcook.com/blog/...
   ```

2. Regenerate: `python3 bot/build_facts.py`

3. Commit and push

The bot will include the new facts in rotation.

## Troubleshooting

**401 Unauthorized**: Access Token doesn't have write permission. Regenerate after setting app to "Read and Write".

**403 Forbidden**: Same as above, or the account is restricted.

**Duplicate tweets**: X blocks identical tweets. Each fact should be unique.

**State not updating**: Check that the workflow has `contents: write` permission.
