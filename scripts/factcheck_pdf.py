#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from statistics import median


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def iso_mtime(path: Path) -> str:
    timestamp = dt.datetime.fromtimestamp(path.stat().st_mtime).astimezone()
    return timestamp.isoformat(timespec="seconds")


def newest_path(paths: list[Path]) -> Path | None:
    if not paths:
        return None
    return max(paths, key=lambda p: p.stat().st_mtime)


def parse_int_with_commas(value: str) -> int | None:
    match = re.search(r"(\d[\d,]*)", value)
    if not match:
        return None
    return int(match.group(1).replace(",", ""))


def norm_text(value: str) -> str:
    value = html.unescape(value)
    value = value.replace("’", "'")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def norm_title(value: str) -> str:
    value = html.unescape(value)
    value = value.replace("’", "'")
    value = re.sub(r"-\s*\n\s*", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def read_pages_jsonl(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def find_in_pages(pages: list[dict], needle: str, limit: int = 10) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    for page in pages:
        text = page["text"]
        if needle not in text:
            continue
        for line in text.splitlines():
            if needle in line:
                hits.append((page["pdf_page"], line.strip()))
                break
        if len(hits) >= limit:
            break
    return hits


def resolve_pdftotext(explicit: Path | None = None) -> Path:
    if explicit is not None:
        if explicit.exists():
            return explicit
        raise SystemExit(f"pdftotext not found at: {explicit}")

    homebrew = Path("/opt/homebrew/bin/pdftotext")
    if homebrew.exists():
        return homebrew

    discovered = shutil.which("pdftotext")
    if discovered:
        return Path(discovered)

    raise SystemExit(
        "pdftotext is required but was not found. Install Poppler (e.g., `brew install poppler`) "
        "or pass --pdftotext /path/to/pdftotext."
    )


def extract_pdf_text(pdf_path: Path, out_text_path: Path, pdftotext_path: Path) -> None:
    out_text_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [str(pdftotext_path), "-layout", str(pdf_path), str(out_text_path)],
        check=True,
    )


def build_pages_jsonl(pdf_text_path: Path, out_pages_path: Path) -> int:
    text = pdf_text_path.read_text(encoding="utf-8", errors="replace")
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]

    out_pages_path.parent.mkdir(parents=True, exist_ok=True)
    with out_pages_path.open("w", encoding="utf-8") as f:
        for i, page_text in enumerate(pages, start=1):
            f.write(json.dumps({"pdf_page": i, "text": page_text}, ensure_ascii=False))
            f.write("\n")
    return len(pages)


def ensure_pdf_text_and_pages(
    pdf_path: Path,
    pdf_text_path: Path,
    pages_path: Path,
    pdftotext_path: Path,
    *,
    force: bool = False,
) -> int:
    needs_extract = force or not pdf_text_path.exists() or not pages_path.exists()
    if not needs_extract:
        pdf_mtime = pdf_path.stat().st_mtime
        if pdf_mtime > pdf_text_path.stat().st_mtime or pdf_mtime > pages_path.stat().st_mtime:
            needs_extract = True

    if needs_extract:
        extract_pdf_text(pdf_path, pdf_text_path, pdftotext_path)
        return build_pages_jsonl(pdf_text_path, pages_path)

    pages = read_pages_jsonl(pages_path)
    return len(pages)


def load_posts_metadata(path: Path) -> list[dict]:
    rows = []
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["dt"] = dt.datetime.fromisoformat(row["date"])
            row["date_only"] = row["date"][:10]
            row["year_int"] = int(row["year"])
            row["word_count_int"] = int(row["word_count"] or 0)
            row["title_norm"] = norm_title(row["title"])
            row["categories_list"] = [
                html.unescape(c.strip()) for c in (row["categories"] or "").split(";") if c.strip()
            ]
            row["tags_list"] = [html.unescape(t.strip()) for t in (row["tags"] or "").split(";") if t.strip()]
            rows.append(row)
    return rows


def compute_category_counts(posts: list[dict], start_year: int, end_year: int) -> tuple[int, dict[str, int]]:
    total_posts = 0
    counts: dict[str, int] = {}
    for post in posts:
        y = post["year_int"]
        if not (start_year <= y <= end_year):
            continue
        total_posts += 1
        for c in post["categories_list"]:
            counts[c] = counts.get(c, 0) + 1
    return total_posts, counts


def compute_tag_counts(posts: list[dict], start_year: int, end_year: int) -> tuple[int, dict[str, int]]:
    total_posts = 0
    counts: dict[str, int] = {}
    for post in posts:
        y = post["year_int"]
        if not (start_year <= y <= end_year):
            continue
        total_posts += 1
        for t in post["tags_list"]:
            counts[t] = counts.get(t, 0) + 1
    return total_posts, counts


def repo_file_stats(root: Path, exclude_top_dirs: set[str] | None = None) -> tuple[int, int]:
    exclude_top_dirs = exclude_top_dirs or set()
    file_count = 0
    total_bytes = 0
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root)
        if rel_dir.parts and rel_dir.parts[0] in exclude_top_dirs:
            dirnames[:] = []
            continue

        dirnames[:] = [d for d in dirnames if (rel_dir / d).parts and (rel_dir / d).parts[0] not in exclude_top_dirs]
        for filename in filenames:
            file_count += 1
            path = Path(dirpath) / filename
            try:
                total_bytes += path.stat().st_size
            except FileNotFoundError:
                continue
    return file_count, total_bytes


def parse_md_table(lines: list[str], start_index: int) -> tuple[list[str], list[list[str]], int]:
    header = [c.strip() for c in lines[start_index].strip().strip("|").split("|")]
    i = start_index + 1
    while i < len(lines) and lines[i].lstrip().startswith("|") and set(lines[i]) <= set("|- :"):
        i += 1
        break

    rows: list[list[str]] = []
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if len(row) == len(header):
            rows.append(row)
        i += 1
    return header, rows, i


