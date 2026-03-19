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


MONTH_TO_NUM = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


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


def parse_month_day_year(value: str) -> dt.date | None:
    match = re.search(r"([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})", value)
    if not match:
        return None
    month = MONTH_TO_NUM.get(match.group(1).lower())
    if month is None:
        return None
    day = int(match.group(2))
    year = int(match.group(3))
    try:
        return dt.date(year, month, day)
    except ValueError:
        return None


def join_wrapped_parts(parts: list[str]) -> str:
    out = ""
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if out.endswith("-") and part and part[0].islower():
            out = out[:-1] + part
        elif out.endswith("-"):
            out = out + " " + part
        elif out:
            out += " " + part
        else:
            out = part
    return re.sub(r"\s+", " ", out).strip()


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


def normalize_space(value: str) -> str:
    value = value.replace("\f", "")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def is_page_number_line(value: str) -> bool:
    return bool(re.fullmatch(r"\d{1,4}", value.strip()))


def detect_boilerplate_lines(pages: list[dict], min_page_hits: int = 10) -> set[str]:
    line_to_pages: dict[str, set[int]] = {}
    for page in pages:
        page_num = int(page["pdf_page"])
        for raw in page.get("text", "").splitlines():
            line = normalize_space(raw)
            if not line or is_page_number_line(line):
                continue
            line_to_pages.setdefault(line, set()).add(page_num)
    return {line for line, hits in line_to_pages.items() if len(hits) >= min_page_hits}


def extract_prose_paragraphs(pages: list[dict], boilerplate_lines: set[str]) -> list[dict]:
    paragraphs: list[dict] = []
    for page in pages:
        page_num = int(page["pdf_page"])
        buf: list[str] = []
        idx = 0
        for raw in page.get("text", "").splitlines():
            line = raw.replace("\f", "").rstrip()
            line_norm = normalize_space(line)
            if not line_norm:
                if buf:
                    paragraphs.append(
                        {"pdf_page": page_num, "index": idx, "text": join_wrapped_parts(buf)}
                    )
                    idx += 1
                    buf = []
                continue
            if is_page_number_line(line_norm):
                continue
            if line_norm in boilerplate_lines:
                continue
            buf.append(line_norm)
        if buf:
            paragraphs.append({"pdf_page": page_num, "index": idx, "text": join_wrapped_parts(buf)})
    return paragraphs


