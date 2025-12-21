#!/usr/bin/env python3
"""Convert markdown chapters to LaTeX format."""

import re
from pathlib import Path

BOOK_DIR = Path(__file__).parent.parent
MD_DIR = BOOK_DIR
LATEX_DIR = BOOK_DIR / "latex" / "chapters"

# Figure mapping: placeholder text -> (filename, caption)
FIGURE_MAP = {
    "Activity heatmap": ("ch01_activity_heatmap.png", "Activity heatmap, 2008-2025"),
    "Posts per year": ("ch01_posts_wordcount.png", "Posts and length by year"),
    "Category treemap": ("ch02_category_treemap.png", "Category distribution"),
    "Circular packing": ("ch02_category_packing.png", "Category relationships"),
    "Radial chart": ("ch03_weekday_radial.png", "Weekly rhythm"),
    "Timeline showing when major": ("ch04_functions_timeline.png", "Function coverage"),
    "special functions": ("ch04_functions_timeline.png", "Function coverage"),
}


def md_to_latex(md_content: str, is_prologue: bool = False, is_appendix: bool = False) -> str:
    """Convert markdown to LaTeX."""
    lines = md_content.split('\n')
    latex_lines = []
    in_code_block = False
    code_lang = ""
    in_table = False
    table_lines = []
    in_list = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Lists
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                in_list = True
                latex_lines.append("\\begin{itemize}")
            item_text = line.strip()[2:]
            latex_lines.append(f"\\item {process_inline(item_text)}")
            i += 1
            continue
        
        if in_list and not (line.strip().startswith('- ') or line.strip().startswith('* ')):
            in_list = False
            latex_lines.append("\\end{itemize}")
            # Don't skip the current line, it needs processing
            # fall through

        # Code blocks
        if line.startswith('```'):
            if in_list: # Close list if code block starts
                 in_list = False
                 latex_lines.append("\\end{itemize}")

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
            if in_list: # Close list if table starts
                 in_list = False
                 latex_lines.append("\\end{itemize}")

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
            if in_list:
                 in_list = False
                 latex_lines.append("\\end{itemize}")
            
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
            if in_list:
                 in_list = False
                 latex_lines.append("\\end{itemize}")

            section = line[3:].strip()
            latex_lines.append(f"\\section*{{{escape_latex(section)}}}")
            i += 1
            continue

        if line.startswith('### '):
            if in_list:
                 in_list = False
                 latex_lines.append("\\end{itemize}")

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
            if in_list:
                 in_list = False
                 latex_lines.append("\\end{itemize}")

            quote_lines = []
            while i < len(lines) and lines[i].startswith('> '):
                quote_lines.append(lines[i][2:])
                i += 1
            quote_text = '\n'.join(quote_lines)
            # Strip markdown links before escaping
            quote_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', quote_text)
            # Convert em-dashes
            quote_text = quote_text.replace('—', '---')
            quote_text = quote_text.replace('–', '--')
            latex_lines.append("\\begin{blogquote}")
            latex_lines.append(escape_latex(quote_text))
            latex_lines.append("\\end{blogquote}")
            continue

        # Figure placeholders
        if line.startswith('[FIGURE:'):
            if in_list:
                 in_list = False
                 latex_lines.append("\\end{itemize}")

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
            if in_list:
                 in_list = False
                 latex_lines.append("\\end{itemize}")

            latex_lines.append("\\bigskip")
            i += 1
            continue

        # Italic emphasis for standalone lines
        if line.startswith('*') and line.endswith('*') and not line.startswith('**'):
            if in_list:
                 in_list = False
                 latex_lines.append("\\end{itemize}")

            text = line[1:-1]
            latex_lines.append(f"\\textit{{{escape_latex(text)}}}")
            latex_lines.append("")
            i += 1
            continue

        # Regular paragraph
        if line.strip():
            # Regular text, part of list? No, handled above.
            # So this must close list if open
            if in_list:
                 in_list = False
                 latex_lines.append("\\end{itemize}")

            latex_lines.append(process_inline(line))
        else:
            # Blank line. If in list, keep it open? Usually blank lines end lists in md.
            if in_list:
                 in_list = False
                 latex_lines.append("\\end{itemize}")
            latex_lines.append("")

        i += 1
    
    # End of loop list closure
    if in_list:
        latex_lines.append("\\end{itemize}")

    return '\n'.join(latex_lines)


def convert_table(table_lines: list) -> list:
    """Convert markdown table to LaTeX using longtable."""
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
        # Pad with empty strings if row is short
        while len(cells) < num_cols:
            cells.append("")
        rows.append(cells[:num_cols])

    # Build LaTeX table
    # Using longtable with p columns for wrapping (safest)
    # Using cm instead of textwidth to avoid backslash escaping hell
    TEXT_WIDTH_CM = 10.0 # Approx 4 inches
    
    if num_cols == 2:
        # Heuristic: First col usually label (tight), second col data (wide)
        # Use 'l' for first, p{6.5cm} for second.
        col_spec = "l p{6.5cm}"
    else:
        # Distributed even width
        width_val = (0.9 * TEXT_WIDTH_CM) / num_cols
        col_spec = (f"p{{{width_val:.2f}cm}}" * num_cols)
    
    latex = [
        f"\\begin{{longtable}}{{{col_spec}}}",
        "\\toprule",
        ' & '.join([f"\\textbf{{{escape_latex(h)}}}" for h in header]) + " \\tabularnewline",
        "\\midrule"
    ]

    for row in rows:
        latex.append(' & '.join([escape_latex(c) for c in row]) + " \\tabularnewline")

    latex.extend([
        "\\bottomrule",
        "\\end{longtable}"
    ])
    
    # Debug
    # print(f"DEBUG TABLE START: {latex[0:3]}")

    return latex


