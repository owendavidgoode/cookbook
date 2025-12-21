import csv
import datetime as dt
import json
import math
from pathlib import Path


DATA_DIR = Path("data")
BOOK_DIR = Path("book")


def load_posts():
    rows = []
    with (DATA_DIR / "posts_metadata.csv").open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["dt"] = dt.datetime.fromisoformat(row["date"])
            row["year"] = int(row["year"])
            row["word_count"] = int(row["word_count"] or 0)
            rows.append(row)
    return rows


def test_overall_counts_and_appendix_a():
    rows = load_posts()
    n_posts = len(rows)
    assert n_posts == 5233

    total_words = sum(r["word_count"] for r in rows)
    assert total_words == 1_823_200

    rows_sorted = sorted(rows, key=lambda r: r["dt"])
    first = rows_sorted[0]["dt"].date()
    last = rows_sorted[-1]["dt"].date()
    assert first == dt.date(2008, 1, 9)
    assert last == dt.date(2025, 11, 27)

    span_days = (last - first).days + 1
    assert span_days == 6533

    mean_words = total_words / n_posts
    assert round(mean_words) == 348

    from statistics import median

    med_words = median(r["word_count"] for r in rows)
    assert med_words == 312

    assert min(r["word_count"] for r in rows) == 5
    assert max(r["word_count"] for r in rows) == 1926

    appendix = (BOOK_DIR / "appendix-a-by-the-numbers.md").read_text()
    assert "| Total posts | 5,233 |" in appendix
    assert "| Total words | 1,823,200 |" in appendix
    assert "| Total days | 6,533 |" in appendix
    assert "| Mean words per post | 348 |" in appendix
    assert "| Median words per post | 312 |" in appendix
    assert "| Longest post | 1,926 words |" in appendix
    assert "| Shortest post | 5 words |" in appendix


def test_year_and_era_tables_match_data():
    rows = load_posts()

    # Year-level aggregates
    by_year = {}
    for r in rows:
        y = r["year"]
        by_year.setdefault(y, []).append(r["word_count"])

    expected_years = {
        2008: (410, 84446, 206, 163),
        2009: (366, 93597, 256, 194),
        2010: (284, 76186, 268, 212),
        2011: (317, 70508, 222, 185),
        2012: (357, 77133, 216, 181),
        2013: (260, 59789, 230, 172),
        2014: (147, 27607, 188, 158),
        2015: (168, 49277, 293, 238),
        2016: (209, 80767, 386, 341),
        2017: (184, 70425, 383, 339),
        2018: (266, 125938, 473, 411),
        2019: (288, 128358, 446, 414),
        2020: (288, 129913, 451, 426),
        2021: (341, 153769, 451, 433),
        2022: (362, 172317, 476, 447),
        2023: (395, 171900, 435, 424),
        2024: (248, 101848, 411, 371),
        2025: (343, 149422, 436, 413),
    }

    from statistics import median

    for year, stats in expected_years.items():
        wcs = by_year[year]
        posts = len(wcs)
        total = sum(wcs)
        mean = round(total / posts)
        med = int(median(wcs))
        assert (posts, total, mean, med) == stats

    appendix = (BOOK_DIR / "appendix-a-by-the-numbers.md").read_text()
    for year, (posts, total, mean_v, med) in expected_years.items():
        total_fmt = f"{total:,}"
        row = f"| {year} | {posts} | {total_fmt} | {mean_v} | {med} |"
        assert row in appendix

    # Era aggregates
    eras = {"Early": (2008, 2012), "Middle": (2013, 2017), "Recent": (2018, 2025)}
    expected_eras = {
        "Early": (1734, 401870, 232),
        "Middle": (968, 287865, 297),
        "Recent": (2531, 1133465, 448),
    }

    for name, (a, b) in eras.items():
        wcs = [r["word_count"] for r in rows if a <= r["year"] <= b]
        posts = len(wcs)
        total = sum(wcs)
        mean = round(total / posts)
        assert (posts, total, mean) == expected_eras[name]


