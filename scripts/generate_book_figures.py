#!/usr/bin/env python3
"""
Generate all 19 figures for the Methodical book.

Output: SVG files in book/figures/
Data sources: data/posts_metadata.csv, data/johndcook_text_index.jsonl

Usage:
    python scripts/generate_book_figures.py
    python scripts/generate_book_figures.py --chapter 1
"""

import argparse
import json
from pathlib import Path
from collections import Counter
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Style configuration for print
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Color palette (print-friendly)
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#7f8c8d',
    'accent': '#e74c3c',
    'math': '#3498db',
    'computing': '#2ecc71',
    'statistics': '#9b59b6',
    'other': '#95a5a6',
}

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
FIGURES_DIR = BASE_DIR / 'book' / 'figures'


def load_data():
    """Load the posts metadata."""
    df = pd.read_csv(DATA_DIR / 'posts_metadata.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    return df


# =============================================================================
# Chapter 1: The Shape of Seventeen Years
# =============================================================================

def fig_01_activity_heatmap(df):
    """GitHub-style activity heatmap for all 17 years."""
    fig, ax = plt.subplots(figsize=(12, 3))

    # Create date range and count posts per day
    date_range = pd.date_range(start='2008-01-01', end='2025-12-31', freq='D')
    daily_counts = df.groupby(df['date'].dt.date).size()

    # Create matrix: rows = day of week (0-6), cols = week number across all years
    # We'll create a simpler year-by-year heatmap instead

    years = range(2008, 2026)
    data = np.zeros((7, len(years) * 53))  # 7 days x ~53 weeks per year

    for _, row in df.iterrows():
        year_idx = row['date'].year - 2008
        week_of_year = row['date'].isocalendar()[1] - 1
        day_of_week = row['date'].weekday()
        col_idx = year_idx * 53 + min(week_of_year, 52)
        if col_idx < data.shape[1]:
            data[day_of_week, col_idx] += 1

    # Plot
    im = ax.imshow(data, aspect='auto', cmap='Greens', vmin=0, vmax=3)

    # Labels
    ax.set_yticks(range(7))
    ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

    # Year labels
    year_positions = [i * 53 + 26 for i in range(len(years))]
    ax.set_xticks(year_positions[::2])  # Every other year
    ax.set_xticklabels([str(y) for y in years][::2])

    ax.set_title('Posting Activity: 2008-2025', fontweight='bold')

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.5, aspect=10)
    cbar.set_label('Posts per day')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch01_activity_heatmap.svg')
    plt.savefig(FIGURES_DIR / 'ch01_activity_heatmap.png')
    plt.close()
    print("  Created: ch01_activity_heatmap.svg")


def fig_01_posts_and_wordcount(df):
    """Dual-axis chart: posts per year (bars) and average word count (line)."""
    fig, ax1 = plt.subplots(figsize=(10, 5))

    yearly = df.groupby('year').agg({
        'word_count': ['count', 'mean']
    })
    yearly.columns = ['posts', 'avg_words']
    years = yearly.index.tolist()

    # Bars for post count
    bars = ax1.bar(years, yearly['posts'], color=COLORS['primary'], alpha=0.7, label='Posts')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Posts per Year', color=COLORS['primary'])
    ax1.tick_params(axis='y', labelcolor=COLORS['primary'])
    ax1.set_ylim(0, 450)

    # Line for average word count
    ax2 = ax1.twinx()
    line = ax2.plot(years, yearly['avg_words'], color=COLORS['accent'], linewidth=2.5,
                    marker='o', markersize=5, label='Avg Words')
    ax2.set_ylabel('Average Words per Post', color=COLORS['accent'])
    ax2.tick_params(axis='y', labelcolor=COLORS['accent'])
    ax2.set_ylim(150, 500)

    # Title
    ax1.set_title('The Inverse Relationship: Quantity vs. Depth', fontweight='bold')

    # Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch01_posts_wordcount.svg')
    plt.savefig(FIGURES_DIR / 'ch01_posts_wordcount.png')
    plt.close()
    print("  Created: ch01_posts_wordcount.svg")