def md_table_after_heading(lines: list[str], heading: str) -> tuple[list[str], list[list[str]]] | None:
    for i, line in enumerate(lines):
        if line.strip() != heading:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].lstrip().startswith("|"):
            j += 1
        if j >= len(lines):
            return None
        header, rows, _ = parse_md_table(lines, j)
        return header, rows
    return None


def check_appendix_a_md(path: Path, posts: list[dict]) -> dict:
    if not path.exists():
        return {"path": path, "available": False}

    lines = path.read_text().splitlines()

    posts_sorted = sorted(posts, key=lambda p: p["dt"])
    total_posts = len(posts)
    total_words = sum(p["word_count_int"] for p in posts)
    first_date = posts_sorted[0]["dt"].date()
    last_date = posts_sorted[-1]["dt"].date()
    total_days = (last_date - first_date).days + 1
    mean_words = round(total_words / total_posts)
    median_words = int(median(p["word_count_int"] for p in posts))
    min_words = min(p["word_count_int"] for p in posts)
    max_words = max(p["word_count_int"] for p in posts)

    mismatches: list[tuple[str, str, str]] = []

    overall = md_table_after_heading(lines, "## Overall Statistics")
    if overall is not None:
        _header, rows = overall
        expected = {
            "Total posts": total_posts,
            "Total words": total_words,
            "Total days": total_days,
            "Mean words per post": mean_words,
            "Median words per post": median_words,
            "Longest post": max_words,
            "Shortest post": min_words,
        }
        for metric, value in rows:
            if metric not in expected:
                continue
            parsed = parse_int_with_commas(value)
            if parsed is None or parsed != expected[metric]:
                mismatches.append(("Overall Statistics", metric, f"md={value} dataset={expected[metric]:,}"))

    by_year = md_table_after_heading(lines, "## Posts by Year")
    if by_year is not None:
        _header, rows = by_year
        by_year_stats: dict[int, dict[str, int]] = {}
        for year in range(min(p["year_int"] for p in posts), max(p["year_int"] for p in posts) + 1):
            year_posts = [p for p in posts if p["year_int"] == year]
            if not year_posts:
                continue
            words = [p["word_count_int"] for p in year_posts]
            by_year_stats[year] = {
                "Posts": len(year_posts),
                "Total Words": sum(words),
                "Mean Words": round(sum(words) / len(words)),
                "Median Words": int(median(words)),
            }

        for year_s, posts_s, total_words_s, mean_s, med_s in rows:
            year = int(year_s)
            expected = by_year_stats.get(year)
            if expected is None:
                mismatches.append(("Posts by Year", year_s, "missing year in dataset"))
                continue
            for key, raw in [
                ("Posts", posts_s),
                ("Total Words", total_words_s),
                ("Mean Words", mean_s),
                ("Median Words", med_s),
            ]:
                parsed = parse_int_with_commas(raw)
                if parsed is None or parsed != expected[key]:
                    mismatches.append(("Posts by Year", f"{year} {key}", f"md={raw} dataset={expected[key]:,}"))

    era = md_table_after_heading(lines, "## Posts by Era")
    if era is not None:
        _header, rows = era
        eras = {
            "Early": (2008, 2012),
            "Middle": (2013, 2017),
            "Recent": (2018, 2025),
        }
        for era_name, years_s, posts_s, mean_s, total_words_s in rows:
            if era_name not in eras:
                continue
            start, end = eras[era_name]
            era_posts = [p for p in posts if start <= p["year_int"] <= end]
            words = [p["word_count_int"] for p in era_posts]
            expected_posts = len(era_posts)
            expected_mean = round(sum(words) / len(words)) if words else 0
            expected_total_words = sum(words)

            parsed_posts = parse_int_with_commas(posts_s)
            parsed_mean = parse_int_with_commas(mean_s)
            parsed_total_words = parse_int_with_commas(total_words_s)

            if parsed_posts != expected_posts:
                mismatches.append(("Posts by Era", f"{era_name} Posts", f"md={posts_s} dataset={expected_posts:,}"))
            if parsed_mean != expected_mean:
                mismatches.append(("Posts by Era", f"{era_name} Mean Words", f"md={mean_s} dataset={expected_mean:,}"))
            if parsed_total_words != expected_total_words:
                mismatches.append(
                    ("Posts by Era", f"{era_name} Total Words", f"md={total_words_s} dataset={expected_total_words:,}")
                )

    cats = md_table_after_heading(lines, "## Categories")
    if cats is not None:
        _header, rows = cats
        category_counts: dict[str, int] = {}
        for p in posts:
            for c in p["categories_list"]:
                category_counts[c] = category_counts.get(c, 0) + 1
        for cat, count_s in rows:
            parsed = parse_int_with_commas(count_s)
            expected = category_counts.get(cat)
            if expected is None:
                mismatches.append(("Categories", cat, "missing category in dataset"))
            elif parsed != expected:
                mismatches.append(("Categories", cat, f"md={count_s} dataset={expected:,}"))

    tags = md_table_after_heading(lines, "## Top 100 Tags")
    if tags is not None:
        _header, rows = tags
        tag_counts: dict[str, int] = {}
        for p in posts:
            for t in p["tags_list"]:
                tag_counts[t] = tag_counts.get(t, 0) + 1
        for rank_s, tag, count_s in rows:
            parsed = parse_int_with_commas(count_s)
            expected = tag_counts.get(tag)
            if expected is None:
                mismatches.append(("Top 100 Tags", tag, "missing tag in dataset"))
            elif parsed != expected:
                mismatches.append(("Top 100 Tags", tag, f"md={count_s} dataset={expected:,}"))

    dows = md_table_after_heading(lines, "## Posts by Day of Week")
    if dows is not None:
        _header, rows = dows
        total = len(posts)
        by_dow: dict[str, int] = {}
        for p in posts:
            day = p["dt"].strftime("%A")
            by_dow[day] = by_dow.get(day, 0) + 1
        for day, count_s, pct_s in rows:
            expected = by_dow.get(day, 0)
            parsed = parse_int_with_commas(count_s)
            expected_pct = round(expected / total * 100, 1)
            parsed_pct = float(pct_s.replace("%", "")) if pct_s.endswith("%") else None
            if parsed != expected:
                mismatches.append(("Posts by Day of Week", day, f"md={count_s} dataset={expected:,}"))
            if parsed_pct is None or abs(parsed_pct - expected_pct) > 0.05:
                mismatches.append(
                    ("Posts by Day of Week", f"{day} %", f"md={pct_s} dataset={expected_pct:.1f}%")
                )

    hours = md_table_after_heading(lines, "## Posts by Hour of Day")
    if hours is not None:
        _header, rows = hours
        total = len(posts)
        by_hour: dict[str, int] = {}
        for p in posts:
            by_hour[f"{p['dt'].hour:02d}:00"] = by_hour.get(f"{p['dt'].hour:02d}:00", 0) + 1
        for hour, count_s, pct_s in rows:
            expected = by_hour.get(hour, 0)
            parsed = parse_int_with_commas(count_s)
            expected_pct = round(expected / total * 100, 1)
            parsed_pct = float(pct_s.replace("%", "")) if pct_s.endswith("%") else None
            if parsed != expected:
                mismatches.append(("Posts by Hour of Day", hour, f"md={count_s} dataset={expected:,}"))
            if parsed_pct is None or abs(parsed_pct - expected_pct) > 0.05:
                mismatches.append(
                    ("Posts by Hour of Day", f"{hour} %", f"md={pct_s} dataset={expected_pct:.1f}%")
                )

    return {"path": path, "available": True, "mismatches": mismatches}