def test_categories_and_multi_category_counts():
    rows = load_posts()
    from collections import Counter

    cat_counts = Counter()
    multi = 0
    for r in rows:
        cats = [c.strip() for c in (r["categories"] or "").split(";") if c.strip()]
        if len(cats) > 1:
            multi += 1
        for c in cats:
            cat_counts[c] += 1

    assert multi == 621

    expected = {
        "Math": 2378,
        "Uncategorized": 996,
        "Computing": 520,
        "Software development": 446,
        "Statistics": 418,
        "Business": 206,
        "Science": 231,
        "Creativity": 161,
        "Python": 177,
        "Music": 85,
        "PowerShell": 47,
        "Typography": 50,
        "Clinical trials": 55,
        "Graphics": 43,
        "Geography": 30,
        "Machine learning": 24,
        "AI": 16,
        "Artificial Intelligence": 13,
    }

    for name, count in expected.items():
        assert cat_counts[name] == count

    appendix = (BOOK_DIR / "appendix-a-by-the-numbers.md").read_text()
    for name, count in expected.items():
        assert f"| {name} | {count:,} |" in appendix


def test_top_tags_and_single_use_tags():
    rows = load_posts()
    from collections import Counter

    tag_counts = Counter()
    for r in rows:
        tags = [t.strip() for t in (r["tags"] or "").split(";") if t.strip()]
        for t in tags:
            tag_counts[t] += 1

    assert len(tag_counts) == 252
    single_use = sum(1 for c in tag_counts.values() if c == 1)
    assert single_use == 79

    appendix = (BOOK_DIR / "appendix-a-by-the-numbers.md").read_text()
    assert "Single-Use Tags" in appendix
    assert "79 tags appear exactly once" in appendix

    # Spot-check a few sample single-use tags
    for tag in [
        "Sage",
        "Leadership",
        "CSS",
        "Neuroplasticity",
        "GPT-5",
        "Ring theory",
    ]:
        assert tag_counts[tag] == 1

    # Check top few tags from Appendix A
    expected_top = {
        "Probability and Statistics": 554,
        "Math": 498,
        "Programming": 342,
        "Number theory": 288,
        "Python": 207,
    }
    for tag, count in expected_top.items():
        assert tag_counts[tag] == count


def test_day_and_hour_distributions():
    rows = load_posts()
    from collections import Counter

    by_dow = Counter()
    by_hour = Counter()
    for r in rows:
        by_dow[r["weekday"]] += 1
        by_hour[r["dt"].hour] += 1

    expected_dow = {
        "Monday": 887,
        "Tuesday": 1003,
        "Wednesday": 938,
        "Thursday": 823,
        "Friday": 561,
        "Saturday": 555,
        "Sunday": 466,
    }

    for day, count in expected_dow.items():
        assert by_dow[day] == count

    appendix = (BOOK_DIR / "appendix-a-by-the-numbers.md").read_text()
    for day, count in expected_dow.items():
        assert f"| {day} | {count:,} |" in appendix

    # Hour of day: just check that the 7 AM peak matches
    assert by_hour[7] == 683
    peak_pct = by_hour[7] / len(rows)
    assert abs(peak_pct - 0.1305) < 1e-3


def test_special_functions_and_languages_tables():
    rows = load_posts()
    from collections import Counter

    # Programming language tags
    tag_counts = Counter()
    for r in rows:
        tags = [t.strip() for t in (r["tags"] or "").split(";") if t.strip()]
        for t in tags:
            tag_counts[t] += 1

    expected_langs = {
        "Python": 207,
        "SciPy": 80,
        "Mathematica": 74,
        "PowerShell": 49,
        "C++": 37,
        "SymPy": 35,
        "Perl": 20,
        "Haskell": 15,
        "Lisp": 10,
        "Rstats": 40,
    }

    for tag, count in expected_langs.items():
        assert tag_counts[tag] == count

    appendix = (BOOK_DIR / "appendix-a-by-the-numbers.md").read_text()
    assert "| Python | 207 |" in appendix
    assert "| SciPy | 80 |" in appendix
    assert "| Mathematica | 74 |" in appendix