# =============================================================================
# Chapter 2: The Topography of Interest
# =============================================================================

def fig_02_category_treemap(df):
    """Treemap of all categories."""
    try:
        import squarify
    except ImportError:
        print("  SKIPPED: ch02_category_treemap.svg (squarify not installed)")
        return

    # Count categories
    cat_counts = Counter()
    for cats in df['categories'].dropna():
        for cat in cats.replace(';', ',').split(','):
            cat = cat.strip()
            if cat:
                cat_counts[cat] += 1

    # Get top categories
    top_cats = cat_counts.most_common(15)
    labels = [f"{cat}\n({count})" for cat, count in top_cats]
    sizes = [count for _, count in top_cats]

    # Colors
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(top_cats)))

    fig, ax = plt.subplots(figsize=(10, 7))
    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.8, ax=ax,
                  text_kwargs={'fontsize': 9})
    ax.axis('off')
    ax.set_title('Category Distribution: Math Dominates at 45%', fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch02_category_treemap.svg')
    plt.savefig(FIGURES_DIR / 'ch02_category_treemap.png')
    plt.close()
    print("  Created: ch02_category_treemap.svg")


def fig_02_category_packing(df):
    """Bubble chart with non-overlapping circles using force-directed placement."""
    # Count categories
    cat_counts = Counter()
    for cats in df['categories'].dropna():
        for cat in cats.replace(';', ',').split(','):
            cat = cat.strip()
            if cat:
                cat_counts[cat] += 1

    top_cats = cat_counts.most_common(10)  # Fewer for clarity

    fig, ax = plt.subplots(figsize=(12, 10))

    # Calculate radii proportional to sqrt of count
    max_count = top_cats[0][1]
    radii = [np.sqrt(count / max_count) * 2.5 for _, count in top_cats]

    # Place circles using a simple packing algorithm (largest first, spiral placement)
    positions = []
    np.random.seed(42)

    for i, ((cat, count), radius) in enumerate(zip(top_cats, radii)):
        if i == 0:
            # Largest circle at center
            x, y = 0, 0
        else:
            # Find position that doesn't overlap using spiral search
            placed = False
            for angle_offset in np.linspace(0, 2*np.pi, 36):
                for dist in np.linspace(0.5, 10, 50):
                    x = dist * np.cos(angle_offset + i * 0.5)
                    y = dist * np.sin(angle_offset + i * 0.5)

                    # Check for overlap with existing circles
                    overlap = False
                    for (px, py), pr in positions:
                        distance = np.sqrt((x - px)**2 + (y - py)**2)
                        if distance < radius + pr + 0.15:  # Gap between circles
                            overlap = True
                            break

                    if not overlap:
                        placed = True
                        break
                if placed:
                    break

        positions.append(((x, y), radius))

        # Draw circle
        circle = plt.Circle((x, y), radius, alpha=0.7,
                           color=plt.cm.Blues(0.3 + 0.5 * count / max_count),
                           edgecolor=COLORS['primary'], linewidth=1.5)
        ax.add_patch(circle)

        # Label inside circle
        fontsize = max(7, min(11, int(radius * 4)))
        ax.text(x, y, f"{cat}\n({count})", ha='center', va='center',
                fontsize=fontsize, fontweight='bold' if count > 500 else 'normal')

    # Set limits with padding
    all_x = [p[0][0] for p in positions]
    all_y = [p[0][1] for p in positions]
    all_r = [p[1] for p in positions]
    margin = 1.5
    ax.set_xlim(min(all_x) - max(all_r) - margin, max(all_x) + max(all_r) + margin)
    ax.set_ylim(min(all_y) - max(all_r) - margin, max(all_y) + max(all_r) + margin)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('The Category Universe', fontweight='bold', fontsize=14)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch02_category_packing.svg')
    plt.savefig(FIGURES_DIR / 'ch02_category_packing.png')
    plt.close()
    print("  Created: ch02_category_packing.svg")


# =============================================================================
# Chapter 3: The Rhythm of a Working Mind
# =============================================================================

def fig_03_weekday_radial(df):
    """Radial bar chart for day of week distribution."""
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    counts = df['weekday'].value_counts()
    values = [counts.get(day, 0) for day in weekday_order]

    # Radial chart
    angles = np.linspace(0, 2 * np.pi, len(weekday_order), endpoint=False).tolist()
    values_plot = values + [values[0]]  # Close the loop
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    ax.plot(angles, values_plot, 'o-', linewidth=2, color=COLORS['primary'])
    ax.fill(angles, values_plot, alpha=0.25, color=COLORS['primary'])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(weekday_order)
    ax.set_ylim(0, max(values) * 1.1)

    # Highlight Tuesday
    tuesday_idx = weekday_order.index('Tuesday')
    ax.plot(angles[tuesday_idx], values[tuesday_idx], 'o', markersize=15,
            color=COLORS['accent'], zorder=5)

    ax.set_title('Posting by Day of Week\n(Tuesday Peaks)', fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch03_weekday_radial.svg')
    plt.savefig(FIGURES_DIR / 'ch03_weekday_radial.png')
    plt.close()
    print("  Created: ch03_weekday_radial.svg")


def fig_03_connected_scatterplot(df):
    """Connected scatterplot: posts vs average length by year."""
    yearly = df.groupby('year').agg({
        'word_count': ['count', 'mean']
    })
    yearly.columns = ['posts', 'avg_words']

    fig, ax = plt.subplots(figsize=(10, 8))

    years = yearly.index.tolist()
    x = yearly['posts'].tolist()
    y = yearly['avg_words'].tolist()

    # Plot line connecting points
    ax.plot(x, y, '-', color=COLORS['secondary'], linewidth=1, alpha=0.5, zorder=1)

    # Plot points with year labels
    scatter = ax.scatter(x, y, c=years, cmap='viridis', s=100, zorder=2)

    # Add year labels
    for i, year in enumerate(years):
        offset = (5, 5) if i % 2 == 0 else (-15, -15)
        ax.annotate(str(year), (x[i], y[i]), textcoords="offset points",
                   xytext=offset, fontsize=8)

    ax.set_xlabel('Posts per Year')
    ax.set_ylabel('Average Words per Post')
    ax.set_title('The Trajectory: High Volume/Short → Moderate Volume/Long', fontweight='bold')

    # Add colorbar for years
    cbar = plt.colorbar(scatter, ax=ax, shrink=0.8)
    cbar.set_label('Year')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch03_connected_scatterplot.svg')
    plt.savefig(FIGURES_DIR / 'ch03_connected_scatterplot.png')
    plt.close()
    print("  Created: ch03_connected_scatterplot.svg")


# =============================================================================
# Chapter 4: The Numbers That Keep Appearing
# =============================================================================

def fig_04_pi_timeline(df):
    """Timeline of pi-related posts."""
    # Find pi posts - broader search to capture more pi-related content
    # Match: pi, π, 3.14, "pi day", "digits of pi", etc.
    pi_pattern = r'\bpi\b|π|3\.14|circumference|pi day|digits of'
    pi_posts = df[df['title'].str.contains(pi_pattern, case=False, na=False, regex=True)].copy()

    # Also check tags for pi-related content
    tag_pi = df[df['tags'].str.contains(r'\bpi\b|π', case=False, na=False, regex=True)]
    pi_posts = pd.concat([pi_posts, tag_pi]).drop_duplicates()
    pi_posts = pi_posts.sort_values('date')

    fig, ax = plt.subplots(figsize=(12, 4))

    # Plot timeline
    years = pi_posts['date'].dt.year
    ax.scatter(pi_posts['date'], [1] * len(pi_posts), c=years, cmap='viridis',
               s=50, alpha=0.7)

    ax.axhline(y=1, color=COLORS['secondary'], linestyle='-', alpha=0.3)
    ax.set_ylim(0.5, 1.5)
    ax.set_yticks([])
    ax.set_xlabel('Year')
    ax.set_title(f'Pi-Related Posts Over Time (n={len(pi_posts)})', fontweight='bold')

    # Format x-axis
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch04_pi_timeline.svg')
    plt.savefig(FIGURES_DIR / 'ch04_pi_timeline.png')
    plt.close()
    print("  Created: ch04_pi_timeline.svg")


def fig_04_constants_dumbbell(df):
    """Dumbbell chart: first/last appearance of mathematical constants."""
    constants = {
        'Pi': r'\bpi\b',
        'Prime': r'prime',
        'Random': r'random',
        'Fibonacci': r'fibonacci',
        'e (Euler)': r'\be\b|euler',
        'Golden ratio': r'golden|phi',
    }

    results = []
    for name, pattern in constants.items():
        matches = df[df['title'].str.contains(pattern, case=False, na=False, regex=True)]
        if len(matches) > 0:
            first = matches['date'].min().year
            last = matches['date'].max().year
            count = len(matches)
            results.append({'name': name, 'first': first, 'last': last, 'count': count})

    results = sorted(results, key=lambda x: -x['count'])

    fig, ax = plt.subplots(figsize=(10, 6))

    y_positions = range(len(results))

    for i, r in enumerate(results):
        # Draw line from first to last
        ax.plot([r['first'], r['last']], [i, i], 'o-', color=COLORS['primary'],
                linewidth=2, markersize=10)
        # Label
        ax.text(2007, i, f"{r['name']} (n={r['count']})", ha='right', va='center')

    ax.set_xlim(2006, 2026)
    ax.set_ylim(-0.5, len(results) - 0.5)
    ax.set_yticks([])
    ax.set_xlabel('Year')
    ax.set_title('First and Last Appearance of Mathematical Constants', fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch04_constants_dumbbell.svg')
    plt.savefig(FIGURES_DIR / 'ch04_constants_dumbbell.png')
    plt.close()
    print("  Created: ch04_constants_dumbbell.svg")


# =============================================================================
# Chapter 5: A Bestiary of Functions
# =============================================================================

def fig_05_functions_stacked_area(df):
    """Stacked area chart of special function mentions over time."""
    functions = ['gamma', 'Fourier', 'Bessel', 'Laplace', 'zeta']

    yearly_counts = {f: [] for f in functions}
    years = range(2008, 2026)

    for year in years:
        year_df = df[df['year'] == year]
        for func in functions:
            count = len(year_df[year_df['title'].str.contains(func, case=False, na=False)])
            yearly_counts[func].append(count)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.stackplot(years, *[yearly_counts[f] for f in functions],
                 labels=functions, alpha=0.8)

    ax.set_xlabel('Year')
    ax.set_ylabel('Posts')
    ax.set_title('Special Functions in Post Titles Over Time', fontweight='bold')
    ax.legend(loc='upper left')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch05_functions_stacked.svg')
    plt.savefig(FIGURES_DIR / 'ch05_functions_stacked.png')
    plt.close()
    print("  Created: ch05_functions_stacked.svg")


def fig_05_functions_bump(df):
    """Bump chart showing which function dominated which era."""
    functions = ['gamma', 'Fourier', 'Bessel', 'Laplace', 'zeta']
    eras = [('Early', 2008, 2012), ('Middle', 2013, 2017), ('Recent', 2018, 2025)]

    era_ranks = {era[0]: {} for era in eras}

    for era_name, start, end in eras:
        era_df = df[(df['year'] >= start) & (df['year'] <= end)]
        counts = {}
        for func in functions:
            counts[func] = len(era_df[era_df['title'].str.contains(func, case=False, na=False)])

        # Rank
        sorted_funcs = sorted(counts.keys(), key=lambda x: -counts[x])
        for rank, func in enumerate(sorted_funcs, 1):
            era_ranks[era_name][func] = rank

    fig, ax = plt.subplots(figsize=(10, 6))

    era_positions = [0, 1, 2]
    era_labels = [e[0] for e in eras]

    for func in functions:
        ranks = [era_ranks[era][func] for era in era_labels]
        ax.plot(era_positions, ranks, 'o-', label=func, linewidth=2, markersize=10)

    ax.set_xticks(era_positions)
    ax.set_xticklabels(era_labels)
    ax.set_ylabel('Rank (1 = most frequent)')
    ax.set_ylim(5.5, 0.5)  # Invert so rank 1 is at top
    ax.set_title('Function Prominence by Era', fontweight='bold')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch05_functions_bump.svg')
    plt.savefig(FIGURES_DIR / 'ch05_functions_bump.png')
    plt.close()
    print("  Created: ch05_functions_bump.svg")


# =============================================================================
# Chapter 6: The Mathematicians Behind the Theorems
# =============================================================================

def fig_06_mathematicians_timeline(df):
    """Timeline of mathematician mentions."""
    mathematicians = ['Gauss', 'Euler', 'Ramanujan', 'Newton', 'Fourier', 'Riemann']

    fig, ax = plt.subplots(figsize=(12, 6))

    for i, math_name in enumerate(mathematicians):
        matches = df[df['title'].str.contains(math_name, case=False, na=False)]
        if len(matches) > 0:
            dates = matches['date']
            ax.scatter(dates, [i] * len(dates), label=math_name, s=50, alpha=0.7)

    ax.set_yticks(range(len(mathematicians)))
    ax.set_yticklabels(mathematicians)
    ax.set_xlabel('Year')
    ax.set_title('Mathematician Mentions Over Time', fontweight='bold')

    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch06_mathematicians_timeline.svg')
    plt.savefig(FIGURES_DIR / 'ch06_mathematicians_timeline.png')
    plt.close()
    print("  Created: ch06_mathematicians_timeline.svg")


def fig_06_mathematicians_lollipop(df):
    """Lollipop chart of total mentions per mathematician."""
    mathematicians = {
        'Fourier': 'Fourier',
        'Gauss': 'Gauss',
        'Laplace': 'Laplace',
        'Bessel': 'Bessel',
        'Newton': 'Newton',
        'Euler': 'Euler',
        'Ramanujan': 'Ramanujan',
        'Fermat': 'Fermat',
        'Riemann': 'Riemann',
        'Knuth': 'Knuth',
        'Cauchy': 'Cauchy',
        'Hilbert': 'Hilbert',
    }

    counts = {}
    for display_name, search_term in mathematicians.items():
        counts[display_name] = len(df[df['title'].str.contains(search_term, case=False, na=False)])

    # Sort by count
    sorted_items = sorted(counts.items(), key=lambda x: x[1])
    names = [x[0] for x in sorted_items]
    values = [x[1] for x in sorted_items]

    fig, ax = plt.subplots(figsize=(8, 8))

    y_pos = range(len(names))
    ax.hlines(y=y_pos, xmin=0, xmax=values, color=COLORS['primary'], linewidth=2)
    ax.scatter(values, y_pos, color=COLORS['accent'], s=100, zorder=3)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.set_xlabel('Posts Mentioning Name in Title')
    ax.set_title('Mathematicians by Frequency of Mention', fontweight='bold')

    # Add count labels
    for i, v in enumerate(values):
        ax.text(v + 0.5, i, str(v), va='center')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch06_mathematicians_lollipop.svg')
    plt.savefig(FIGURES_DIR / 'ch06_mathematicians_lollipop.png')
    plt.close()
    print("  Created: ch06_mathematicians_lollipop.svg")


# =============================================================================
# Chapter 7: Languages as Thinking Tools
# =============================================================================

def fig_07_languages_stacked(df):
    """Stacked area chart of programming language mentions."""
    languages = ['Python', 'Mathematica', 'PowerShell', 'C++', 'Perl', 'Haskell']

    yearly_counts = {lang: [] for lang in languages}
    years = range(2008, 2026)

    for year in years:
        year_df = df[df['year'] == year]
        for lang in languages:
            # Check tags
            count = 0
            for tags in year_df['tags'].dropna():
                if lang.lower() in tags.lower():
                    count += 1
            yearly_counts[lang].append(count)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.stackplot(years, *[yearly_counts[lang] for lang in languages],
                 labels=languages, alpha=0.8)

    ax.set_xlabel('Year')
    ax.set_ylabel('Posts (by tag)')
    ax.set_title('Programming Languages Over Time', fontweight='bold')
    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch07_languages_stacked.svg')
    plt.savefig(FIGURES_DIR / 'ch07_languages_stacked.png')
    plt.close()
    print("  Created: ch07_languages_stacked.svg")


def fig_07_languages_bar(df):
    """Bar chart of total posts per language."""
    languages = ['Python', 'SciPy', 'Mathematica', 'PowerShell', 'C++', 'Perl',
                 'Haskell', 'SymPy', 'Emacs']

    counts = {}
    for lang in languages:
        count = 0
        for tags in df['tags'].dropna():
            if lang.lower() in tags.lower():
                count += 1
        counts[lang] = count

    # Sort
    sorted_items = sorted(counts.items(), key=lambda x: -x[1])
    names = [x[0] for x in sorted_items]
    values = [x[1] for x in sorted_items]

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(names, values, color=COLORS['primary'], alpha=0.8)
    ax.set_xlabel('Posts (by tag)')
    ax.set_title('Programming Languages and Tools by Total Posts', fontweight='bold')
    ax.invert_yaxis()

    # Add value labels
    for bar, val in zip(bars, values):
        ax.text(val + 2, bar.get_y() + bar.get_height()/2, str(val), va='center')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch07_languages_bar.svg')
    plt.savefig(FIGURES_DIR / 'ch07_languages_bar.png')
    plt.close()
    print("  Created: ch07_languages_bar.svg")


# =============================================================================
# Chapter 8: Cryptography's Moment
# =============================================================================

def fig_08_crypto_line(df):
    """Line chart of crypto and privacy posts over time."""
    years = range(2008, 2026)
    crypto_counts = []
    privacy_counts = []

    for year in years:
        year_df = df[df['year'] == year]
        crypto = 0
        privacy = 0
        for tags in year_df['tags'].dropna():
            if 'cryptography' in tags.lower():
                crypto += 1
            if 'privacy' in tags.lower():
                privacy += 1
        crypto_counts.append(crypto)
        privacy_counts.append(privacy)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(years, crypto_counts, 'o-', label='Cryptography', linewidth=2,
            color=COLORS['primary'], markersize=8)
    ax.plot(years, privacy_counts, 's-', label='Privacy', linewidth=2,
            color=COLORS['accent'], markersize=8)

    # Annotate 2019 spike
    ax.annotate('2019 Peak:\n38 crypto posts', xy=(2019, 38), xytext=(2016, 35),
                arrowprops=dict(arrowstyle='->', color='gray'),
                fontsize=9, ha='center')

    # Add context annotations
    ax.axvline(x=2018, color='gray', linestyle='--', alpha=0.5)
    ax.text(2018.1, 5, 'GDPR\n(2018)', fontsize=8, alpha=0.7)

    ax.set_xlabel('Year')
    ax.set_ylabel('Posts')
    ax.set_title('Cryptography and Privacy Posts Over Time', fontweight='bold')
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch08_crypto_line.svg')
    plt.savefig(FIGURES_DIR / 'ch08_crypto_line.png')
    plt.close()
    print("  Created: ch08_crypto_line.svg")


def fig_08_crypto_dumbbell(df):
    """Dumbbell chart for crypto topics."""
    topics = {
        'RSA': 'RSA',
        'Elliptic curves': 'elliptic curve',
        'Bitcoin': 'bitcoin',
        'Cryptocurrency': 'cryptocurrency',
        'AES': 'AES',
        'Diffie-Hellman': 'diffie',
    }

    results = []
    for display, search in topics.items():
        matches = df[df['title'].str.contains(search, case=False, na=False)]
        if len(matches) > 0:
            first = matches['date'].min().year
            last = matches['date'].max().year
            count = len(matches)
            results.append({'name': display, 'first': first, 'last': last, 'count': count})

    results = sorted(results, key=lambda x: x['first'])

    fig, ax = plt.subplots(figsize=(10, 5))

    for i, r in enumerate(results):
        ax.plot([r['first'], r['last']], [i, i], 'o-', color=COLORS['primary'],
                linewidth=2, markersize=10)
        ax.text(2007, i, f"{r['name']} (n={r['count']})", ha='right', va='center')

    ax.set_xlim(2006, 2026)
    ax.set_ylim(-0.5, len(results) - 0.5)
    ax.set_yticks([])
    ax.set_xlabel('Year')
    ax.set_title('Cryptography Topics: First to Last Appearance', fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch08_crypto_dumbbell.svg')
    plt.savefig(FIGURES_DIR / 'ch08_crypto_dumbbell.png')
    plt.close()
    print("  Created: ch08_crypto_dumbbell.svg")


# =============================================================================
# Chapter 9: The Edges of the Map
# =============================================================================

def fig_09_category_network(df):
    """Network diagram of category co-occurrence."""
    try:
        import networkx as nx
    except ImportError:
        print("  SKIPPED: ch09_category_network.svg (networkx not installed)")
        return

    # Count co-occurrences
    cooccur = Counter()
    cat_counts = Counter()

    for cats in df['categories'].dropna():
        cat_list = [c.strip() for c in cats.replace(';', ',').split(',') if c.strip()]
        for cat in cat_list:
            cat_counts[cat] += 1
        for i, c1 in enumerate(cat_list):
            for c2 in cat_list[i+1:]:
                pair = tuple(sorted([c1, c2]))
                cooccur[pair] += 1

    # Build graph
    G = nx.Graph()

    # Add top categories as nodes
    top_cats = [c for c, _ in cat_counts.most_common(12)]
    for cat in top_cats:
        G.add_node(cat, size=cat_counts[cat])

    # Add edges for co-occurrences
    for (c1, c2), count in cooccur.most_common(30):
        if c1 in top_cats and c2 in top_cats and count > 5:
            G.add_edge(c1, c2, weight=count)

    fig, ax = plt.subplots(figsize=(12, 10))

    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    # Node sizes based on count
    node_sizes = [G.nodes[n].get('size', 100) * 2 for n in G.nodes()]

    # Edge widths based on weight
    edge_weights = [G[u][v].get('weight', 1) / 5 for u, v in G.edges()]

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=COLORS['math'],
                          alpha=0.7, ax=ax)
    nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.4, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, ax=ax)

    ax.set_title('Category Co-occurrence Network\n(Math at Center)', fontweight='bold')
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch09_category_network.svg')
    plt.savefig(FIGURES_DIR / 'ch09_category_network.png')
    plt.close()
    print("  Created: ch09_category_network.svg")


# =============================================================================
# Chapter 11: The Evolution of a Blog
# =============================================================================

def fig_11_small_multiples(df):
    """Small multiples showing topic evolution across eras."""
    topics = ['Math', 'Computing', 'Statistics', 'Software development']
    eras = [('Early\n2008-12', 2008, 2012), ('Middle\n2013-17', 2013, 2017),
            ('Recent\n2018-25', 2018, 2025)]

    fig, axes = plt.subplots(1, len(topics), figsize=(14, 5), sharey=False)

    # Calculate all counts first to determine shared y-max
    all_counts = []
    for topic in topics:
        counts = []
        for _, start, end in eras:
            era_df = df[(df['year'] >= start) & (df['year'] <= end)]
            count = 0
            for cats in era_df['categories'].dropna():
                if topic.lower() in cats.lower():
                    count += 1
            counts.append(count)
        all_counts.append(counts)

    for ax, topic, counts in zip(axes, topics, all_counts):
        bars = ax.bar([e[0] for e in eras], counts, color=COLORS['primary'], alpha=0.8)
        ax.set_title(topic, fontweight='bold', pad=10)
        ax.set_ylim(0, max(counts) * 1.15 if max(counts) > 0 else 100)

        # Add value labels with proper positioning
        for bar, val in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(counts) * 0.02,
                   str(val), ha='center', va='bottom', fontsize=9)

    axes[0].set_ylabel('Posts')

    # Add overall title with proper positioning (inside figure bounds)
    fig.suptitle('Topic Evolution Across Eras', fontweight='bold', fontsize=14, y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.93])  # Leave room for suptitle
    plt.savefig(FIGURES_DIR / 'ch11_small_multiples.svg')
    plt.savefig(FIGURES_DIR / 'ch11_small_multiples.png')
    plt.close()
    print("  Created: ch11_small_multiples.svg")


