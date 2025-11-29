"""Calendar card export using WeasyPrint.

Renders 365 daily fact cards as PNG images for print production.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

# Card dimensions at 300 DPI
# Vendor template is 630x750 px ratio (0.84 aspect)
# Scaling to 300 DPI print: ~4.2" x 5" with bleed
CARD_WIDTH_IN = 4.2
CARD_HEIGHT_IN = 5.0
DPI = 300
CARD_WIDTH_PX = int(CARD_WIDTH_IN * DPI)  # 1260
CARD_HEIGHT_PX = int(CARD_HEIGHT_IN * DPI)  # 1500

# Safe area: ~0.35" margin on each side
SAFE_WIDTH_IN = 3.5
SAFE_HEIGHT_IN = 4.3

# Font paths relative to assets/fonts/
FONT_DIR = Path(__file__).parent.parent.parent / "assets" / "fonts"
SERIF_FONT = FONT_DIR / "SourceSerif4Variable-Roman.ttf"
SANS_FONT = FONT_DIR / "SourceSans3VF-Upright.ttf"


@dataclass
class Fact:
    """A single calendar fact."""

    id: int
    fact_type: str
    text: str
    source_link: str
    original_date: str
    slug: str

    @property
    def day_number(self) -> int:
        """1-indexed day number for the calendar."""
        return self.id


def load_facts(facts_path: Path) -> list[Fact]:
    """Load facts from JSON or CSV file."""
    facts = []

    if facts_path.suffix == ".json":
        import json
        with facts_path.open(encoding="utf-8") as f:
            data = json.load(f)
        for row in data:
            facts.append(
                Fact(
                    id=int(row["id"]),
                    fact_type=row["type"],
                    text=row["text"],
                    source_link=row.get("source_link", ""),
                    original_date="",
                    slug=row.get("slug", ""),
                )
            )
    else:
        # CSV fallback
        with facts_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                facts.append(
                    Fact(
                        id=int(row["id"]),
                        fact_type=row["type"],
                        text=row.get("fact") or row.get("text", ""),
                        source_link=row.get("source_link", ""),
                        original_date=row.get("date", ""),
                        slug=row.get("slug", ""),
                    )
                )
    return facts


def day_to_date(day: int, year: int) -> date:
    """Convert 1-indexed day number to calendar date for given year.

    Skips leap day - day 60+ maps to March 1+ in leap years.
    """
    jan1 = date(year, 1, 1)
    # Simple: just add days, but cap at 365
    # For leap years, we skip Feb 29 by mapping day 60 -> Mar 1
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        # Leap year - skip Feb 29
        if day >= 60:
            return jan1 + timedelta(days=day)  # +1 to skip Feb 29
        return jan1 + timedelta(days=day - 1)
    return jan1 + timedelta(days=day - 1)


def format_date(d: date) -> str:
    """Format date as MM/DD/YYYY."""
    return d.strftime("%m/%d/%Y")


def extract_number(text: str) -> float | None:
    """Try to extract a prominent number from fact text for charting.

    Returns the first percentage or large number found, or None.
    """
    # Look for percentages first
    pct_match = re.search(r"(\d+(?:\.\d+)?)\s*%", text)
    if pct_match:
        return float(pct_match.group(1))

    # Look for "X points" (HN)
    points_match = re.search(r"(\d+)\s+points?", text, re.IGNORECASE)
    if points_match:
        return float(points_match.group(1))

    # Look for "X times" or "Xth"
    times_match = re.search(r"(\d+)\s+times?", text, re.IGNORECASE)
    if times_match:
        return float(times_match.group(1))

    # Look for standalone large numbers (>10)
    numbers = re.findall(r"\b(\d+(?:,\d{3})*)\b", text)
    for num_str in numbers:
        num = int(num_str.replace(",", ""))
        if num > 10:
            return float(num)

    return None


def make_bar_svg(value: float, max_value: float = 100, width: int = 200, height: int = 20) -> str:
    """Generate a simple horizontal bar SVG for a value."""
    bar_width = int((value / max_value) * (width - 4))
    bar_width = max(2, min(bar_width, width - 4))

    return f"""<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="{width}" height="{height}" fill="#f0f0f0" rx="4"/>
  <rect x="2" y="2" width="{bar_width}" height="{height - 4}" fill="#666" rx="2"/>