def test_extremes_longest_and_shortest_posts():
    rows = load_posts()
    rows_sorted = sorted(rows, key=lambda r: r["word_count"], reverse=True)
    top10 = rows_sorted[:10]
    longest = [(r["date"][:10], r["title"], r["word_count"]) for r in top10]

    assert longest[0][2] == 1926
    assert longest[0][1].startswith("Interview with Sir Michael Atiyah")

    appendix = (BOOK_DIR / "appendix-a-by-the-numbers.md").read_text()
    assert "| 1 | Interview with Sir Michael Atiyah | 2013-09-24 | 1,926 |" in appendix
    assert "| 10 | Probability that a number is prime | 2010-10-06 | 1,390 |" in appendix

    # Shortest
    rows_sorted_min = sorted(rows, key=lambda r: r["word_count"])
    shortest10 = rows_sorted_min[:10]
    assert shortest10[0]["title"] == "Music recommendations"
    assert shortest10[0]["word_count"] == 5


def test_symbol_frequencies():
    # Use precomputed symbol fields where available, plus direct scans for Greek letters
    counts_text = {"π": 0, "∞": 0}
    counts_greek = {"α": 0, "β": 0, "λ": 0, "ε": 0, "ζ": 0}
    sqrt_unicode = 0

    path = DATA_DIR / "johndcook_text_index.jsonl"
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            text = (obj.get("title", "") + "\n" + obj.get("plain_text", ""))
            sym = obj.get("symbols") or {}
            if sym.get("pi", 0) > 0:
                counts_text["π"] += 1
            if sym.get("infty", 0) > 0:
                counts_text["∞"] += 1
            if "√" in text:
                sqrt_unicode += 1
            for g in counts_greek:
                if g in text:
                    counts_greek[g] += 1

    assert counts_text["π"] == 404
    assert counts_text["∞"] == 136
    assert sqrt_unicode == 269
    assert counts_greek == {"α": 108, "β": 83, "λ": 81, "ε": 70, "ζ": 38}

    chapter7 = (BOOK_DIR / "07-edges-of-the-map.md").read_text()
    for sym, count in [("π", 404), ("√", 269), ("∞", 136)]:
        assert f"| {sym} | {count} |" in chapter7


def test_crypto_and_language_timelines():
    rows = load_posts()
    from collections import Counter

    # Crypto: posts tagged Cryptography or Cryptocurrency by year
    crypto_by_year = Counter()
    for r in rows:
        tags = [t.strip() for t in (r["tags"] or "").split(";") if t.strip()]
        if any(t in ("Cryptography", "Cryptocurrency") for t in tags):
            crypto_by_year[r["year"]] += 1

    expected_crypto = {
        2016: 1,
        2017: 5,
        2018: 12,
        2019: 38,
        2020: 6,
        2021: 6,
        2022: 3,
        2023: 18,
        2024: 15,
        2025: 47,
    }
    for year, count in expected_crypto.items():
        assert crypto_by_year[year] == count

    chapter8 = (BOOK_DIR / "08-interviews.md").read_text()
    # Spot-check that the 2019 spike and a couple of rows are present
    assert "| 2018 | 12 |" in chapter8
    assert "| 2019 | 38 |" in chapter8
    assert "| 2025 | 47 |" in chapter8

    # Programming language era counts (tags) for Chapter 6 table
    spans = {"2008-2012": (2008, 2012), "2018-2025": (2018, 2025)}
    langs = ["PowerShell", "Perl", "Python", "Mathematica", "C++"]
    from collections import Counter as C2

    counts = {span: C2() for span in spans}
    for r in rows:
        y = r["year"]
        tags = [t.strip() for t in (r["tags"] or "").split(";") if t.strip()]
        for span, (a, b) in spans.items():
            if a <= y <= b:
                for lang in langs:
                    if lang in tags:
                        counts[span][lang] += 1

    assert counts["2008-2012"]["PowerShell"] == 48
    assert counts["2008-2012"]["Python"] == 77
    assert counts["2018-2025"]["PowerShell"] == 0
    assert counts["2018-2025"]["Mathematica"] == 65


