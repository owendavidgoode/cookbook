#!/usr/bin/env python3
"""Convert markdown chapters to LaTeX format."""

import re
from pathlib import Path

BOOK_DIR = Path(__file__).parent.parent
MD_DIR = BOOK_DIR
LATEX_DIR = BOOK_DIR / "latex" / "chapters"

# Figure mapping: placeholder text -> (filename, caption)
FIGURE_MAP = {
    "Full-span activity heatmap": ("ch01_activity_heatmap", "Posting activity across 17 years"),
    "Dual-axis line chart showing posts per year": ("ch01_posts_wordcount", "The inverse relationship: fewer posts, more depth"),
    "Treemap of all categories": ("ch02_category_treemap", "Category distribution: Math dominates at 45\\%"),
    "Circular packing diagram": ("ch02_category_packing", "The category universe"),
    "Radial bar chart": ("ch03_weekday_radial", "Posting by day of week: Tuesday peaks"),
    "Dumbbell chart showing first/last appearance of each constant": ("ch04_constants_dumbbell", "Mathematical constants: first and last appearances"),
    "Timeline showing when major functions first appeared": ("ch04_functions_timeline", "Special functions over time"),
    "Stacked area chart showing language mentions": ("ch05_languages_stacked", "Programming languages over time"),
    "Bar chart showing total posts per programming language": ("ch05_languages_bar", "Programming languages by total posts"),
    "Line chart with annotations showing crypto and privacy": ("ch06_crypto_line", "Cryptography and privacy posts over time"),
    "Dumbbell chart showing first and last appearance of cryptography": ("ch06_crypto_dumbbell", "Cryptography topics: first to last appearance"),
    "Network diagram showing categories": ("ch07_category_network", "Category co-occurrence network"),
    "Small multiples showing topic evolution": ("ch09_small_multiples", "Topic evolution across eras"),
    "Connected scatterplot with era annotations": ("ch09_scatterplot_eras", "The three eras: evolution of output"),
}


def md_to_latex(md_content: str, is_prologue: bool = False, is_appendix: bool = False) -> str:
    """Convert markdown to LaTeX."""
    lines = md_content.split('\n')
    latex_lines = []
    in_code_block = False
    code_lang = ""
    in_table = False
    table_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lang = line[3:].strip() or "text"
                latex_lines.append(f"\\begin{{lstlisting}}[language={code_lang}]")
            else:
                in_code_block = False
                latex_lines.append("\\end{lstlisting}")
            i += 1
            continue

        if in_code_block:
            latex_lines.append(line)
            i += 1
            continue

        # Tables
        if '|' in line and not line.startswith('['):
            if not in_table:
                in_table = True
                table_lines = [line]
            else:
                table_lines.append(line)
            i += 1
            # Check if next line continues table
            if i >= len(lines) or '|' not in lines[i] or lines[i].startswith('['):
                # End of table, convert it
                latex_lines.extend(convert_table(table_lines))
                in_table = False
                table_lines = []
            continue

        # Chapter title (# heading)
        if line.startswith('# '):
            title = line[2:].strip()
            # Remove "Chapter N:" prefix if present
            title = re.sub(r'^(Chapter \d+|Prologue|Epilogue|Appendix [AB]):\s*', '', title)
            if is_prologue:
                latex_lines.append(f"\\chapter*{{{title}}}")
                latex_lines.append(f"\\addcontentsline{{toc}}{{chapter}}{{{title}}}")
            elif is_appendix:
                latex_lines.append(f"\\chapter{{{title}}}")
            else:
                latex_lines.append(f"\\chapter{{{title}}}")
            i += 1
            continue

        # Section headings
        if line.startswith('## '):
            section = line[3:].strip()
            latex_lines.append(f"\\section*{{{escape_latex(section)}}}")
            i += 1
            continue

        if line.startswith('### '):
            subsection = line[4:].strip()
            latex_lines.append(f"\\subsection*{{{escape_latex(subsection)}}}")
            i += 1
            continue

        # Epigraph (> quote at start)
        if line.startswith('> ') and (i == 0 or (i > 0 and lines[i-1].strip() == '' and i < 5)):
            quote_lines = []
            while i < len(lines) and lines[i].startswith('> '):
                quote_lines.append(lines[i][2:])
                i += 1
            quote_text = ' '.join(quote_lines)
            # Check for attribution (— or --)
            if '—' in quote_text:
                parts = quote_text.rsplit('—', 1)
                quote_body = parts[0].strip()
                attrib = parts[1].strip()
                latex_lines.append(f"\\epigraph{{{escape_latex(quote_body)}}}{{{escape_latex(attrib)}}}")
            else:
                latex_lines.append(f"\\epigraph{{{escape_latex(quote_text)}}}{{}}")
            continue

        # Block quotes (other > lines)
        if line.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].startswith('> '):
                quote_lines.append(lines[i][2:])
                i += 1
            quote_text = '\n'.join(quote_lines)
            latex_lines.append("\\begin{quote}")
            latex_lines.append(escape_latex(quote_text))
            latex_lines.append("\\end{quote}")
            continue

        # Figure placeholders
        if line.startswith('[FIGURE:'):
            fig_desc = line[8:].rstrip(']').strip()
            fig_file, fig_caption = find_figure(fig_desc)
            if fig_file:
                latex_lines.append(f"\\bookfigure{{{fig_file}}}{{{fig_caption}}}")
            else:
                latex_lines.append(f"% TODO: Figure placeholder: {fig_desc}")
            i += 1
            continue

        # Horizontal rules
        if line.strip() == '---':
            latex_lines.append("\\bigskip")
            i += 1
            continue

        # Italic emphasis for standalone lines
        if line.startswith('*') and line.endswith('*') and not line.startswith('**'):
            text = line[1:-1]
            latex_lines.append(f"\\textit{{{escape_latex(text)}}}")
            latex_lines.append("")
            i += 1
            continue

        # Regular paragraph
        if line.strip():
            latex_lines.append(process_inline(line))
        else:
            latex_lines.append("")

        i += 1

    return '\n'.join(latex_lines)