def find_figure(description: str) -> tuple:
    """Find figure file and caption from description."""
    for key, (filename, caption) in FIGURE_MAP.items():
        if key.lower() in description.lower():
            return filename, caption
    return None, None


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    # Convert Unicode math symbols to LaTeX
    unicode_to_latex = {
        'π': r'$\pi$',
        'α': r'$\alpha$',
        'β': r'$\beta$',
        'γ': r'$\gamma$',
        'ε': r'$\varepsilon$',
        'ζ': r'$\zeta$',
        'λ': r'$\lambda$',
        'Γ': r'$\Gamma$',
        '√': r'$\sqrt{}$',
        '∞': r'$\infty$',
        '∀': r'$\forall$',
        '∃': r'$\exists$',
        '⁻': r'$^{-}$',
        '¹': r'$^1$',
        '²': r'$^2$',
        '³': r'$^3$',
        '₀': r'$_{0}$',
        '₁': r'$_{1}$',
        '₂': r'$_{2}$',
    }
    for uni, latex in unicode_to_latex.items():
        text = text.replace(uni, latex)

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
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
    ]
    for old, new in replacements:
        if old != '\\':  # Already handled
            text = text.replace(old, new)
    return text


def process_inline(text: str) -> str:
    """Process inline markdown formatting."""
    # Links (just show text) - do first before escaping
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # Convert em-dashes to LaTeX
    text = text.replace('—', '---')
    text = text.replace('–', '--')

    # Convert Unicode math symbols to LaTeX (outside of existing math)
    unicode_to_latex = {
        'π': r'$\pi$',
        'α': r'$\alpha$',
        'β': r'$\beta$',
        'γ': r'$\gamma$',
        'ε': r'$\varepsilon$',
        'ζ': r'$\zeta$',
        'λ': r'$\lambda$',
        'Γ': r'$\Gamma$',
        '√': r'$\sqrt{}$',
        '∞': r'$\infty$',
        '∀': r'$\forall$',
        '∃': r'$\exists$',
        '⁻': r'$^{-}$',
        '¹': r'$^1$',
        '²': r'$^2$',
        '³': r'$^3$',
        '₀': r'$_{0}$',
        '₁': r'$_{1}$',
        '₂': r'$_{2}$',
    }
    for uni, latex in unicode_to_latex.items():
        text = text.replace(uni, latex)

    # If text contains math ($...$), process math and non-math parts separately
    if '$' in text:
        parts = text.split('$')
        result_parts = []
        for i, part in enumerate(parts):
            if i % 2 == 0:  # Non-math part (even indices)
                result_parts.append(_process_text_part(part))
            else:  # Math part (odd indices) - leave as-is
                result_parts.append(part)
        return '$'.join(result_parts)
    else:
        return _process_text_part(text)


def _process_text_part(text: str) -> str:
    """Process non-math text: escape special chars and apply markdown formatting."""
    # Protect markdown syntax first
    text = text.replace('**', '\x00BOLD\x00')
    text = text.replace('*', '\x00ITAL\x00')
    text = text.replace('`', '\x00CODE\x00')

    # Escape LaTeX special chars
    text = text.replace('&', r'\&')
    text = text.replace('%', r'\%')
    text = text.replace('#', r'\#')
    text = text.replace('_', r'\_')
    text = text.replace('~', r'\textasciitilde{}')
    text = text.replace('^', r'\textasciicircum{}')

    # Restore markdown and convert to LaTeX
    text = text.replace('\x00BOLD\x00', '**')
    text = text.replace('\x00ITAL\x00', '*')
    text = text.replace('\x00CODE\x00', '`')

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)

    return text


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
        ("01-the-shape-of-the-start.md", "01-the-shape-of-the-start.tex", False, False),
        ("02-the-consultants-toolkit.md", "02-the-consultants-toolkit.tex", False, False),
        ("03-finding-the-rhythm.md", "03-finding-the-rhythm.tex", False, False),
        ("04-the-quiet-year.md", "04-the-quiet-year.tex", False, False),
        ("05-the-deepening.md", "05-the-deepening.tex", False, False),
        ("06-the-shedding.md", "06-the-shedding.tex", False, False),
        ("07-the-mathematical-core.md", "07-the-mathematical-core.tex", False, False),
        ("08-adaptation-and-urgency.md", "08-adaptation-and-urgency.tex", False, False),
        ("09-the-modern-translation-layer.md", "09-the-modern-translation-layer.tex", False, False),
        ("10-the-shape-of-persistence.md", "10-the-shape-of-persistence.tex", False, False),
        ("11-the-dark-matter.md", "11-the-dark-matter.tex", False, False),
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