def test_external_stats_prologue_and_ch10():
    # GSC totals
    pages_path = DATA_DIR / "gsc_exports" / "https___www.johndcook.com_-Performance-on-Search-2025-11-28" / "Pages.csv"
    with pages_path.open() as f:
        r = csv.DictReader(f)
        total_clicks = sum(int(row["Clicks"]) for row in r)
    assert total_clicks == 1_017_608

    countries_path = DATA_DIR / "gsc_exports" / "https___www.johndcook.com_-Performance-on-Search-2025-11-28" / "Countries.csv"
    with countries_path.open() as f:
        r = csv.DictReader(f)
        countries = list(r)
    assert len(countries) == 244

    # Check interpolator clicks
    with pages_path.open() as f:
        r = csv.DictReader(f)
        interpolator_clicks = None
        for row in r:
            if row["Top pages"] == "https://www.johndcook.com/interpolator.html":
                interpolator_clicks = int(row["Clicks"])
                break
    assert interpolator_clicks == 605_722

    prologue = (BOOK_DIR / "00-prologue.md").read_text()
    assert "5,881 citations on Google Scholar" in prologue
    assert "Over 1,200 submissions to Hacker News" in prologue
    assert "25,000 upvotes" in prologue
    assert "Seventeen specialized Twitter accounts with 500,000 combined followers" in prologue
    assert "has generated over 600,000 search clicks in sixteen months" in prologue

    # HN facts
    hn_path = DATA_DIR / "hn_facts.csv"
    with hn_path.open() as f:
        rows = list(csv.DictReader(f))
    assert any("1,266 times" in row["fact"] for row in rows)
    assert any("25,486 upvotes" in row["fact"] for row in rows)


def test_2008_year_and_quiet_year_tables():
    rows = load_posts()
    # 2008 stats
    stats_2008 = [r for r in rows if r["year"] == 2008]
    assert len(stats_2008) == 410
    from statistics import mean, median

    mean_2008 = round(mean(r["word_count"] for r in stats_2008))
    med_2008 = int(median(r["word_count"] for r in stats_2008))
    assert mean_2008 == 206
    assert med_2008 == 163

    chapter1 = (BOOK_DIR / "01-shape-of-seventeen-years.md").read_text()
    assert "| 2008 | 410 | 206 |" in chapter1

    # Quiet year table in Chapter 4
    chapter4 = (BOOK_DIR / "04-mathematical-obsessions.md").read_text()
    for year, posts, avg in [
        (2012, 357, 216),
        (2013, 260, 230),
        (2014, 147, 188),
        (2015, 168, 293),
        (2016, 209, 386),
    ]:
        assert f"| {year} | {posts} | {avg} |" in chapter4

    # Check that 2014 is indeed the minimum posts/year
    by_year_posts = {}
    for r in rows:
        by_year_posts.setdefault(r["year"], 0)
        by_year_posts[r["year"]] += 1
    assert min(by_year_posts.values()) == 147


def test_gaps_and_monthly_cv():
    rows = load_posts()
    rows_sorted = sorted(rows, key=lambda r: r["dt"])
    dates = sorted({r["dt"].date() for r in rows_sorted})

    # Longest gap in empty days between posting dates
    gaps = []
    for a, b in zip(dates, dates[1:]):
        gap_days = (b - a).days - 1
        gaps.append((gap_days, a, b))
    max_gap = max(gaps, key=lambda t: t[0])[0]
    assert max_gap == 11
    # Second-longest nonzero gap is 8 days
    assert sum(1 for g in gaps if g[0] == 8) == 3

    # Weekday/weekend ratio and monthly CV
    from collections import Counter

    by_dow = Counter(r["weekday"] for r in rows)
    weekday = sum(by_dow[d] for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    weekend = len(rows) - weekday
    ratio = weekday / weekend
    assert abs(ratio - 4.125) < 1e-3

    months = Counter(r["dt"].month for r in rows)
    counts = [months[m] for m in range(1, 13)]
    mean_m = sum(counts) / len(counts)
    var = sum((c - mean_m) ** 2 for c in counts) / len(counts)
    cv = math.sqrt(var) / mean_m
    assert abs(cv - 0.0636) < 1e-3