</svg>"""


def render_card_html(fact: Fact) -> str:
    """Render a single card as HTML."""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @font-face {{
            font-family: 'Source Serif 4';
            src: url('file://{SERIF_FONT.absolute()}') format('truetype');
            font-weight: 100 900;
        }}
        @font-face {{
            font-family: 'Source Sans 3';
            src: url('file://{SANS_FONT.absolute()}') format('truetype');
            font-weight: 100 900;
        }}

        @page {{
            size: {CARD_WIDTH_IN}in {CARD_HEIGHT_IN}in;
            margin: 0;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html, body {{
            width: {CARD_WIDTH_IN}in;
            height: {CARD_HEIGHT_IN}in;
            background: #fefefe;
        }}

        .card {{
            width: {CARD_WIDTH_IN}in;
            height: {CARD_HEIGHT_IN}in;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: {(CARD_HEIGHT_IN - SAFE_HEIGHT_IN) / 2}in {(CARD_WIDTH_IN - SAFE_WIDTH_IN) / 2}in;
        }}

        .fact {{
            font-family: 'Source Serif 4', serif;
            font-size: 20pt;
            font-weight: 400;
            line-height: 1.3;
            color: #1a1a1a;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="fact">{fact.text}</div>
    </div>
</body>
</html>"""


def export_cards(
    facts_path: Path,
    output_dir: Path,
    limit: int | None = None,
) -> Iterator[Path]:
    """Export calendar cards as PNG images.

    Args:
        facts_path: Path to the 365 facts JSON or CSV.
        output_dir: Directory to write card images.
        limit: Optional limit on number of cards to render (for testing).

    Yields:
        Path to each rendered card image.
    """
    try:
        from weasyprint import HTML
    except ImportError as e:
        raise ImportError(
            "WeasyPrint is required for calendar export. "
            "Install with: pip install weasyprint"
        ) from e

    try:
        from pdf2image import convert_from_bytes
    except ImportError as e:
        raise ImportError(
            "pdf2image is required for PNG export. "
            "Install with: pip install pdf2image"
        ) from e

    import random

    output_dir.mkdir(parents=True, exist_ok=True)
    facts = load_facts(facts_path)

    # Shuffle facts into random order
    random.shuffle(facts)

    if limit:
        facts = facts[:limit]

    for idx, fact in enumerate(facts, start=1):
        html_content = render_card_html(fact)

        # Render HTML to PDF bytes
        doc = HTML(string=html_content)
        pdf_bytes = doc.write_pdf()

        # Convert PDF to PNG at 300 DPI
        images = convert_from_bytes(pdf_bytes, dpi=DPI)

        # Save with sequential numbering
        output_path = output_dir / f"card_{idx:03d}.png"
        images[0].save(output_path, "PNG")

        yield output_path


def validate_export(output_dir: Path, expected_count: int = 365) -> list[str]:
    """Validate exported cards.

    Returns list of error messages, empty if valid.
    """
    errors = []
    cards = sorted(output_dir.glob("card_*.png"))

    if len(cards) != expected_count:
        errors.append(f"Expected {expected_count} cards, found {len(cards)}")

    # Check for missing numbers
    expected_nums = set(range(1, expected_count + 1))
    found_nums = set()
    for card in cards:
        match = re.match(r"card_(\d+)\.png", card.name)
        if match:
            found_nums.add(int(match.group(1)))

    missing = expected_nums - found_nums
    if missing:
        errors.append(f"Missing card numbers: {sorted(missing)[:10]}...")

    return errors