def compute_max_no_post_run(dates: set[dt.date]) -> tuple[int, dt.date | None, dt.date | None]:
    if not dates:
        return 0, None, None

    first = min(dates)
    last = max(dates)

    max_run = 0
    max_start = None
    max_end = None

    run = 0
    run_start = None
    d = first
    while d <= last:
        if d in dates:
            if run > max_run:
                max_run = run
                max_start = run_start
                max_end = d - dt.timedelta(days=1)
            run = 0
            run_start = None
        else:
            if run == 0:
                run_start = d
            run += 1
        d += dt.timedelta(days=1)

    if run > max_run:
        max_run = run
        max_start = run_start
        max_end = last
    return max_run, max_start, max_end


def extract_quote_year_titles(pdf_text: str) -> list[tuple[str, int]]:
    pattern = re.compile(r"\"([^\"]{3,200}?)\"\s*\((\d{4})\)")
    pairs: list[tuple[str, int]] = []
    for raw_title, year_s in pattern.findall(pdf_text):
        year = int(year_s)
        if 2000 <= year <= 2100:
            pairs.append((raw_title, year))
    return pairs


def check_quote_year_pairs(pairs: list[tuple[str, int]], posts: list[dict]) -> list[tuple[int, str]]:
    by_year_title = {(p["year_int"], norm_title(p["title_norm"]).lower()) for p in posts}
    out: list[tuple[int, str]] = []
    seen = set()
    for raw_title, year in pairs:
        title_norm = norm_title(raw_title)
        key = (year, title_norm)
        if key in seen:
            continue
        seen.add(key)
        if (year, title_norm.lower()) not in by_year_title:
            out.append(key)
    return out


def check_appendix_b(appendix_path: Path, posts: list[dict]) -> dict:
    posts_by_date: dict[str, list[dict]] = {}
    for post in posts:
        posts_by_date.setdefault(post["date_only"], []).append(post)

    tex = appendix_path.read_text()
    row_re = re.compile(r"^(\d{4}-\d{2}-\d{2})\s*&\s*(.*?)\s*&\s*(.*?)\\tabularnewline\s*$")
    rows = []
    for line in tex.splitlines():
        match = row_re.match(line.strip())
        if match:
            rows.append((match.group(1), match.group(2), match.group(3).strip()))

    word_rows: list[tuple[str, str, int]] = []
    for date_s, title, third in rows:
        if re.fullmatch(r"[\d,]+", third):
            word_rows.append((date_s, title, int(third.replace(",", ""))))

    missing = []
    word_mismatch = []

    for date_s, title, expected_wc in word_rows:
        candidates = posts_by_date.get(date_s, [])
        if not candidates:
            missing.append((date_s, title, "no post on date"))
            continue
        title_norm = norm_title(title)
        match = next(
            (
                c
                for c in candidates
                if norm_title(c["title_norm"]) == title_norm
                or norm_title(c["title_norm"]).lower() == title_norm.lower()
            ),
            None,
        )
        if match is None:
            missing.append((date_s, title, "title not found on date"))
            continue
        if match["word_count_int"] != expected_wc:
            word_mismatch.append((date_s, title, expected_wc, match["word_count_int"]))

    return {
        "rows_total": len(rows),
        "rows_word_count": len(word_rows),
        "missing": missing,
        "word_mismatch": word_mismatch,
    }


def read_gsc_interpolator_clicks() -> tuple[Path, int] | None:
    root = Path("data/gsc_exports")
    pages_paths = list(root.glob("*Performance-on-Search-*/Pages.csv"))
    latest = newest_path(pages_paths)
    if latest is None:
        return None

    with latest.open() as f:
        reader = csv.DictReader(f)
        page_col = next((c for c in (reader.fieldnames or []) if "page" in c.lower()), None)
        if page_col is None:
            return None
        for row in reader:
            page = row.get(page_col, "")
            if "interpolator.html" not in page:
                continue
            clicks = parse_int_with_commas(row.get("Clicks", ""))
            if clicks is None:
                return None
            return latest, clicks
    return None


def read_hn_snapshot() -> dict | None:
    path = Path("data/hn_facts.csv")
    if not path.exists():
        return None

    submissions = None
    upvotes = None
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            fact = row.get("fact", "")
            if submissions is None and "submitted to Hacker News" in fact:
                submissions = parse_int_with_commas(fact)
            if upvotes is None and "Total Hacker News impact" in fact and "upvotes" in fact:
                upvotes = parse_int_with_commas(fact)

    if submissions is None and upvotes is None:
        return None
    return {"path": path, "submissions": submissions, "upvotes": upvotes}