def fig_11_scatterplot_eras(df):
    """Connected scatterplot with era annotations."""
    yearly = df.groupby('year').agg({
        'word_count': ['count', 'mean']
    })
    yearly.columns = ['posts', 'avg_words']

    fig, ax = plt.subplots(figsize=(10, 8))

    years = yearly.index.tolist()
    x = yearly['posts'].tolist()
    y = yearly['avg_words'].tolist()

    # Define eras
    era_colors = {
        'Early (2008-2012)': '#3498db',
        'Middle (2013-2017)': '#f39c12',
        'Recent (2018-2025)': '#2ecc71',
    }

    # Plot connecting line
    ax.plot(x, y, '-', color=COLORS['secondary'], linewidth=1, alpha=0.5, zorder=1)

    # Plot points colored by era
    for i, year in enumerate(years):
        if year <= 2012:
            color = era_colors['Early (2008-2012)']
        elif year <= 2017:
            color = era_colors['Middle (2013-2017)']
        else:
            color = era_colors['Recent (2018-2025)']

        ax.scatter(x[i], y[i], c=color, s=100, zorder=2, edgecolors='white', linewidth=1)

        # Label select years
        if year in [2008, 2012, 2014, 2017, 2019, 2022, 2025]:
            offset = (8, 8) if year % 2 == 0 else (-20, -15)
            ax.annotate(str(year), (x[i], y[i]), textcoords="offset points",
                       xytext=offset, fontsize=9)

    # Legend for eras
    for era, color in era_colors.items():
        ax.scatter([], [], c=color, s=100, label=era)
    ax.legend(loc='upper right')

    ax.set_xlabel('Posts per Year')
    ax.set_ylabel('Average Words per Post')
    ax.set_title('The Three Eras: Evolution of Output', fontweight='bold')

    # Add trajectory annotation
    ax.annotate('', xy=(x[-1], y[-1]), xytext=(x[0], y[0]),
                arrowprops=dict(arrowstyle='->', color='gray', alpha=0.3, lw=2))

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch11_scatterplot_eras.svg')
    plt.savefig(FIGURES_DIR / 'ch11_scatterplot_eras.png')
    plt.close()
    print("  Created: ch11_scatterplot_eras.svg")


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Generate book figures')
    parser.add_argument('--chapter', type=int, help='Generate figures for specific chapter only')
    args = parser.parse_args()

    print("Loading data...")
    df = load_data()
    print(f"  Loaded {len(df)} posts")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    chapters = {
        1: [fig_01_activity_heatmap, fig_01_posts_and_wordcount],
        2: [fig_02_category_treemap, fig_02_category_packing],
        3: [fig_03_weekday_radial, fig_03_connected_scatterplot],
        4: [fig_04_pi_timeline, fig_04_constants_dumbbell],
        5: [fig_05_functions_stacked_area, fig_05_functions_bump],
        6: [fig_06_mathematicians_timeline, fig_06_mathematicians_lollipop],
        7: [fig_07_languages_stacked, fig_07_languages_bar],
        8: [fig_08_crypto_line, fig_08_crypto_dumbbell],
        9: [fig_09_category_network],
        11: [fig_11_small_multiples, fig_11_scatterplot_eras],
    }

    if args.chapter:
        if args.chapter in chapters:
            print(f"\nGenerating Chapter {args.chapter} figures...")
            for func in chapters[args.chapter]:
                func(df)
        else:
            print(f"No figures defined for Chapter {args.chapter}")
    else:
        for chapter, funcs in sorted(chapters.items()):
            print(f"\nGenerating Chapter {chapter} figures...")
            for func in funcs:
                func(df)

    print("\nDone!")


if __name__ == '__main__':
    main()