def convert_table(table_lines: list) -> list:
    """Convert markdown table to LaTeX."""
    if len(table_lines) < 2:
        return []

    # Parse header
    header = [c.strip() for c in table_lines[0].split('|')[1:-1]]
    num_cols = len(header)

    # Skip separator line (|---|---|)
    data_start = 1
    if table_lines[1].replace('-', '').replace('|', '').replace(' ', '') == '':
        data_start = 2

    # Parse data rows
    rows = []
    for line in table_lines[data_start:]:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) == num_cols:
            rows.append(cells)

    # Build LaTeX table
    col_spec = 'l' * num_cols
    latex = [
        "\\begin{center}",
        f"\\begin{{tabular}}{{{col_spec}}}",
        "\\toprule",
        ' & '.join([f"\\textbf{{{escape_latex(h)}}}" for h in header]) + " \\\\",
        "\\midrule"
    ]

    for row in rows:
        latex.append(' & '.join([escape_latex(c) for c in row]) + " \\\\")

    latex.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{center}"
    ])

    return latex


def find_figure(description: str) -> tuple:
    """Find figure file and caption from description."""
    for key, (filename, caption) in FIGURE_MAP.items():
        if key.lower() in description.lower():
            return filename, caption
    return None, None


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    # Don't escape if it's already LaTeX math
    if '$' in text:
        # Split by $ and only escape non-math parts
        parts = text.split('$')
        for i in range(0, len(parts), 2):  # Even indices are non-math
            parts[i] = _escape_text(parts[i])
        return '$'.join(parts)
    return _escape_text(text)


def _escape_text(text: str) -> str:
    """Escape text (not math)."""
    replacements = [
        ('\\', '\\textbackslash{}'),
        ('&', '\\&'),
        ('%', '\\%'),
        ('#', '\\#'),
        ('_', '\\_'),
        ('{', '\\{'),
        ('}', '\\}'),
        ('~', '\\textasciitilde{}'),
        ('^', '\\textasciicircum{}'),
    ]
    for old, new in replacements:
        if old != '\\':  # Already handled
            text = text.replace(old, new)
    return text


def process_inline(text: str) -> str:
    """Process inline markdown formatting."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)
    # Links (just show text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    return escape_latex(text)


def convert_file(md_path: Path, tex_path: Path, is_prologue: bool = False, is_appendix: bool = False):
    """Convert a single markdown file to LaTeX."""
    content = md_path.read_text()
    latex = md_to_latex(content, is_prologue=is_prologue, is_appendix=is_appendix)
    tex_path.write_text(latex)
    print(f"  {md_path.name} -> {tex_path.name}")


def main():
    LATEX_DIR.mkdir(parents=True, exist_ok=True)

    # Chapter files to convert
    chapters = [
        ("00-prologue.md", "00-prologue.tex", True, False),
        ("01-shape-of-seventeen-years.md", "01-shape-of-seventeen-years.tex", False, False),
        ("02-topography-of-interest.md", "02-topography-of-interest.tex", False, False),
        ("03-rhythm-of-a-working-mind.md", "03-rhythm-of-a-working-mind.tex", False, False),
        ("04-mathematical-obsessions.md", "04-mathematical-obsessions.tex", False, False),
        ("05-languages-as-thinking-tools.md", "05-languages-as-thinking-tools.tex", False, False),
        ("06-cryptographys-moment.md", "06-cryptographys-moment.tex", False, False),
        ("07-edges-of-the-map.md", "07-edges-of-the-map.tex", False, False),
        ("08-interviews.md", "08-interviews.tex", False, False),
        ("09-evolution-of-a-blog.md", "09-evolution-of-a-blog.tex", False, False),
        ("10-what-the-numbers-miss.md", "10-what-the-numbers-miss.tex", False, False),
        ("appendix-a-by-the-numbers.md", "appendix-a.tex", False, True),
        ("appendix-b-reading-list.md", "appendix-b.tex", False, True),
        ("99-epilogue.md", "99-epilogue.tex", False, False),
    ]

    print("Converting markdown to LaTeX...")
    for md_name, tex_name, is_prol, is_app in chapters:
        md_path = MD_DIR / md_name
        tex_path = LATEX_DIR / tex_name
        if md_path.exists():
            convert_file(md_path, tex_path, is_prologue=is_prol, is_appendix=is_app)
        else:
            print(f"  WARNING: {md_name} not found")

    print("Done!")


if __name__ == "__main__":
    main()