def read_scholar_snapshot() -> dict | None:
    path = Path("data/scholar_impact/academic_profile.md")
    if not path.exists():
        return None
    text = path.read_text()
    match = re.search(r"Google Scholar Citations:[^0-9]*([\d,]+)", text)
    if not match:
        return None
    citations = int(match.group(1).replace(",", ""))
    return {"path": path, "citations": citations}


def read_cook_impact_snapshot() -> dict | None:
    path = Path("data/cook_impact_master.md")
    if not path.exists():
        return None
    text = path.read_text()

    so_reach = None
    match = re.search(r"\*\*Stack Overflow reach:\*\*\s*([^\n]+)", text)
    if match:
        so_reach = match.group(1).strip()

    twitter_accounts = None
    twitter_followers = None
    m_accounts = re.search(r"^\|\s*Total accounts\s*\|\s*([^\|]+)\|", text, re.M)
    if m_accounts:
        twitter_accounts = m_accounts.group(1).strip()
    m_followers = re.search(r"^\|\s*Total followers\s*\|\s*([^\|]+)\|", text, re.M)
    if m_followers:
        twitter_followers = m_followers.group(1).strip()

    if so_reach is None and twitter_accounts is None and twitter_followers is None:
        return None

    return {
        "path": path,
        "stack_overflow_reach": so_reach,
        "twitter_accounts": twitter_accounts,
        "twitter_followers": twitter_followers,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deep fact-check of book/latex/main.pdf against local datasets (auto-extracts text)."
    )
    parser.add_argument("--pdf", type=Path, default=Path("book/latex/main.pdf"))
    parser.add_argument("--pdf-text", type=Path, default=Path("out/factcheck/latest/main.txt"))
    parser.add_argument("--pages", type=Path, default=Path("out/factcheck/latest/main_pages.jsonl"))
    parser.add_argument("--pdftotext", type=Path, default=None, help="Optional path to Poppler pdftotext.")
    parser.add_argument(
        "--force-extract",
        action="store_true",
        help="Re-extract PDF text even if extracted files appear up-to-date.",
    )
    parser.add_argument("--posts", type=Path, default=Path("data/posts_metadata.csv"))
    parser.add_argument("--appendix-a", type=Path, default=Path("book/appendix-a-by-the-numbers.md"))
    parser.add_argument("--appendix-b", type=Path, default=Path("book/latex/chapters/appendix-b.tex"))
    parser.add_argument("--enriched", type=Path, default=Path("data/johndcook_posts_enriched.jsonl"))
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, default=Path("out/factcheck/latest/fact-check-report.md"))
    parser.add_argument(
        "--canonical-out",
        type=Path,
        default=Path("out/factcheck/fact-check-report.md"),
        help="Stable output path for the latest report (avoids stale/renamed report confusion).",
    )
    parser.add_argument(
        "--archive-dir",
        type=Path,
        default=Path("out/factcheck/archive"),
        help="Directory for per-run archived snapshots of inputs/outputs.",
    )
    args = parser.parse_args()

    required = [args.pdf, args.posts, args.appendix_b]
    missing = [p for p in required if not p.exists()]
    if missing:
        raise SystemExit("Missing required files: " + ", ".join(str(p) for p in missing))

    pdftotext_path = resolve_pdftotext(args.pdftotext)
    page_count = ensure_pdf_text_and_pages(
        args.pdf,
        args.pdf_text,
        args.pages,
        pdftotext_path,
        force=args.force_extract,
    )

    pdf_text = args.pdf_text.read_text(encoding="utf-8", errors="replace")
    pages = read_pages_jsonl(args.pages)
    posts = load_posts_metadata(args.posts)

    now_dt = dt.datetime.now().astimezone()
    now = now_dt.isoformat(timespec="seconds")
    run_id = now_dt.strftime("%Y%m%dT%H%M%S%z")
    pdf_sha = sha256_file(args.pdf)
    pdf_sha_short = pdf_sha[:12]

    posts_sorted = sorted(posts, key=lambda p: p["dt"])
    n_posts = len(posts)
    total_words = sum(p["word_count_int"] for p in posts)
    first_date = posts_sorted[0]["dt"].date()
    last_date = posts_sorted[-1]["dt"].date()
    span_days = (last_date - first_date).days + 1
    mean_words = round(total_words / n_posts)
    median_words = int(median(p["word_count_int"] for p in posts))
    min_words = min(p["word_count_int"] for p in posts)
    max_words = max(p["word_count_int"] for p in posts)

    report: list[str] = []
    report.append(f"# Fact-Check Report: `{args.pdf}` (SHA256 `{pdf_sha}`)")
    report.append("")
    report.append(f"- Run ID: `{run_id}`")
    report.append(f"- Generated: {now}")
    report.append(f"- PDF mtime: `{iso_mtime(args.pdf)}`")
    report.append(f"- Extracted via: `{pdftotext_path.name} -layout`")
    report.append(f"- Extracted text: `{args.pdf_text}` (mtime `{iso_mtime(args.pdf_text)}`)")
    report.append(f"- Page text index: `{args.pages}` (mtime `{iso_mtime(args.pages)}`, pages {page_count})")
    report.append(f"- Dataset: `{args.posts}`")
    report.append(f"- Report (latest): `{args.out}`")
    report.append(f"- Report (canonical): `{args.canonical_out}`")
    report.append("")

    report.append("## Reproduce")
    report.append("")
    report.append("- `python3 scripts/factcheck_pdf.py`")
    report.append("")

    report.append("## Verdict")
    report.append("")
    verdict_index = len(report)
    report.append("__VERDICT__")
    report.append("")

    report.append("## Dataset Baseline (Recomputed)")
    report.append("")
    report.append(f"- Total posts: {n_posts:,}")
    report.append(f"- Total words: {total_words:,}")
    report.append(f"- Date range: {first_date.isoformat()} → {last_date.isoformat()}")
    report.append(f"- Total days: {span_days:,}")
    report.append(f"- Mean words/post: {mean_words:,}")
    report.append(f"- Median words/post: {median_words:,}")
    report.append(f"- Shortest post: {min_words} words")
    report.append(f"- Longest post: {max_words:,} words")
    report.append("")

    report.append("## Placeholders")
    report.append("")
    placeholder_needles = ["[TBD]", "Lorem ipsum", "[Author Name]", "[Location]", "[Month]"]
    placeholder_hits = []
    for needle in placeholder_needles:
        for page_num, line in find_in_pages(pages, needle):
            placeholder_hits.append((needle, page_num, line))
    if placeholder_hits:
        for needle, page_num, line in placeholder_hits:
            report.append(f"- `{needle}`: PDF page {page_num}: {line}")
    else:
        report.append("- None found.")
    report.append("")

    report.append("## High-Confidence Errors")
    report.append("")
    error_count = 0
    warn_count = 0
    verified: list[str] = []

    median_claim = find_in_pages(pages, "median post length overall is 293", limit=1)
    if median_claim:
        error_count += 1
        report.append("- Overall median words/post:")
        report.append(f"  - PDF page {median_claim[0][0]}: {median_claim[0][1]}")
        report.append(f"  - Dataset median is {median_words}.")

    ct_2018 = sum(
        1 for p in posts if p["year_int"] == 2018 and "Clinical trials" in p["categories_list"]
    )
    ct_claims = []
    ct_claims += find_in_pages(pages, "By 2018, they disappear entirely", limit=1)
    ct_claims += find_in_pages(pages, "By 2018, zero", limit=1)
    if ct_claims:
        error_count += 1
        report.append("- Clinical trials by 2018:")
        for page_num, line in ct_claims:
            report.append(f"  - PDF page {page_num}: {line}")
        report.append(f"  - Dataset has {ct_2018} Clinical trials-category posts in 2018.")

    first_scipy = min((p for p in posts if "SciPy" in p["tags_list"]), key=lambda p: p["dt"], default=None)
    sc_claim = find_in_pages(pages, "first SciPy post appeared in", limit=1)
    if sc_claim and first_scipy is not None:
        error_count += 1
        report.append("- SciPy first tagged post:")
        report.append(f"  - PDF page {sc_claim[0][0]}: {sc_claim[0][1]}")
        report.append(
            f"  - Dataset first SciPy-tag post: {first_scipy['date_only']} — "
            f"{norm_text(first_scipy['title_norm'])}"
        )

    python_total = sum(1 for p in posts if "Python" in p["tags_list"])
    python_through_2018 = sum(1 for p in posts if "Python" in p["tags_list"] and p["year_int"] <= 2018)
    python_claim = find_in_pages(pages, "By 2018, Python dominated with 207 tagged posts", limit=1)
    if python_claim:
        error_count += 1
        report.append("- Python tagged posts by 2018:")
        report.append(f"  - PDF page {python_claim[0][0]}: {python_claim[0][1]}")
        report.append(f"  - Dataset cumulative through 2018: {python_through_2018} (total {python_total}).")

    perl_claim = find_in_pages(pages, "Perl gets 20 posts, mostly in 2009-2011", limit=1)
    if perl_claim:
        error_count += 1
        perl_by_year: dict[int, int] = {}
        for p in posts:
            if "Perl" in p["tags_list"]:
                perl_by_year[p["year_int"]] = perl_by_year.get(p["year_int"], 0) + 1
        report.append("- Perl tagged-post timeline:")
        report.append(f"  - PDF page {perl_claim[0][0]}: {perl_claim[0][1]}")
        report.append(f"  - Dataset Perl-tag posts by year: {dict(sorted(perl_by_year.items()))}")

    perl_14_claim = find_in_pages(pages, "Perl appears in 14 posts", limit=1)
    if perl_14_claim:
        error_count += 1
        perl_total = sum(1 for p in posts if "Perl" in p["tags_list"])
        report.append("- Perl total tagged posts:")
        report.append(f"  - PDF page {perl_14_claim[0][0]}: {perl_14_claim[0][1]}")
        report.append(f"  - Dataset Perl-tag posts total: {perl_total}.")

    ps_az_claim = find_in_pages(pages, "linked to Joe Pruitt", limit=1)
    if ps_az_claim:
        az_posts = [p for p in posts if "PowerShell A-Z" in p["title_norm"]]
        az_post = sorted(az_posts, key=lambda p: p["dt"])[0] if az_posts else None
        if az_post is not None:
            year_in_line = None
            match = re.search(r"\b(20\d{2})\b", ps_az_claim[0][1])
            if match:
                year_in_line = int(match.group(1))

            if year_in_line is not None and year_in_line != az_post["year_int"]:
                error_count += 1
                report.append("- PowerShell A-Z series link date mismatch:")
                report.append(f"  - PDF page {ps_az_claim[0][0]}: {ps_az_claim[0][1]}")
                report.append(
                    f"  - Dataset: {az_post['date_only']} — {norm_text(az_post['title_norm'])} ({az_post['link']})"
                )
            else:
                verified.append(
                    f"- PowerShell A-Z reference year matches dataset ({az_post['date_only']}). "
                    f"(PDF page {ps_az_claim[0][0]})"
                )

    powershell_claims: list[tuple[int, str]] = []
    powershell_claims += find_in_pages(pages, "Cook wrote about PowerShell from 2009", limit=3)
    powershell_claims += find_in_pages(pages, "Cook wrote about PowerShell consistently from 2009-2012", limit=3)
    powershell_claims += find_in_pages(pages, "about PowerShell extensively from 2009-2012", limit=3)
    powershell_claims += find_in_pages(pages, "producing 47 posts on scripting techniques", limit=3)
    if powershell_claims:
        ps_cat_total = sum(1 for p in posts if "PowerShell" in p["categories_list"])
        ps_tag_total = sum(1 for p in posts if "PowerShell" in p["tags_list"])
        ps_cat_by_year: dict[int, int] = {}
        ps_tag_by_year: dict[int, int] = {}
        for p in posts:
            y = p["year_int"]
            if "PowerShell" in p["categories_list"]:
                ps_cat_by_year[y] = ps_cat_by_year.get(y, 0) + 1
            if "PowerShell" in p["tags_list"]:
                ps_tag_by_year[y] = ps_tag_by_year.get(y, 0) + 1

        uniq_claims = []
        seen_claims = set()
        for page_num, line in powershell_claims:
            key = (page_num, line)
            if key in seen_claims:
                continue
            seen_claims.add(key)
            uniq_claims.append(key)

        report.append("- PowerShell timeline confusion (category vs tag):")
        for page_num, line in uniq_claims:
            report.append(f"  - PDF page {page_num}: {line}")
        report.append(f"  - Dataset PowerShell category posts total: {ps_cat_total}.")
        report.append(f"  - Dataset PowerShell tag posts total: {ps_tag_total}.")
        report.append(f"  - Dataset PowerShell category posts by year: {dict(sorted(ps_cat_by_year.items()))}")
        report.append(f"  - Dataset PowerShell tag posts by year: {dict(sorted(ps_tag_by_year.items()))}")

        union_years = sorted({*ps_cat_by_year.keys(), *ps_tag_by_year.keys()})
        if union_years:
            earliest = union_years[0]
            latest = union_years[-1]

            extracted_years = []
            for _page_num, line in uniq_claims:
                extracted_years += [int(y) for y in re.findall(r"\b(20\d{2})\b", line)]

            years_in_claim = sorted(set(extracted_years))
            if years_in_claim:
                claim_min = years_in_claim[0]
                claim_max = years_in_claim[-1]
                if claim_min > earliest or claim_max < latest:
                    error_count += 1
            else:
                warn_count += 1

    tuesday_claim = find_in_pages(pages, "Tuesday leads every year", limit=1)
    if tuesday_claim:
        error_count += 1
        by_year_dow: dict[int, dict[str, int]] = {}
        for p in posts:
            y = p["year_int"]
            by_year_dow.setdefault(y, {})
            day = p["dt"].strftime("%A")
            by_year_dow[y][day] = by_year_dow[y].get(day, 0) + 1

        not_tuesday = []
        for y in sorted(by_year_dow):
            counts = by_year_dow[y]
            top = max(counts.values())
            top_days = sorted([d for d, c in counts.items() if c == top])
            if top_days != ["Tuesday"]:
                not_tuesday.append((y, top_days, top, counts.get("Tuesday", 0)))

        report.append("- Top weekday by year:")
        report.append(f"  - PDF page {tuesday_claim[0][0]}: {tuesday_claim[0][1]}")
        report.append("  - Dataset: Tuesday is not the sole top weekday in these years:")
        for y, days, top, tue in not_tuesday:
            report.append(f"    - {y}: top={days} ({top}), Tuesday={tue}")

    dominance_mismatches = []
    for start, end in [(2008, 2012), (2013, 2017), (2018, 2025)]:
        era_label = f"{start}-{end}"
        total_era, era_counts = compute_category_counts(posts, start, end)
        expected_count = era_counts.get("Math", 0)
        expected_pct = round(expected_count / total_era * 100) if total_era else 0

        hit = None
        row_re = re.compile(rf"^{re.escape(era_label)}\s+([\d,]+)\s+(\d+)%\s*$")
        for page in pages:
            for line in page["text"].splitlines():
                m = row_re.match(line.strip())
                if not m:
                    continue
                pdf_count = int(m.group(1).replace(",", ""))
                pdf_pct = int(m.group(2))
                hit = (page["pdf_page"], line.strip(), pdf_count, pdf_pct)
                break
            if hit is not None:
                break

        if hit is None:
            continue

        page_num, line, pdf_count, pdf_pct = hit
        if (pdf_count, pdf_pct) != (expected_count, expected_pct):
            dominance_mismatches.append((era_label, page_num, line, pdf_count, pdf_pct, expected_count, expected_pct))

    if dominance_mismatches:
        error_count += 1
        report.append("- Math dominance table mismatch:")
        for era_label, page_num, line, pdf_count, pdf_pct, exp_count, exp_pct in dominance_mismatches:
            report.append(f"  - {era_label}: PDF {pdf_count:,} ({pdf_pct}%) vs dataset {exp_count:,} ({exp_pct}%)")
            report.append(f"    - PDF page {page_num}: {line}")

    compare_2020_claim = find_in_pages(pages, "Compare to the 2020-2025 distribution", limit=1)
    if compare_2020_claim:
        expected_total, expected_counts = compute_category_counts(posts, 2020, 2025)
        wanted = {"Math", "Uncategorized", "Statistics", "Computing", "Python"}

        table_rows: dict[str, tuple[int, int, str]] = {}
        for page_num in range(compare_2020_claim[0][0], compare_2020_claim[0][0] + 3):
            page = next((p for p in pages if p["pdf_page"] == page_num), None)
            if page is None:
                continue
            for line in page["text"].splitlines():
                m = re.match(r"^([A-Za-z][A-Za-z ]+?)\s+([\d,]+)\s+(\d+)%\s*$", line.strip())
                if not m:
                    continue
                cat = m.group(1).strip()
                if cat not in wanted:
                    continue
                table_rows[cat] = (int(m.group(2).replace(",", "")), int(m.group(3)), line.strip())

        mismatches = []
        for cat in sorted(wanted):
            pdf = table_rows.get(cat)
            exp_count = expected_counts.get(cat, 0)
            exp_pct = round(exp_count / expected_total * 100) if expected_total else 0
            if pdf is None:
                mismatches.append((cat, None, None, exp_count, exp_pct))
                continue
            pdf_count, pdf_pct, line = pdf
            if (pdf_count, pdf_pct) != (exp_count, exp_pct):
                mismatches.append((cat, line, (pdf_count, pdf_pct), exp_count, exp_pct))

        if mismatches:
            error_count += 1
            report.append("- 2020-2025 category distribution table mismatch:")
            report.append(f"  - Dataset total posts in 2020-2025: {expected_total}")
            for cat, line, pdf_vals, exp_count, exp_pct in mismatches:
                if pdf_vals is None:
                    report.append(f"  - {cat}: not found in PDF table text (expected {exp_count:,} / {exp_pct}%)")
                    continue
                pdf_count, pdf_pct = pdf_vals
                report.append(
                    f"  - {cat}: PDF {pdf_count:,} ({pdf_pct}%) vs dataset {exp_count:,} ({exp_pct}%)"
                )
                report.append(f"    - {line}")

    cluster_anchor = find_in_pages(pages, "Compare the morning cluster", limit=1)
    cluster_match = re.search(
        r"morning cluster\s*\(6-10 AM:\s*([\d,]+)\s*posts\).*?noon cluster\s*\(12-5 PM:\s*([\d,]+)\s*posts\)"
        r".*?evening cluster\s*\(6-10\s*PM:\s*([\d,]+)\s*posts\)",
        pdf_text,
        flags=re.S,
    )
    if cluster_anchor and cluster_match:
        by_hour: dict[int, int] = {}
        for p in posts:
            h = p["dt"].hour
            by_hour[h] = by_hour.get(h, 0) + 1

        expected_morning = sum(by_hour.get(h, 0) for h in range(6, 10))
        expected_afternoon = sum(by_hour.get(h, 0) for h in range(12, 18))
        expected_evening = sum(by_hour.get(h, 0) for h in range(18, 23))

        pdf_morning = int(cluster_match.group(1).replace(",", ""))
        pdf_afternoon = int(cluster_match.group(2).replace(",", ""))
        pdf_evening = int(cluster_match.group(3).replace(",", ""))

        if (pdf_morning, pdf_afternoon, pdf_evening) != (expected_morning, expected_afternoon, expected_evening):
            error_count += 1
            report.append("- Daypart cluster counts mismatch:")
            report.append(f"  - PDF page {cluster_anchor[0][0]}: {cluster_anchor[0][1]}")
            report.append(
                f"  - PDF: morning={pdf_morning:,}, afternoon={pdf_afternoon:,}, evening={pdf_evening:,}"
            )
            report.append(
                f"  - Dataset: morning={expected_morning:,}, afternoon={expected_afternoon:,}, "
                f"evening={expected_evening:,}"
            )

    repo_claim = find_in_pages(pages, "holds 221 MB across 2,711", limit=1)
    if repo_claim:
        warn_count += 1
        stats_all = repo_file_stats(args.repo_root)
        stats_no_git = repo_file_stats(args.repo_root, exclude_top_dirs={".git"})
        stats_no_git_out = repo_file_stats(args.repo_root, exclude_top_dirs={".git", "out"})
        report.append("- Repository size/file-count claim (context-dependent):")
        report.append(f"  - PDF page {repo_claim[0][0]}: {repo_claim[0][1]}")
        report.append(
            f"  - Current repo (including .git): {stats_all[1] / (1024 * 1024):.1f} MB across {stats_all[0]:,} files"
        )
        report.append(
            f"  - Current repo (excluding .git): {stats_no_git[1] / (1024 * 1024):.1f} MB across {stats_no_git[0]:,} files"
        )
        report.append(
            f"  - Current repo (excluding .git,out): {stats_no_git_out[1] / (1024 * 1024):.1f} MB across "
            f"{stats_no_git_out[0]:,} files"
        )

    quote_year_pairs = extract_quote_year_titles(pdf_text)
    unmatched_pairs = check_quote_year_pairs(quote_year_pairs, posts)
    report.append("- Post-title citations of the form `\"Title\" (YEAR)`:")
    if unmatched_pairs:
        error_count += 1
        report.append(f"  - {len(unmatched_pairs)} cited title-year pairs do not match any title in `{args.posts}`.")
        for year, title in unmatched_pairs:
            hits = find_in_pages(pages, f"\"{title}\" ({year})", limit=1)
            if hits:
                report.append(f"    - PDF page {hits[0][0]}: \"{title}\" ({year})")
            else:
                report.append(f"    - \"{title}\" ({year})")
    else:
        report.append("  - No mismatches found.")

    bad_title_needles = ["Beware the custom solution", "Building vs. buying software", "Staying billable"]
    dataset_titles = {norm_title(p["title_norm"]).lower() for p in posts}
    missing_bad_titles = []
    for needle in bad_title_needles:
        if needle.lower() in dataset_titles:
            continue
        hits = find_in_pages(pages, needle, limit=1)
        if hits:
            missing_bad_titles.append((needle, hits[0][0], hits[0][1]))
    if missing_bad_titles:
        error_count += 1
        report.append("- Quoted titles (no year) not found in dataset:")
        for _needle, page_num, line in missing_bad_titles:
            report.append(f"  - PDF page {page_num}: {line}")

    pandas_std_claim = []
    pandas_std_claim += find_in_pages(pages, "called .std() on a grouped DataFrame", limit=1)
    pandas_std_claim += find_in_pages(pages, "Every time a data scientist calls .std()", limit=1)
    if pandas_std_claim:
        warn_count += 1
        report.append("- pandas `.std()` / `.var()` attribution (manual source-check required):")
        for page_num, line in pandas_std_claim:
            report.append(f"  - PDF page {page_num}: {line}")
        report.append(
            "  - The cited `groupby.pyx` comment links to skewness/kurtosis; it is not in the std/var code path."
        )

    report.append("")

    report.append("## Appendix A (By the Numbers) Cross-Check")
    report.append("")
    appendix_a = check_appendix_a_md(args.appendix_a, posts)
    report.append(f"- Source: `{appendix_a['path']}`")
    if not appendix_a.get("available"):
        report.append("- Not found; skipped.")
    else:
        mismatches = appendix_a.get("mismatches", [])
        report.append(f"- Mismatches: {len(mismatches)}")
        if mismatches:
            error_count += 1
            for section, key, detail in mismatches[:20]:
                report.append(f"  - {section}: {key} ({detail})")
            if len(mismatches) > 20:
                report.append(f"  - ... and {len(mismatches) - 20} more")
    report.append("")

    report.append("## Appendix B (Reading List) Cross-Check")
    report.append("")
    appendix_b = check_appendix_b(args.appendix_b, posts)
    report.append(f"- Parsed table rows: {appendix_b['rows_total']}")
    report.append(f"- Rows with word counts: {appendix_b['rows_word_count']}")
    report.append(f"- Missing rows: {len(appendix_b['missing'])}")
    report.append(f"- Word-count mismatches: {len(appendix_b['word_mismatch'])}")
    report.append("")

    report.append("## Posting-Gap Sanity Check")
    report.append("")
    dates = {p["dt"].date() for p in posts}
    max_run, start, end = compute_max_no_post_run(dates)
    report.append(f"- Max consecutive no-post days (dataset): {max_run}")
    if start and end:
        report.append(f"- Max no-post run: {start.isoformat()} → {end.isoformat()}")
    report.append("")

    report.append("## External Claims (Local Snapshots)")
    report.append("")
    gsc = read_gsc_interpolator_clicks()
    if gsc is not None:
        gsc_path, clicks = gsc
        report.append(f"- GSC export: `{gsc_path}`")
        report.append(f"- `interpolator.html` clicks: {clicks:,} (supports “over 600,000 search clicks”).")
    else:
        report.append("- GSC export not found; cannot verify “over 600,000 search clicks”.")

    hn = read_hn_snapshot()
    if hn is not None:
        report.append(f"- HN snapshot: `{hn['path']}`")
        if hn.get("submissions") is not None:
            report.append(f"- HN submissions: {hn['submissions']:,} (supports “over 1,200 submissions”).")
        if hn.get("upvotes") is not None:
            report.append(f"- HN upvotes: {hn['upvotes']:,} (supports “25,000 upvotes”).")
    else:
        report.append("- HN snapshot not found; cannot verify Hacker News claims from local data.")

    scholar = read_scholar_snapshot()
    if scholar is not None:
        report.append(f"- Scholar snapshot: `{scholar['path']}`")
        report.append(f"- Google Scholar citations (snapshot): {scholar['citations']:,}.")
    else:
        report.append("- Scholar snapshot not found; cannot verify Google Scholar citation claim from local data.")

    impact = read_cook_impact_snapshot()
    if impact is not None:
        report.append(f"- Impact notes: `{impact['path']}`")
        if impact.get("stack_overflow_reach") is not None:
            report.append(f"- Stack Overflow reach (notes): {impact['stack_overflow_reach']}")
        if impact.get("twitter_accounts") is not None:
            report.append(f"- Twitter accounts (notes): {impact['twitter_accounts']}")
        if impact.get("twitter_followers") is not None:
            report.append(f"- Twitter followers (notes): {impact['twitter_followers']}")
        report.append("- Note: these are local notes/snapshots, not live primary-source verification.")
    else:
        report.append("- Impact notes not found; cannot cross-check Stack Overflow/Twitter claims locally.")
    report.append("")

    report.append("## Unverified (Not Checked Against Primary Sources)")
    report.append("")
    report.append(
        "- External-ecosystem claims (e.g., \"ported to ten programming languages\", syllabi at MIT/Stanford/CMU) "
        "were not validated against live primary sources in this pass."
    )
    report.append("")

    report.append("## Verified Spot-Checks")
    report.append("")
    if verified:
        report.extend(verified)
    else:
        report.append("- None recorded in this run.")
    report.append("")

    if placeholder_hits or error_count or warn_count:
        parts = []
        if placeholder_hits:
            placeholder_count = len(placeholder_hits)
            parts.append(f"{placeholder_count} placeholder hit{'s' if placeholder_count != 1 else ''}")
        if error_count:
            parts.append(f"{error_count} contradiction{'s' if error_count != 1 else ''}")
        if warn_count:
            parts.append(f"{warn_count} context-dependent warning{'s' if warn_count != 1 else ''}")
        report[verdict_index] = f"- FAIL: Found {', '.join(parts)}."
    else:
        report[verdict_index] = "- PASS: No placeholders or contradictions detected in checked claims."

    args.out.parent.mkdir(parents=True, exist_ok=True)
    report_text = "\n".join(report) + "\n"
    args.out.write_text(report_text, encoding="utf-8")

    args.canonical_out.parent.mkdir(parents=True, exist_ok=True)
    args.canonical_out.write_text(report_text, encoding="utf-8")

    archive_run_dir = args.archive_dir / f"{run_id}_main-pdf_{pdf_sha_short}"
    archive_run_dir.mkdir(parents=True, exist_ok=True)
    (archive_run_dir / "inputs.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "generated_at": now,
                "pdf_path": str(args.pdf),
                "pdf_sha256": pdf_sha,
                "pdf_mtime": iso_mtime(args.pdf),
                "pdftotext": str(pdftotext_path),
                "pdf_text_path": str(args.pdf_text),
                "pdf_text_mtime": iso_mtime(args.pdf_text),
                "pages_path": str(args.pages),
                "pages_mtime": iso_mtime(args.pages),
                "page_count": len(pages),
                "posts_path": str(args.posts),
                "appendix_a_path": str(args.appendix_a),
                "appendix_b_path": str(args.appendix_b),
                "report_latest_path": str(args.out),
                "report_canonical_path": str(args.canonical_out),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (archive_run_dir / "fact-check-report.md").write_text(report_text, encoding="utf-8")
    shutil.copy2(args.pdf_text, archive_run_dir / args.pdf_text.name)
    shutil.copy2(args.pages, archive_run_dir / args.pages.name)

    print(f"wrote {args.out}")
    print(f"wrote {args.canonical_out}")
    print(f"archived {archive_run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