def normalize_for_compare(value: str) -> str:
    value = norm_text(value).lower()
    value = re.sub(r"[^a-z0-9']+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def split_sentences(text: str) -> list[str]:
    text = norm_text(text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def alpha_ratio(text: str) -> float:
    if not text:
        return 0.0
    letters = sum(1 for ch in text if ch.isalpha())
    return letters / len(text)


def digit_ratio(text: str) -> float:
    if not text:
        return 0.0
    digits = sum(1 for ch in text if ch.isdigit())
    return digits / len(text)


def is_probably_prose(text: str) -> bool:
    text = text.strip()
    if len(text) < 40:
        return False
    if re.search(r"\b20\d{2}-\d{2}-\d{2}\b", text):
        return False
    if "\\begin{" in text or "\\end{" in text:
        return False
    if text.count("\\") >= 2:
        return False
    if digit_ratio(text) > 0.12:
        return False
    headerish = bool(re.search(r"\b(Year|Era|Rank|Date)\b", text) and re.search(r"\b(Posts|Words)\b", text))
    if headerish:
        return False
    return True


def find_duplicate_paragraphs(paragraphs: list[dict], min_chars: int = 160) -> list[dict]:
    buckets: dict[str, list[dict]] = {}
    for para in paragraphs:
        text = para["text"]
        if len(text) < min_chars or alpha_ratio(text) < 0.6:
            continue
        key = normalize_for_compare(text)
        if len(key) < min_chars:
            continue
        buckets.setdefault(key, []).append(para)

    out: list[dict] = []
    for key, occs in buckets.items():
        if len(occs) <= 1:
            continue
        pages = sorted({o["pdf_page"] for o in occs})
        out.append({"text": occs[0]["text"], "count": len(occs), "pages": pages})

    out.sort(key=lambda item: (-item["count"], -len(item["text"])))
    return out


def find_repeated_sentences(paragraphs: list[dict], min_chars: int = 120) -> list[dict]:
    buckets: dict[str, list[tuple[int, str]]] = {}
    for para in paragraphs:
        page_num = int(para["pdf_page"])
        for sentence in split_sentences(para["text"]):
            if len(sentence) < min_chars or alpha_ratio(sentence) < 0.7:
                continue
            key = normalize_for_compare(sentence)
            if len(key) < min_chars:
                continue
            buckets.setdefault(key, []).append((page_num, sentence))

    out: list[dict] = []
    for key, occs in buckets.items():
        pages = sorted({p for p, _ in occs})
        if len(pages) <= 1:
            continue
        out.append({"text": occs[0][1], "count_pages": len(pages), "pages": pages})

    out.sort(key=lambda item: (-item["count_pages"], -len(item["text"])))
    return out


def find_double_words(paragraphs: list[dict]) -> list[dict]:
    double_re = re.compile(r"\b([A-Za-z]{2,})\s+\1\b", flags=re.I)
    findings: list[dict] = []
    seen = set()
    for para in paragraphs:
        page_num = int(para["pdf_page"])
        text = para["text"]
        for match in double_re.finditer(text):
            word = match.group(1).lower()
            start = max(0, match.start() - 60)
            end = min(len(text), match.end() + 60)
            context = text[start:end].strip()
            key = (page_num, word, context)
            if key in seen:
                continue
            seen.add(key)
            findings.append({"pdf_page": page_num, "word": word, "context": context})
    findings.sort(key=lambda item: (item["pdf_page"], item["word"]))
    return findings


def variant_regex(variant: str) -> re.Pattern[str]:
    if re.fullmatch(r"[A-Za-z0-9']+", variant):
        return re.compile(rf"\b{re.escape(variant)}\b")
    return re.compile(re.escape(variant))


def find_term_variant_mix(pages: list[dict], full_text: str) -> list[dict]:
    groups = [
        {"name": "LaTeX", "canonical": "LaTeX", "variants": ["Latex", "latex"]},
        {"name": "SciPy", "canonical": "SciPy", "variants": ["Scipy", "scipy"]},
        {
            "name": "PowerShell",
            "canonical": "PowerShell",
            "variants": ["Powershell", "powershell", "Power Shell", "power shell"],
        },
        {"name": "GitHub", "canonical": "GitHub", "variants": ["Github", "github"]},
        {
            "name": "Stack Overflow",
            "canonical": "Stack Overflow",
            "variants": ["StackOverflow", "Stackoverflow"],
        },
        {"name": "Hacker News", "canonical": "Hacker News", "variants": ["Hackernews"]},
        {"name": "JohnDCook.com", "canonical": "JohnDCook.com", "variants": ["John D Cook"]},
        {"name": "PowerShell A-Z", "canonical": "A-Z", "variants": ["A–Z", "A—Z"]},
    ]

    findings: list[dict] = []
    for group in groups:
        canonical = group["canonical"]
        variants = group["variants"]
        counts: dict[str, int] = {}

        all_forms = [canonical, *variants]
        for form in all_forms:
            counts[form] = len(variant_regex(form).findall(full_text))

        present = [form for form, count in counts.items() if count > 0]
        if len(present) <= 1:
            continue

        examples: dict[str, list[tuple[int, str]]] = {}
        for form in variants:
            if counts.get(form, 0) <= 0:
                continue
            examples[form] = find_in_pages(pages, form, limit=3)
        findings.append(
            {
                "name": group["name"],
                "canonical": canonical,
                "counts": counts,
                "examples": examples,
            }
        )
    return findings


def find_inconsistent_numeric_lines(pages: list[dict], boilerplate_lines: set[str]) -> list[dict]:
    keywords = (
        "percent",
        "total",
        "median",
        "mean",
        "average",
        "posts",
        "words",
        "days",
        "tag",
        "tags",
        "category",
        "categories",
        "citations",
        "followers",
        "upvotes",
        "submissions",
        "million",
    )
    num_re = re.compile(r"\d[\d,]*(?:\.\d+)?")
    buckets: dict[str, list[tuple[int, str]]] = {}
    for page in pages:
        page_num = int(page["pdf_page"])
        for raw in page.get("text", "").splitlines():
            line = normalize_space(raw)
            if not line or is_page_number_line(line) or line in boilerplate_lines:
                continue
            lower = line.lower()
            if not any(k in lower for k in keywords):
                continue
            if not num_re.search(line):
                continue
            if re.match(r"^(Figure|Table|Chapter)\b", line):
                continue
            if re.match(r"^\d{2}:\d{2}\s+[0-9,]+\s+\d+(\.\d+)?%$", line):
                continue
            if re.match(r"^\d+\s+(AM|PM)\s+[0-9,]+\s+\d+(\.\d+)?%$", line, flags=re.I):
                continue
            if re.match(r"^\d{4}-\d{4}\s+[0-9,]+\s+\d+%$", line):
                continue
            if lower.startswith("post #"):
                continue
            if lower.startswith("category posts"):
                continue
            if re.match(r"^(math|statistics|computing|uncategorized)\s+[0-9,]+\s+\d+%$", lower):
                continue
            template = num_re.sub("#", lower)
            buckets.setdefault(template, []).append((page_num, line))

    inconsistencies: list[dict] = []
    for template, occs in buckets.items():
        if len(occs) <= 1:
            continue
        variants = {}
        for page_num, line in occs:
            variants.setdefault(line, []).append(page_num)
        if len(variants) <= 1:
            continue
        samples = sorted(variants.items(), key=lambda item: (-len(item[1]), item[0]))
        inconsistencies.append(
            {
                "template": template,
                "variants": [
                    {"text": text, "pages": sorted(set(pages_list))} for text, pages_list in samples
                ],
            }
        )

    inconsistencies.sort(key=lambda item: (-len(item["variants"]), item["template"]))
    return inconsistencies


def build_prose_consistency_report(
    pages: list[dict],
    pdf_path: Path,
    pdf_sha: str,
    now: str,
    run_id: str,
    pdf_text_path: Path,
    pages_path: Path,
    n_posts: int,
    total_words: int,
    span_days: int,
    mean_words: int,
    median_words: int,
) -> dict:
    boilerplate_lines = detect_boilerplate_lines(pages, min_page_hits=max(10, len(pages) // 10))
    paragraphs = extract_prose_paragraphs(pages, boilerplate_lines)
    prose_paragraphs = [p for p in paragraphs if is_probably_prose(p["text"])]
    duplicates = find_duplicate_paragraphs(prose_paragraphs)
    repeated_sentences = find_repeated_sentences(prose_paragraphs)
    double_words = find_double_words(prose_paragraphs)

    full_text = "\n".join(page.get("text", "") for page in pages)
    term_variants = find_term_variant_mix(pages, full_text)
    numeric_inconsistencies = find_inconsistent_numeric_lines(pages, boilerplate_lines)

    report: list[str] = []
    report.append(f"# Consistency & Prose Report: `{pdf_path}` (SHA256 `{pdf_sha}`)")
    report.append("")
    report.append(f"- Run ID: `{run_id}`")
    report.append(f"- Generated: {now}")
    report.append(f"- Extracted text: `{pdf_text_path}`")
    report.append(f"- Page text index: `{pages_path}`")
    report.append("")
    report.append(
        "- Note: This pass is heuristic and runs on extracted PDF text; line wrapping can create false positives."
    )
    report.append("")

    report.append("## Summary")
    report.append("")
    report.append(f"- Baseline (dataset): {n_posts:,} posts, {total_words:,} words, {span_days:,} days")
    report.append(f"- Mean/median words per post: {mean_words} / {median_words}")
    report.append(f"- Duplicate long paragraphs: {len(duplicates)}")
    report.append(f"- Repeated long sentences: {len(repeated_sentences)}")
    report.append(f"- Possible doubled-word typos: {len(double_words)}")
    report.append(f"- Mixed term/casing variants: {len(term_variants)}")
    report.append(f"- Potential inconsistent numeric lines: {len(numeric_inconsistencies)}")
    report.append("")

    report.append("## Duplicate Paragraphs")
    report.append("")
    if not duplicates:
        report.append("- None detected (excluding headers/footers and table/code blocks).")
    else:
        for item in duplicates[:50]:
            snippet = item["text"][:160].rstrip()
            pages_s = ", ".join(str(p) for p in item["pages"][:15])
            suffix = "" if len(item["pages"]) <= 15 else f", … (+{len(item['pages']) - 15})"
            report.append(f"- ({item['count']}x) pages {pages_s}{suffix}: {snippet}")
        if len(duplicates) > 50:
            report.append(f"- ... and {len(duplicates) - 50} more")
    report.append("")

    report.append("## Repeated Sentences")
    report.append("")
    if not repeated_sentences:
        report.append("- None detected (excluding headers/footers and table/code blocks).")
    else:
        for item in repeated_sentences[:75]:
            snippet = item["text"][:160].rstrip()
            pages_s = ", ".join(str(p) for p in item["pages"][:20])
            suffix = "" if len(item["pages"]) <= 20 else f", … (+{len(item['pages']) - 20})"
            report.append(f"- ({item['count_pages']} pages) {pages_s}{suffix}: {snippet}")
        if len(repeated_sentences) > 75:
            report.append(f"- ... and {len(repeated_sentences) - 75} more")
    report.append("")

    report.append("## Doubled Words")
    report.append("")
    if not double_words:
        report.append("- None detected.")
    else:
        for item in double_words[:100]:
            report.append(f"- PDF page {item['pdf_page']}: {item['context']}")
        if len(double_words) > 100:
            report.append(f"- ... and {len(double_words) - 100} more")
    report.append("")

    report.append("## Term/Casing Consistency")
    report.append("")
    if not term_variants:
        report.append("- No mixed variants detected for the monitored terms.")
    else:
        for item in term_variants:
            report.append(f"- {item['name']}:")
            counts = item["counts"]
            present = [f"{k}={v}" for k, v in counts.items() if v]
            report.append(f"  - counts: {', '.join(present)}")
            for variant, examples in item["examples"].items():
                if not examples:
                    continue
                for page_num, line in examples:
                    report.append(f"  - example {variant} (PDF page {page_num}): {line}")
    report.append("")

    report.append("## Potential Inconsistent Numeric Lines")
    report.append("")
    if not numeric_inconsistencies:
        report.append("- None detected (after excluding obvious table rows and figure/table labels).")
    else:
        for item in numeric_inconsistencies[:50]:
            report.append(f"- Template: {item['template']}")
            for variant in item["variants"][:5]:
                pages_s = ", ".join(str(p) for p in variant["pages"][:15])
                suffix = "" if len(variant["pages"]) <= 15 else f", … (+{len(variant['pages']) - 15})"
                report.append(f"  - pages {pages_s}{suffix}: {variant['text']}")
            if len(item["variants"]) > 5:
                report.append(f"  - ... and {len(item['variants']) - 5} more variants")
        if len(numeric_inconsistencies) > 50:
            report.append(f"- ... and {len(numeric_inconsistencies) - 50} more")
    report.append("")

    return {
        "report_text": "\n".join(report) + "\n",
        "summary": {
            "duplicate_paragraphs": len(duplicates),
            "repeated_sentences": len(repeated_sentences),
            "double_words": len(double_words),
            "term_variant_groups": len(term_variants),
            "numeric_inconsistencies": len(numeric_inconsistencies),
        },
    }


def find_in_pages(pages: list[dict], needle: str, limit: int = 10) -> list[tuple[int, str]]:
    """
    Locate a phrase in the extracted PDF page text.

    `pdftotext -layout` frequently inserts hard line breaks mid-sentence, so we
    search in a whitespace-normalized view of each page to allow matches across
    line wraps.
    """

    needle_norm = norm_text(needle).replace("“", '"').replace("”", '"')
    needle_norm = normalize_space(needle_norm)
    if not needle_norm:
        return []

    hits: list[tuple[int, str]] = []
    for page in pages:
        haystack_norm = norm_text(page["text"]).replace("“", '"').replace("”", '"')
        haystack_norm = normalize_space(haystack_norm)

        idx = haystack_norm.find(needle_norm)
        if idx < 0:
            continue

        start = max(0, idx - 80)
        end = min(len(haystack_norm), idx + len(needle_norm) + 80)
        snippet = haystack_norm[start:end].strip()
        hits.append((page["pdf_page"], snippet))
        if len(hits) >= limit:
            break

    return hits


def resolve_pdftotext(explicit: Path | None = None) -> Path | None:
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

    return None


def extract_pdf_text_pdftotext(pdf_path: Path, out_text_path: Path, pdftotext_path: Path) -> str | None:
    out_text_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_text_path.with_suffix(out_text_path.suffix + ".tmp")
    try:
        result = subprocess.run(
            [str(pdftotext_path), "-layout", str(pdf_path), str(tmp_path)],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        return str(exc)

    if result.returncode != 0:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        err = (result.stderr or "").strip()
        if not err:
            err = f"pdftotext exited with code {result.returncode}"
        return err

    tmp_path.replace(out_text_path)
    return None


def extract_pdf_text_pypdf2(pdf_path: Path) -> tuple[list[str], str | None]:
    try:
        from PyPDF2 import PdfReader  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        return [], f"PyPDF2 not available: {exc}"

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:  # noqa: BLE001
        return [], f"PyPDF2 failed to read PDF: {exc}"

    out_pages: list[str] = []
    for page in reader.pages:
        try:
            out_pages.append(page.extract_text() or "")
        except Exception:  # noqa: BLE001
            out_pages.append("")
    return out_pages, None


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


def write_pages_jsonl(pages: list[str], out_pages_path: Path) -> None:
    out_pages_path.parent.mkdir(parents=True, exist_ok=True)
    with out_pages_path.open("w", encoding="utf-8") as f:
        for i, page_text in enumerate(pages, start=1):
            f.write(json.dumps({"pdf_page": i, "text": page_text}, ensure_ascii=False))
            f.write("\n")


def write_pages_text(pages: list[str], out_text_path: Path) -> None:
    out_text_path.parent.mkdir(parents=True, exist_ok=True)
    out_text_path.write_text("\f".join(pages) + "\f", encoding="utf-8")


def ensure_pdf_text_and_pages(
    pdf_path: Path,
    pdf_text_path: Path,
    pages_path: Path,
    *,
    pdftotext_path: Path | None = None,
    force: bool = False,
) -> tuple[int, str, str | None]:
    needs_extract = force or not pdf_text_path.exists() or not pages_path.exists()
    if not needs_extract:
        pdf_mtime = pdf_path.stat().st_mtime
        if pdf_mtime > pdf_text_path.stat().st_mtime or pdf_mtime > pages_path.stat().st_mtime:
            needs_extract = True

    if needs_extract:
        if pdftotext_path is not None:
            error = extract_pdf_text_pdftotext(pdf_path, pdf_text_path, pdftotext_path)
            if error is None:
                page_count = build_pages_jsonl(pdf_text_path, pages_path)
                return page_count, "pdftotext -layout", None

            pages, fallback_error = extract_pdf_text_pypdf2(pdf_path)
            if fallback_error is None and pages:
                write_pages_text(pages, pdf_text_path)
                write_pages_jsonl(pages, pages_path)
                return len(pages), "PyPDF2", f"pdftotext failed: {error}"

            raise SystemExit(f"Failed to extract PDF text. pdftotext error: {error}. PyPDF2 error: {fallback_error}")

        pages, fallback_error = extract_pdf_text_pypdf2(pdf_path)
        if fallback_error is None and pages:
            write_pages_text(pages, pdf_text_path)
            write_pages_jsonl(pages, pages_path)
            return len(pages), "PyPDF2", None
        raise SystemExit(f"Failed to extract PDF text via PyPDF2: {fallback_error}")

    pages = read_pages_jsonl(pages_path)
    return len(pages), "existing", None


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


def find_page_containing(pages: list[dict], needle: str, *, start_page: int = 1) -> int | None:
    for page in pages:
        if page["pdf_page"] < start_page:
            continue
        if needle in page["text"]:
            return page["pdf_page"]
    return None


def join_pages_text(pages: list[dict], start_page: int, end_page_inclusive: int | None = None) -> str:
    chunks = []
    for page in pages:
        if page["pdf_page"] < start_page:
            continue
        if end_page_inclusive is not None and page["pdf_page"] > end_page_inclusive:
            break
        chunks.append(page["text"])
    return "\n".join(chunks)


def parse_pdf_appendix_a_tables(pdf_text: str) -> dict:
    lines = [line.replace("\f", "").rstrip() for line in pdf_text.splitlines()]
    idx_overall = next((i for i, line in enumerate(lines) if line.strip() == "Overall Statistics"), None)
    idx_by_year = next((i for i, line in enumerate(lines) if line.strip() == "Posts by Year"), None)
    idx_by_era = next((i for i, line in enumerate(lines) if line.strip() == "Posts by Era"), None)
    idx_categories = next((i for i, line in enumerate(lines) if line.strip() == "Categories"), None)
    idx_top_tags = next((i for i, line in enumerate(lines) if line.strip() == "Top 100 Tags"), None)
    idx_by_dow = next((i for i, line in enumerate(lines) if line.strip() == "Posts by Day of Week"), None)
    idx_by_hour = next((i for i, line in enumerate(lines) if line.strip() == "Posts by Hour of Day"), None)
    idx_extremes = next((i for i, line in enumerate(lines) if line.strip() == "Extremes"), None)
    idx_single_use = next((i for i, line in enumerate(lines) if line.strip() == "Single-Use Tags"), None)
    idx_key_dates = next((i for i, line in enumerate(lines) if line.strip() == "Key Dates"), None)
    idx_programming = next((i for i, line in enumerate(lines) if line.strip() == "Programming Languages"), None)
    idx_special_titles = next((i for i, line in enumerate(lines) if line.strip() == "Special Functions in Titles"), None)

    return {
        "lines": lines,
        "idx_overall": idx_overall,
        "idx_by_year": idx_by_year,
        "idx_by_era": idx_by_era,
        "idx_categories": idx_categories,
        "idx_top_tags": idx_top_tags,
        "idx_by_dow": idx_by_dow,
        "idx_by_hour": idx_by_hour,
        "idx_extremes": idx_extremes,
        "idx_single_use": idx_single_use,
        "idx_key_dates": idx_key_dates,
        "idx_programming": idx_programming,
        "idx_special_titles": idx_special_titles,
    }


def check_appendix_a_pdf(pdf_text: str, posts: list[dict]) -> dict:
    parsed = parse_pdf_appendix_a_tables(pdf_text)
    lines: list[str] = parsed["lines"]
    mismatches: list[str] = []

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
    expected_avg_posts_per_day = round(total_posts / total_days, 2)
    expected_avg_days_between = round(total_days / total_posts, 2)

    idx_overall = parsed["idx_overall"]
    if idx_overall is None:
        mismatches.append("Missing 'Overall Statistics' heading in PDF appendix.")
    else:
        overall_block = "\n".join(lines[idx_overall : idx_overall + 60])
        kv_patterns: list[tuple[str, int | float | dt.date | tuple[dt.date, dt.date]]] = [
            ("Total posts", total_posts),
            ("Total words", total_words),
            ("Total days", total_days),
            ("Mean words per post", mean_words),
            ("Median words per post", median_words),
            ("Longest post", max_words),
            ("Shortest post", min_words),
        ]
        for key, expected in kv_patterns:
            m = re.search(rf"{re.escape(key)}\s+([0-9][0-9,]*)", overall_block)
            if not m:
                mismatches.append(f"Overall Statistics: missing '{key}' row in PDF.")
                continue
            got = int(m.group(1).replace(",", ""))
            exp_int = int(expected) if not isinstance(expected, dt.date) else None
            if exp_int is not None and got != exp_int:
                mismatches.append(f"Overall Statistics: {key} PDF={got:,} dataset={exp_int:,}.")

        date_match = re.search(
            r"Date range\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})\s*[–-]\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})",
            overall_block,
            flags=re.S,
        )
        if not date_match:
            mismatches.append("Overall Statistics: could not parse 'Date range' in PDF.")
        else:
            start = parse_month_day_year(date_match.group(1))
            end = parse_month_day_year(date_match.group(2))
            if start != first_date or end != last_date:
                mismatches.append(
                    "Overall Statistics: Date range PDF="
                    f"{date_match.group(1)}–{date_match.group(2)} dataset="
                    f"{first_date.isoformat()}–{last_date.isoformat()}."
                )

        avg_match = re.search(r"Average posts per day\s+([0-9]+\.[0-9]+)", overall_block)
        if avg_match:
            got = float(avg_match.group(1))
            if abs(got - expected_avg_posts_per_day) > 0.01:
                mismatches.append(
                    f"Overall Statistics: Average posts/day PDF={got:.2f} dataset={expected_avg_posts_per_day:.2f}."
                )
        else:
            mismatches.append("Overall Statistics: missing 'Average posts per day' row in PDF.")

        gap_match = re.search(r"Average days between posts\s+([0-9]+\.[0-9]+)", overall_block)
        if gap_match:
            got = float(gap_match.group(1))
            if abs(got - expected_avg_days_between) > 0.01:
                mismatches.append(
                    "Overall Statistics: Average days-between-posts "
                    f"PDF={got:.2f} dataset={expected_avg_days_between:.2f}."
                )
        else:
            mismatches.append("Overall Statistics: missing 'Average days between posts' row in PDF.")

    idx_by_year = parsed["idx_by_year"]
    idx_by_era = parsed["idx_by_era"]
    if idx_by_year is None or idx_by_era is None:
        mismatches.append("Missing 'Posts by Year' or 'Posts by Era' heading in PDF appendix.")
    else:
        year_rows: dict[int, tuple[int, int, int, int]] = {}
        for line in lines[idx_by_year:idx_by_era]:
            m = re.match(r"^\s*(20\d{2})\s+([0-9,]+)\s+([0-9,]+)\s+(\d+)\s+(\d+)\s*$", line)
            if not m:
                continue
            year_rows[int(m.group(1))] = (
                int(m.group(2).replace(",", "")),
                int(m.group(3).replace(",", "")),
                int(m.group(4)),
                int(m.group(5)),
            )

        expected_by_year: dict[int, tuple[int, int, int, int]] = {}
        for year in range(first_date.year, last_date.year + 1):
            year_posts = [p for p in posts if p["year_int"] == year]
            if not year_posts:
                continue
            words = [p["word_count_int"] for p in year_posts]
            expected_by_year[year] = (
                len(year_posts),
                sum(words),
                round(sum(words) / len(words)),
                int(median(words)),
            )

        missing_years = sorted(set(expected_by_year) - set(year_rows))
        if missing_years:
            mismatches.append(f"Posts by Year: missing rows for years {missing_years}.")

        for year, expected in expected_by_year.items():
            got = year_rows.get(year)
            if got is None:
                continue
            if got != expected:
                mismatches.append(
                    f"Posts by Year: {year} PDF=(posts={got[0]:,}, words={got[1]:,}, mean={got[2]}, median={got[3]}) "
                    f"dataset=(posts={expected[0]:,}, words={expected[1]:,}, mean={expected[2]}, median={expected[3]})."
                )

    idx_categories = parsed["idx_categories"]
    idx_top_tags = parsed["idx_top_tags"]
    if idx_categories is None or idx_top_tags is None:
        mismatches.append("Missing 'Categories' or 'Top 100 Tags' heading in PDF appendix.")
    else:
        category_counts: dict[str, int] = {}
        for p in posts:
            for c in p["categories_list"]:
                category_counts[c] = category_counts.get(c, 0) + 1

        pdf_categories: dict[str, int] = {}
        current_parts: list[str] | None = None
        current_count: int | None = None
        for raw in lines[idx_categories:idx_top_tags]:
            line = raw.replace("\f", "")
            stripped = line.strip()
            if not stripped:
                continue
            if re.match(r"^\d+\s+BY THE NUMBERS\s*$", stripped):
                continue
            if stripped.startswith("Category") or stripped.startswith("Posts"):
                continue
            if stripped.startswith("Note:"):
                break

            m = re.match(r"^([A-Za-z][A-Za-z -]+?)\s+([0-9,]+)\s*$", stripped)
            if m:
                if current_parts is not None and current_count is not None:
                    pdf_categories[join_wrapped_parts(current_parts)] = current_count
                current_parts = [m.group(1)]
                current_count = int(m.group(2).replace(",", ""))
                continue

            if current_parts is not None and not re.search(r"\d", stripped):
                current_parts.append(stripped)

        if current_parts is not None and current_count is not None:
            pdf_categories[join_wrapped_parts(current_parts)] = current_count

        missing_cats = sorted(set(category_counts) - set(pdf_categories))
        extra_cats = sorted(set(pdf_categories) - set(category_counts))
        if missing_cats:
            mismatches.append(f"Categories: missing categories in PDF: {missing_cats}.")
        if extra_cats:
            mismatches.append(f"Categories: unknown categories in PDF: {extra_cats}.")
        for cat, expected in category_counts.items():
            got = pdf_categories.get(cat)
            if got is None:
                continue
            if got != expected:
                mismatches.append(f"Categories: {cat} PDF={got:,} dataset={expected:,}.")

    idx_by_dow = parsed["idx_by_dow"]
    if idx_top_tags is not None and idx_by_dow is not None:
        from collections import Counter

        tag_counts = Counter()
        for p in posts:
            for t in p["tags_list"]:
                tag_counts[t] += 1

        top_tags_rows: list[tuple[int, str, int]] = []
        current_rank: int | None = None
        current_count: int | None = None
        tag_parts: list[str] = []

        for raw in lines[idx_top_tags:idx_by_dow]:
            line = raw.replace("\f", "")
            stripped = line.strip()
            if not stripped:
                continue
            # Running headers like "94 APPENDIX A: BY THE NUMBERS" can get merged into
            # the tag table; skip them regardless of leading page-number text.
            if "APPENDIX" in stripped and "BY THE NUMBERS" in stripped:
                continue
            if "APPENDIX:" in stripped or stripped.startswith("APPENDIX"):
                continue
            if re.match(r"^\d+\s+BY THE NUMBERS\s*$", stripped):
                continue
            if stripped.isdigit():
                continue
            header = stripped.lower()
            if header.startswith("rank") or header.startswith("top 100"):
                continue

            m = re.match(r"^(\d{1,3})\s+(.*?)\s+([0-9,]+)\s*$", stripped)
            if m and 1 <= int(m.group(1)) <= 100:
                if current_rank is not None and current_count is not None:
                    top_tags_rows.append((current_rank, join_wrapped_parts(tag_parts), current_count))
                current_rank = int(m.group(1))
                current_count = int(m.group(3).replace(",", ""))
                tag_parts = [m.group(2)]
                continue

            if current_rank is not None:
                tag_parts.append(stripped)

        if current_rank is not None and current_count is not None:
            top_tags_rows.append((current_rank, join_wrapped_parts(tag_parts), current_count))

        ranks = [r for r, _t, _c in top_tags_rows]
        if sorted(ranks) != list(range(1, 101)):
            mismatches.append("Top 100 Tags: ranks are not exactly 1..100 in PDF extraction.")

        cutoff = sorted(tag_counts.values(), reverse=True)[99] if len(tag_counts) >= 100 else 0
        for _rank, tag, count in top_tags_rows:
            expected_count = tag_counts.get(tag)
            if expected_count is None:
                mismatches.append(f"Top 100 Tags: tag not found in dataset: '{tag}'.")
                continue
            if count != expected_count:
                mismatches.append(f"Top 100 Tags: {tag} PDF={count:,} dataset={expected_count:,}.")
            if count < cutoff:
                mismatches.append(f"Top 100 Tags: {tag} count {count} is below cutoff {cutoff}.")

    idx_by_hour = parsed["idx_by_hour"]
    if idx_by_dow is not None and idx_by_hour is not None:
        total = len(posts)
        by_dow: dict[str, int] = {}
        for p in posts:
            day = p["dt"].strftime("%A")
            by_dow[day] = by_dow.get(day, 0) + 1

        for line in lines[idx_by_dow:idx_by_hour]:
            m = re.match(r"^\s*(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+([0-9,]+)\s+(\d+\.\d)%\s*$", line)
            if not m:
                continue
            day = m.group(1)
            got = int(m.group(2).replace(",", ""))
            got_pct = float(m.group(3))
            expected = by_dow.get(day, 0)
            expected_pct = round(expected / total * 100, 1)
            if got != expected:
                mismatches.append(f"Posts by Day of Week: {day} PDF={got:,} dataset={expected:,}.")
            if abs(got_pct - expected_pct) > 0.05:
                mismatches.append(
                    f"Posts by Day of Week: {day} % PDF={got_pct:.1f}% dataset={expected_pct:.1f}%."
                )

        by_hour: dict[int, int] = {}
        for p in posts:
            by_hour[p["dt"].hour] = by_hour.get(p["dt"].hour, 0) + 1

        peak_line = None
        for line in lines[idx_by_hour : idx_by_hour + 80]:
            if line.strip().startswith("Peak hour:"):
                peak_line = line.strip()
                break

        for line in lines[idx_by_hour : idx_by_hour + 120]:
            m = re.match(r"^\s*(\d{2}):00\s+([0-9,]+)\s+(\d+\.\d)%\s*$", line)
            if not m:
                continue
            hour = int(m.group(1))
            got = int(m.group(2).replace(",", ""))
            got_pct = float(m.group(3))
            expected = by_hour.get(hour, 0)
            expected_pct = round(expected / total * 100, 1)
            if got != expected:
                mismatches.append(f"Posts by Hour of Day: {hour:02d}:00 PDF={got:,} dataset={expected:,}.")
            if abs(got_pct - expected_pct) > 0.05:
                mismatches.append(
                    f"Posts by Hour of Day: {hour:02d}:00 % PDF={got_pct:.1f}% dataset={expected_pct:.1f}%."
                )

        if peak_line is not None:
            m = re.search(r"Peak hour:\s*(\d{2}:00)\s*\\(([\d,]+)\s+posts,\s*([0-9.]+)%\\)", peak_line)
            if m:
                peak_hour = int(m.group(1)[:2])
                peak_posts = int(m.group(2).replace(",", ""))
                peak_pct = float(m.group(3))
                expected_posts = by_hour.get(peak_hour, 0)
                expected_pct = round(expected_posts / total * 100, 1)
                if peak_posts != expected_posts or abs(peak_pct - expected_pct) > 0.05:
                    mismatches.append(
                        f"Peak hour line PDF={peak_line} dataset={peak_hour:02d}:00 ({expected_posts}, {expected_pct:.1f}%)."
                    )

    idx_single_use = parsed["idx_single_use"]
    if idx_single_use is not None:
        from collections import Counter

        tag_counts = Counter()
        for p in posts:
            for t in p["tags_list"]:
                tag_counts[t] += 1
        expected_single_use = sum(1 for c in tag_counts.values() if c == 1)

        for line in lines[idx_single_use : idx_single_use + 10]:
            m = re.match(r"^\s*(\d+)\s+tags appear exactly once", line.strip())
            if not m:
                continue
            got = int(m.group(1))
            if got != expected_single_use:
                mismatches.append(f"Single-Use Tags: PDF={got} dataset={expected_single_use}.")
            break

    idx_key_dates = parsed["idx_key_dates"]
    if idx_key_dates is not None:
        block = "\n".join(lines[idx_key_dates : idx_key_dates + 40])
        first_match = re.search(r"First post\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", block)
        if first_match:
            got = parse_month_day_year(first_match.group(1))
            if got != first_date:
                mismatches.append(
                    f"Key Dates: First post PDF={first_match.group(1)} dataset={first_date.isoformat()}."
                )
        last_match = re.search(r"Last post in dataset\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", block)
        if last_match:
            got = parse_month_day_year(last_match.group(1))
            if got != last_date:
                mismatches.append(
                    f"Key Dates: Last post PDF={last_match.group(1)} dataset={last_date.isoformat()}."
                )

    idx_programming = parsed["idx_programming"]
    if idx_programming is not None:
        from collections import Counter

        tag_counts = Counter()
        for p in posts:
            for t in p["tags_list"]:
                tag_counts[t] += 1

        wanted = {
            "Python": "Python",
            "SciPy": "SciPy",
            "Mathematica": "Mathematica",
            "PowerShell": "PowerShell",
            "C++": "C++",
            "SymPy": "SymPy",
            "Perl": "Perl",
            "Haskell": "Haskell",
            "Lisp": "Lisp",
            "R (Rstats)": "Rstats",
        }

        for line in lines[idx_programming : idx_programming + 50]:
            m = re.match(r"^\s*([A-Za-z0-9+() ]+?)\s+([0-9,]+)\s*$", line)
            if not m:
                continue
            label = re.sub(r"\s+", " ", m.group(1).strip())
            count = int(m.group(2).replace(",", ""))
            tag = wanted.get(label)
            if tag is None:
                continue
            expected = tag_counts.get(tag, 0)
            if count != expected:
                mismatches.append(f"Programming Languages: {label} PDF={count:,} dataset={expected:,}.")

    idx_special_titles = parsed["idx_special_titles"]
    if idx_special_titles is not None:
        functions = ["Gamma", "Bessel", "Zeta", "Hypergeometric", "Legendre"]
        title_counts: dict[str, int] = {fn: 0 for fn in functions}
        for p in posts:
            title = p["title_norm"]
            for fn in functions:
                if re.search(re.escape(fn), title, flags=re.I):
                    title_counts[fn] += 1

        for line in lines[idx_special_titles : idx_special_titles + 30]:
            m = re.match(r"^\s*(Gamma|Bessel|Zeta|Hypergeometric|Legendre)\s+([0-9,]+)\s*$", line)
            if not m:
                continue
            fn = m.group(1)
            got = int(m.group(2).replace(",", ""))
            expected = title_counts[fn]
            if got != expected:
                mismatches.append(f"Special Functions in Titles: {fn} PDF={got:,} dataset={expected:,}.")

    idx_extremes = parsed["idx_extremes"]
    if idx_extremes is not None:
        longest_start = next(
            (i for i in range(idx_extremes, min(idx_extremes + 80, len(lines))) if lines[i].strip() == "Longest Posts"),
            None,
        )
        shortest_start = next(
            (i for i in range(idx_extremes, min(idx_extremes + 200, len(lines))) if lines[i].strip() == "Shortest Posts"),
            None,
        )

        if longest_start is not None and shortest_start is not None and longest_start < shortest_start:
            longest_block = lines[longest_start:shortest_start]
            expected_longest = sorted(posts, key=lambda p: (-p["word_count_int"], p["dt"]))[:10]

            parsed_rows: dict[int, dict[str, object]] = {}
            current_rank: int | None = None
            title_parts: list[str] = []
            current_date_only: str | None = None
            current_wc: int | None = None
            for raw in longest_block:
                line = raw.replace("\f", "")
                stripped = line.strip()
                if not stripped:
                    continue
                if "APPENDIX:" in stripped:
                    continue
                if "BY THE NUMBERS" in stripped and re.match(r"^\d+", stripped):
                    continue
                m = re.match(r"^(\d{1,2})\s+(.+)$", stripped)
                if m and 1 <= int(m.group(1)) <= 10:
                    if current_rank is not None:
                        parsed_rows[current_rank] = {
                            "title": join_wrapped_parts(title_parts),
                            "date_only": current_date_only,
                            "word_count": current_wc,
                        }
                    current_rank = int(m.group(1))
                    rest = m.group(2).strip()
                    dm = re.search(r"(20\d{2}-\d{2}-\d{2})\s+([0-9][0-9,]*)\s*$", rest)
                    if dm:
                        current_date_only = dm.group(1)
                        current_wc = int(dm.group(2).replace(",", ""))
                        title_parts = [rest[: dm.start()].rstrip()]
                    else:
                        current_date_only = None
                        current_wc = None
                        title_parts = [rest]
                elif current_rank is not None:
                    title_parts.append(stripped)
            if current_rank is not None:
                parsed_rows[current_rank] = {
                    "title": join_wrapped_parts(title_parts),
                    "date_only": current_date_only,
                    "word_count": current_wc,
                }

            for rank, expected_post in enumerate(expected_longest, start=1):
                row = parsed_rows.get(rank)
                if not row:
                    mismatches.append(f"Longest Posts: missing rank {rank} row in PDF.")
                    continue
                title_text = str(row.get("title", ""))
                got_date = row.get("date_only")
                got_wc = row.get("word_count")
                if not got_date or got_wc is None:
                    mismatches.append(f"Longest Posts: could not parse date/words for rank {rank} in PDF.")
                    continue
                if got_date != expected_post["date_only"] or got_wc != expected_post["word_count_int"]:
                    mismatches.append(
                        f"Longest Posts: rank {rank} PDF=({got_date}, {got_wc:,}) "
                        f"dataset=({expected_post['date_only']}, {expected_post['word_count_int']:,})."
                    )
                expected_words = [w.lower() for w in re.findall(r"[\w']+", norm_title(expected_post["title_norm"]))]
                row_words = [w.lower() for w in re.findall(r"[\w']+", norm_title(title_text))]
                it = iter(row_words)
                for word in expected_words:
                    for candidate in it:
                        if candidate == word:
                            break
                    else:
                        mismatches.append(
                            f"Longest Posts: rank {rank} title mismatch (expected '{expected_post['title']}')."
                        )
                        break

    return {"mismatches": mismatches}


def check_reading_list_pdf(pdf_text: str, posts: list[dict]) -> dict:
    lines = [line.replace("\f", "").rstrip() for line in pdf_text.splitlines()]
    from collections import defaultdict

    posts_by_date: dict[str, list[dict]] = defaultdict(list)
    for p in posts:
        posts_by_date[p["date_only"]].append(p)

    def normalize_words(value: str) -> list[str]:
        value = html.unescape(value)
        value = value.replace("’", "'")
        value = re.sub(r"([A-Za-z])-\s+([A-Za-z])", r"\1\2", value)
        return [w.lower() for w in re.findall(r"[\w']+", value)]

    def detect_table_layout(line: str) -> tuple[str, int | None] | None:
        words = set(normalize_words(line))
        if not {"date", "title"} <= words:
            return None
        if "words" in words:
            m = re.search(r"\bwords\b", line, flags=re.I)
            return "words", (m.start() if m else None)
        if "categories" in words:
            m = re.search(r"\bcategories\b", line, flags=re.I)
            return "categories", (m.start() if m else None)
        if "why" in words and "essential" in words:
            m = re.search(r"\bwhy\b", line, flags=re.I)
            return "why", (m.start() if m else None)
        return None

    def extract_title_piece(text: str, mode: str | None, boundary: int | None) -> str:
        text = text.rstrip()
        if not text.strip():
            return ""
        if boundary is not None and boundary > 0:
            b = min(boundary, len(text))
            if 0 < b < len(text) and text[b - 1].isalpha() and text[b].isalpha():
                while b < len(text) and text[b].isalpha():
                    b += 1
            left = text[:b].rstrip()
            if mode == "words":
                left = re.sub(r"\s{2,}[\d,]+\s*$", "", left)
            return left.strip()

        text = text.strip()
        chunks = [c.strip() for c in re.split(r"\s{2,}", text) if c.strip()]
        if not chunks:
            return ""
        if mode == "words":
            if len(chunks) > 1 and re.fullmatch(r"[\d,]+", chunks[-1]):
                chunks = chunks[:-1]
            return " ".join(chunks).strip()
        return chunks[0]

    def is_subsequence(needle: list[str], haystack: list[str]) -> bool:
        if not needle:
            return False
        it = iter(haystack)
        for word in needle:
            for cand in it:
                if cand == word:
                    break
            else:
                return False
        return True

    entry_re = re.compile(r"^\s*(20\d{2}-\d{2}-\d{2})\s+(.+)$")
    entries: list[tuple[str, str]] = []
    current_date: str | None = None
    current_mode: str | None = None
    current_boundary: int | None = None
    current_title_parts: list[str] = []
    table_mode: str | None = None
    table_boundary: int | None = None

    for line in lines:
        maybe_layout = detect_table_layout(line)
        if maybe_layout is not None:
            table_mode, table_boundary = maybe_layout
            continue

        m = entry_re.match(line)
        if m:
            if current_date is not None:
                entries.append((current_date, join_wrapped_parts(current_title_parts)))
            current_date = m.group(1)
            current_mode = table_mode
            current_boundary = table_boundary
            current_title_parts = []
            boundary = None
            if current_boundary is not None:
                boundary = current_boundary - m.start(2)
                if boundary <= 0:
                    boundary = None
            first_piece = extract_title_piece(m.group(2), current_mode, boundary)
            if first_piece:
                current_title_parts.append(first_piece)
        elif current_date is not None:
            if is_page_number_line(line.strip()):
                continue
            if not line.strip():
                entries.append((current_date, join_wrapped_parts(current_title_parts)))
                current_date = None
                current_mode = None
                current_boundary = None
                current_title_parts = []
                continue
            if line and not line[0].isspace():
                entries.append((current_date, join_wrapped_parts(current_title_parts)))
                current_date = None
                current_mode = None
                current_boundary = None
                current_title_parts = []
                continue
            piece = extract_title_piece(line, current_mode, current_boundary)
            if piece:
                current_title_parts.append(piece)

    if current_date is not None:
        entries.append((current_date, join_wrapped_parts(current_title_parts)))

    missing: list[str] = []
    ambiguous: list[str] = []
    matched: list[tuple[str, str]] = []

    for date_s, title_blob in entries:
        candidates = posts_by_date.get(date_s, [])
        if not candidates:
            missing.append(f"{date_s}: no post on date")
            continue

        blob_words = normalize_words(title_blob)
        candidate_matches = []
        for c in candidates:
            title_words = normalize_words(c["title_norm"])
            if is_subsequence(title_words, blob_words):
                candidate_matches.append(c)

        if not candidate_matches:
            missing.append(f"{date_s}: could not match to any dataset title")
        elif len(candidate_matches) > 1:
            ambiguous.append(f"{date_s}: multiple candidate titles matched")
        else:
            matched.append((date_s, candidate_matches[0]["title"]))

    unique_matches = sorted(set(matched))
    return {
        "entries": entries,
        "unique_matches": unique_matches,
        "missing": missing,
        "ambiguous": ambiguous,
    }

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
        pass

    repos_citing = None
    combined_stars = None
    gamma_languages = None
    pep_citations = None
    official_doc_citations = None
    m_repos = re.search(r"^\|\s*Repos citing johndcook\.com\s*\|\s*([^|]+)\|", text, re.M)
    if m_repos:
        repos_citing = m_repos.group(1).strip()
    m_stars = re.search(r"^\|\s*Combined stars of citing repos\s*\|\s*([^|]+)\|", text, re.M)
    if m_stars:
        combined_stars = m_stars.group(1).strip()
    m_gamma = re.search(r"^\|\s*Languages with gamma implementation\s*\|\s*([^|]+)\|", text, re.M)
    if m_gamma:
        gamma_languages = m_gamma.group(1).strip()
    m_pep = re.search(r"^\|\s*PEP citations\s*\|\s*([^|]+)\|", text, re.M)
    if m_pep:
        pep_citations = m_pep.group(1).strip()
    m_docs = re.search(r"^\|\s*Official language doc citations\s*\|\s*([^|]+)\|", text, re.M)
    if m_docs:
        official_doc_citations = m_docs.group(1).strip()

    if (
        so_reach is None
        and twitter_accounts is None
        and twitter_followers is None
        and repos_citing is None
        and combined_stars is None
        and gamma_languages is None
        and pep_citations is None
        and official_doc_citations is None
    ):
        return None

    return {
        "path": path,
        "stack_overflow_reach": so_reach,
        "twitter_accounts": twitter_accounts,
        "twitter_followers": twitter_followers,
        "repos_citing": repos_citing,
        "combined_stars": combined_stars,
        "gamma_languages": gamma_languages,
        "pep_citations": pep_citations,
        "official_doc_citations": official_doc_citations,
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
        "--line-audit-out",
        type=Path,
        default=Path("out/factcheck/latest/line-by-line-audit.jsonl"),
        help="Line-by-line audit output (JSONL).",
    )
    parser.add_argument(
        "--canonical-line-audit-out",
        type=Path,
        default=Path("out/factcheck/line-by-line-audit.jsonl"),
        help="Stable output path for the latest line-by-line audit (JSONL).",
    )
    parser.add_argument(
        "--prose-out",
        type=Path,
        default=Path("out/factcheck/latest/prose-consistency-report.md"),
        help="Heuristic consistency/prose report output (Markdown).",
    )
    parser.add_argument(
        "--canonical-prose-out",
        type=Path,
        default=Path("out/factcheck/prose-consistency-report.md"),
        help="Stable output path for the latest prose report (Markdown).",
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
    page_count, extractor_label, extractor_note = ensure_pdf_text_and_pages(
        args.pdf,
        args.pdf_text,
        args.pages,
        pdftotext_path=pdftotext_path,
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
    if extractor_label == "pdftotext -layout" and pdftotext_path is not None:
        report.append(f"- Extracted via: `{extractor_label}` (`{pdftotext_path}`)")
    else:
        report.append(f"- Extracted via: `{extractor_label}`")
    if extractor_note is not None:
        report.append(f"- Extraction note: {extractor_note}")
    report.append(f"- Extracted text: `{args.pdf_text}` (mtime `{iso_mtime(args.pdf_text)}`)")
    report.append(f"- Page text index: `{args.pages}` (mtime `{iso_mtime(args.pages)}`, pages {page_count})")
    report.append(f"- Dataset: `{args.posts}`")
    report.append(f"- Report (latest): `{args.out}`")
    report.append(f"- Report (canonical): `{args.canonical_out}`")
    report.append(f"- Line audit (latest): `{args.line_audit_out}`")
    report.append(f"- Line audit (canonical): `{args.canonical_line_audit_out}`")
    report.append(f"- Prose report (latest): `{args.prose_out}`")
    report.append(f"- Prose report (canonical): `{args.canonical_prose_out}`")
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

    report.append("## Appendix A (PDF) Cross-Check")
    report.append("")
    by_numbers_start_page = find_page_containing(
        pages, "This appendix is the canonical reference for all statistics in the book."
    )
    reading_list_start_page = None
    if by_numbers_start_page is not None:
        reading_list_start_page = find_page_containing(
            pages, "Fifty-five posts worth reading", start_page=by_numbers_start_page
        )
    if by_numbers_start_page is None:
        report.append("- Could not locate the Appendix A section in PDF text; skipped.")
        warn_count += 1
    else:
        end_page = (reading_list_start_page - 1) if reading_list_start_page is not None else None
        appendix_a_pdf_text = join_pages_text(pages, by_numbers_start_page, end_page)
        appendix_a_pdf = check_appendix_a_pdf(appendix_a_pdf_text, posts)
        mismatches = appendix_a_pdf.get("mismatches", [])
        report.append(f"- Appendix A PDF start page: {by_numbers_start_page}")
        report.append(f"- Mismatches: {len(mismatches)}")
        if mismatches:
            error_count += 1
            for item in mismatches[:25]:
                report.append(f"  - {item}")
            if len(mismatches) > 25:
                report.append(f"  - ... and {len(mismatches) - 25} more")
    report.append("")

    report.append("## Appendix B (PDF Reading List) Cross-Check")
    report.append("")
    reading_list_end_page = None
    if reading_list_start_page is None:
        report.append("- Could not locate the Reading List section in PDF text; skipped.")
        warn_count += 1
    else:
        afterword_start_page = find_page_containing(
            pages, "Afterword: How This Book Was Made", start_page=reading_list_start_page
        )
        if afterword_start_page is not None:
            reading_list_end_page = afterword_start_page - 1
        reading_list_pdf_text = join_pages_text(pages, reading_list_start_page, reading_list_end_page)
        reading_list = check_reading_list_pdf(reading_list_pdf_text, posts)
        entries = reading_list.get("entries", [])
        unique_matches = reading_list.get("unique_matches", [])
        missing = reading_list.get("missing", [])
        ambiguous = reading_list.get("ambiguous", [])
        report.append(f"- Reading List PDF start page: {reading_list_start_page}")
        if reading_list_end_page is not None:
            report.append(f"- Reading List PDF end page: {reading_list_end_page}")
        report.append(f"- Parsed date entries: {len(entries)}")
        report.append(f"- Unique matched posts: {len(unique_matches)}")
        report.append(f"- Missing entries: {len(missing)}")
        report.append(f"- Ambiguous entries: {len(ambiguous)}")
        if missing or ambiguous:
            error_count += 1
            for item in (missing + ambiguous)[:25]:
                report.append(f"  - {item}")
            if len(missing) + len(ambiguous) > 25:
                report.append(f"  - ... and {len(missing) + len(ambiguous) - 25} more")
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

    report.append("## Line-by-Line Audit")
    report.append("")
    links_set = {p.get("link") for p in posts if p.get("link")}
    audit_total_lines = 0
    audit_numeric_lines = 0
    audit_structural_numeric = 0
    audit_verified_numeric = 0
    audit_unverified_numeric = 0
    unverified_numeric_samples: list[tuple[int, str]] = []
    url_missing: list[tuple[int, str]] = []

    gsc_clicks = gsc[1] if gsc is not None else None
    hn_submissions = hn.get("submissions") if hn is not None else None
    hn_upvotes = hn.get("upvotes") if hn is not None else None
    scholar_citations = scholar.get("citations") if scholar is not None else None

    by_numbers_end_page = (reading_list_start_page - 1) if reading_list_start_page is not None else None

    args.line_audit_out.parent.mkdir(parents=True, exist_ok=True)
    with args.line_audit_out.open("w", encoding="utf-8") as audit_f:
        for page in pages:
            page_num = page["pdf_page"]
            in_by_numbers = (
                by_numbers_start_page is not None
                and page_num >= by_numbers_start_page
                and (by_numbers_end_page is None or page_num <= by_numbers_end_page)
            )
            in_reading_list = (
                reading_list_start_page is not None
                and page_num >= reading_list_start_page
                and (reading_list_end_page is None or page_num <= reading_list_end_page)
            )

            for line_idx, line in enumerate(page["text"].splitlines(), start=1):
                audit_total_lines += 1
                has_digit = bool(re.search(r"\d", line))
                section = "main"
                if in_by_numbers:
                    section = "appendix_a_pdf"
                elif in_reading_list:
                    section = "appendix_b_pdf"

                status = "narrative"
                reason = None
                if not line.strip():
                    status = "blank"
                elif has_digit:
                    audit_numeric_lines += 1
                    if re.fullmatch(r"\s*\d{1,3}\s*", line):
                        audit_structural_numeric += 1
                        status = "layout"
                    elif section != "main":
                        status = "covered_by_section_checks"
                    else:
                        claim_line = line.strip()
                        high_signal = bool(
                            re.search(r"\d{4}-\d{2}-\d{2}", claim_line)
                            or re.search(r"\d{1,3}(,\d{3})+", claim_line)
                            or re.search(r"[+%]", claim_line)
                            or re.search(r"\d+\.\d+", claim_line)
                        )
                        if not high_signal:
                            audit_structural_numeric += 1
                            status = "low_signal_number"
                        else:
                            verified_here = False
                            if str(n_posts) in claim_line.replace(",", "") and "posts" in claim_line.lower():
                                verified_here = True
                                reason = "matches total posts"
                            elif str(span_days) in claim_line.replace(",", "") and "days" in claim_line.lower():
                                verified_here = True
                                reason = "matches total days"
                            elif "citations" in claim_line.lower() and scholar_citations is not None:
                                got = parse_int_with_commas(claim_line)
                                if got == scholar_citations:
                                    verified_here = True
                                    reason = "matches Scholar snapshot"
                            elif "search clicks" in claim_line.lower() and gsc_clicks is not None:
                                # threshold claims like "over 600,000"
                                got = parse_int_with_commas(claim_line)
                                if got is not None and gsc_clicks >= got:
                                    verified_here = True
                                    reason = "meets GSC threshold"
                            elif "hacker news" in claim_line.lower() and hn_submissions is not None and "submission" in claim_line.lower():
                                got = parse_int_with_commas(claim_line)
                                if got is not None and hn_submissions >= got:
                                    verified_here = True
                                    reason = "meets HN submissions threshold"
                            elif "upvotes" in claim_line.lower() and hn_upvotes is not None:
                                got = parse_int_with_commas(claim_line)
                                if got is not None and hn_upvotes >= got:
                                    verified_here = True
                                    reason = "meets HN upvotes threshold"
                            elif impact is not None:
                                impact_pairs = [
                                    ("repos citing", impact.get("repos_citing")),
                                    ("combined stars", impact.get("combined_stars")),
                                    ("gamma", impact.get("gamma_languages")),
                                ]
                                for key, expected in impact_pairs:
                                    if expected and expected in claim_line:
                                        verified_here = True
                                        reason = f"matches impact notes ({key})"
                                        break

                            if verified_here:
                                audit_verified_numeric += 1
                                status = "verified_against_local_data"
                            else:
                                audit_unverified_numeric += 1
                                status = "unverified_numeric"
                                if len(unverified_numeric_samples) < 50:
                                    unverified_numeric_samples.append((page_num, claim_line))

                for url in re.findall(r"https?://\\S+", line):
                    cleaned = url.rstrip(").,;]")
                    if cleaned.startswith("https://www.johndcook.com/blog/") and cleaned not in links_set:
                        url_missing.append((page_num, cleaned))

                audit_f.write(
                    json.dumps(
                        {
                            "pdf_page": page_num,
                            "line": line_idx,
                            "section": section,
                            "status": status,
                            "reason": reason,
                            "text": line,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )

    args.canonical_line_audit_out.parent.mkdir(parents=True, exist_ok=True)
    args.canonical_line_audit_out.write_text(args.line_audit_out.read_text(encoding="utf-8"), encoding="utf-8")

    report.append(f"- Total lines scanned: {audit_total_lines:,}")
    report.append(f"- Lines containing digits: {audit_numeric_lines:,}")
    report.append(f"- Structural/low-signal numeric lines: {audit_structural_numeric:,}")
    report.append(f"- Verified numeric lines (local data): {audit_verified_numeric:,}")
    report.append(f"- Unverified numeric lines (sampled): {audit_unverified_numeric:,}")
    if url_missing:
        error_count += 1
        report.append(f"- Missing johndcook.com/blog URLs in dataset: {len(url_missing)}")
        for page_num, url in url_missing[:10]:
            report.append(f"  - PDF page {page_num}: {url}")
        if len(url_missing) > 10:
            report.append(f"  - ... and {len(url_missing) - 10} more")
    if unverified_numeric_samples:
        report.append("- Unverified numeric lines (sample):")
        for page_num, text in unverified_numeric_samples[:25]:
            report.append(f"  - PDF page {page_num}: {text}")
        if len(unverified_numeric_samples) > 25:
            report.append(f"  - ... and {len(unverified_numeric_samples) - 25} more shown in audit file")
    report.append("")

    prose = build_prose_consistency_report(
        pages=pages,
        pdf_path=args.pdf,
        pdf_sha=pdf_sha,
        now=now,
        run_id=run_id,
        pdf_text_path=args.pdf_text,
        pages_path=args.pages,
        n_posts=n_posts,
        total_words=total_words,
        span_days=span_days,
        mean_words=mean_words,
        median_words=median_words,
    )
    args.prose_out.parent.mkdir(parents=True, exist_ok=True)
    args.prose_out.write_text(prose["report_text"], encoding="utf-8")
    args.canonical_prose_out.parent.mkdir(parents=True, exist_ok=True)
    args.canonical_prose_out.write_text(prose["report_text"], encoding="utf-8")

    report.append("## Consistency & Prose (Heuristic)")
    report.append("")
    report.append(f"- Report (latest): `{args.prose_out}`")
    report.append(f"- Report (canonical): `{args.canonical_prose_out}`")
    report.append(f"- Duplicate long paragraphs: {prose['summary']['duplicate_paragraphs']}")
    report.append(f"- Repeated long sentences: {prose['summary']['repeated_sentences']}")
    report.append(f"- Possible doubled-word typos: {prose['summary']['double_words']}")
    report.append(f"- Mixed term/casing groups: {prose['summary']['term_variant_groups']}")
    report.append(f"- Potential inconsistent numeric lines: {prose['summary']['numeric_inconsistencies']}")
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
                "extractor": extractor_label,
                "extractor_note": extractor_note,
                "pdftotext": str(pdftotext_path) if pdftotext_path is not None else None,
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
                "line_audit_latest_path": str(args.line_audit_out),
                "line_audit_canonical_path": str(args.canonical_line_audit_out),
                "prose_report_latest_path": str(args.prose_out),
                "prose_report_canonical_path": str(args.canonical_prose_out),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (archive_run_dir / "fact-check-report.md").write_text(report_text, encoding="utf-8")
    (archive_run_dir / "prose-consistency-report.md").write_text(prose["report_text"], encoding="utf-8")
    shutil.copy2(args.pdf_text, archive_run_dir / args.pdf_text.name)
    shutil.copy2(args.pages, archive_run_dir / args.pages.name)
    shutil.copy2(args.line_audit_out, archive_run_dir / args.line_audit_out.name)

    print(f"wrote {args.out}")
    print(f"wrote {args.canonical_out}")
    print(f"archived {archive_run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
