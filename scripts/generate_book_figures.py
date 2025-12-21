#!/usr/bin/env python3
"""
Generate figures for the Methodical book (Revised Structure).

Output: SVG files in book/figures/
Data sources: data/posts_metadata.csv

Usage:
    python scripts/generate_book_figures.py
    python scripts/generate_book_figures.py --chapter 1
"""

# Force non-interactive backend BEFORE importing pyplot
import matplotlib
matplotlib.use('Agg')

import argparse
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
    daily_counts = df.groupby(df['date'].dt.date).size()
    
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

    # Get top categories (10 to avoid cramped labels for small categories)
    top_cats = cat_counts.most_common(10)
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


# =============================================================================
# Chapter 4: The Connectors
# =============================================================================

def fig_04_constants_dumbbell(df):
    """Dumbbell chart: first/last appearance of mathematical constants."""
    constants = {
        'Pi': r'\\bpi\\b',
        'Prime': r'prime',
        'Random': r'random',
        'Fibonacci': r'fibonacci',
        'e (Euler)': r'\\be\\b|euler',
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

    for i, r in enumerate(results):
        # Draw line from first to last
        ax.plot([r['first'], r['last']], [i, i], 'o-', color=COLORS['primary'],
                linewidth=2, markersize=10)
        # Label
        ax.text(2007, i, f"{r['name']} (n={r['count']})", ha='right', va='center')

    ax.set_xlim(2006, 2026)
    ax.set_ylim(-0.5, len(results) - 0.5)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)  # Remove left spine to avoid label overlap
    ax.set_xlabel('Year')
    ax.set_title('First and Last Appearance of Constants', fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch04_constants_dumbbell.svg')
    plt.savefig(FIGURES_DIR / 'ch04_constants_dumbbell.png')
    plt.close()
    print("  Created: ch04_constants_dumbbell.svg")


def fig_04_functions_timeline(df):
    """Timeline of when special functions appeared."""
    functions = ['gamma', 'Fourier', 'Bessel', 'Laplace', 'zeta']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for i, func in enumerate(functions):
        matches = df[df['title'].str.contains(func, case=False, na=False)]
        if len(matches) > 0:
            dates = matches['date']
            ax.scatter(dates, [i] * len(dates), label=func, s=50, alpha=0.7)
            
    ax.set_yticks(range(len(functions)))
    ax.set_yticklabels(functions)
    ax.set_xlabel('Year')
    ax.set_title('Special Function Appearances Over Time', fontweight='bold')
    
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch04_functions_timeline.svg')
    plt.savefig(FIGURES_DIR / 'ch04_functions_timeline.png')
    plt.close()
    print("  Created: ch04_functions_timeline.svg")


# =============================================================================
# Chapter 5: The Translation Layer
# =============================================================================

def fig_05_languages_stacked(df):
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
    plt.savefig(FIGURES_DIR / 'ch05_languages_stacked.svg')
    plt.savefig(FIGURES_DIR / 'ch05_languages_stacked.png')
    plt.close()
    print("  Created: ch05_languages_stacked.svg")


def fig_05_languages_bar(df):
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
    plt.savefig(FIGURES_DIR / 'ch05_languages_bar.svg')
    plt.savefig(FIGURES_DIR / 'ch05_languages_bar.png')
    plt.close()
    print("  Created: ch05_languages_bar.svg")


# =============================================================================
# Chapter 6: Cryptography's Moment
# =============================================================================

def fig_06_crypto_line(df):
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
    plt.savefig(FIGURES_DIR / 'ch06_crypto_line.svg')
    plt.savefig(FIGURES_DIR / 'ch06_crypto_line.png')
    plt.close()
    print("  Created: ch06_crypto_line.svg")


def fig_06_crypto_dumbbell(df):
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
    ax.spines['left'].set_visible(False)  # Remove left spine to avoid label overlap
    ax.set_xlabel('Year')
    ax.set_title('Cryptography Topics: First to Last Appearance', fontweight='bold')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch06_crypto_dumbbell.svg')
    plt.savefig(FIGURES_DIR / 'ch06_crypto_dumbbell.png')
    plt.close()
    print("  Created: ch06_crypto_dumbbell.svg")


# =============================================================================
# Chapter 7: The Edges of the Map
# =============================================================================

def fig_07_category_network(df):
    """Network diagram of category co-occurrence."""
    try:
        import networkx as nx
    except ImportError:
        print("  SKIPPED: ch07_category_network.svg (networkx not installed)")
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
    # Check top 100 pairs to ensure peripheral categories (like Typography) get connected
    for (c1, c2), count in cooccur.most_common(100):
        if c1 in top_cats and c2 in top_cats and count >= 2:
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
    plt.savefig(FIGURES_DIR / 'ch07_category_network.svg')
    plt.savefig(FIGURES_DIR / 'ch07_category_network.png')
    plt.close()
    print("  Created: ch07_category_network.svg")


# =============================================================================
# Chapter 2: Topic Migration (Alluvial/Streamgraph)
# =============================================================================

def fig_02_topic_migration(df):
    """Streamgraph showing topic migration from 2008 to 2025.

    This is the "centerpiece visualization" requested by the editor (rough_editor_pass_2.md).
    It visually proves the book's central argument about intellectual evolution:
    "The Shedding and The Deepening."

    Shows the rise and fall of major categories over time:
    - Decline: Business, Software Development (professional obligations fade)
    - Rise: Math dominates by 2018+ (personal fascination wins)
    - Persistence: Statistics stays relatively steady throughout

    Technical notes:
    - Uses 'wiggle' baseline for classic streamgraph aesthetic
    - 3-point moving average smoothing for visual clarity
    - Era boundaries at 2013 (end of Notebook Phase) and 2018 (start of Institution)

    Output: ch02_topic_migration.svg, ch02_topic_migration.png
    """
    # Define the key categories to track (the narrative ones)
    categories_to_track = [
        'Math',
        'Statistics',
        'Computing',
        'Software development',
        'Business',
        'Science',
    ]

    years = list(range(2008, 2026))

    # Count posts per category per year
    data = {cat: [] for cat in categories_to_track}

    for year in years:
        year_df = df[df['year'] == year]
        for cat in categories_to_track:
            count = 0
            for cats in year_df['categories'].dropna():
                if cat.lower() in cats.lower():
                    count += 1
            data[cat].append(count)

    # Simple moving average smoothing (no scipy needed)
    def smooth(arr, window=3):
        arr = np.array(arr, dtype=float)
        result = np.copy(arr)
        for i in range(len(arr)):
            start = max(0, i - window // 2)
            end = min(len(arr), i + window // 2 + 1)
            result[i] = np.mean(arr[start:end])
        return result

    smoothed_data = {}
    for cat, counts in data.items():
        smoothed_data[cat] = smooth(counts, window=3)

    # Create streamgraph (centered stacked area)
    fig, ax = plt.subplots(figsize=(14, 7))

    # Stack the data
    y_stack = np.row_stack([smoothed_data[cat] for cat in categories_to_track])

    # Color palette - distinct but harmonious
    stream_colors = [
        '#3498db',  # Math - blue (dominant)
        '#9b59b6',  # Statistics - purple
        '#2ecc71',  # Computing - green
        '#e67e22',  # Software dev - orange
        '#e74c3c',  # Business - red
        '#1abc9c',  # Science - teal
    ]

    # Create baseline-centered streamgraph
    baseline = np.zeros(len(years))

    ax.stackplot(years, y_stack, labels=categories_to_track,
                 colors=stream_colors, alpha=0.85, baseline='wiggle')

    # Styling
    ax.set_xlim(2008, 2025)
    ax.set_xlabel('Year', fontsize=11)
    ax.set_ylabel('')  # No y-label for streamgraph
    ax.set_title('Topic Migration: The Shedding and The Deepening\n2008–2025',
                 fontweight='bold', fontsize=14)

    # Add era annotations
    ax.axvline(x=2013, color='gray', linestyle='--', alpha=0.4, linewidth=1)
    ax.axvline(x=2018, color='gray', linestyle='--', alpha=0.4, linewidth=1)

    # Era labels at top
    ax.text(2010.5, ax.get_ylim()[1] * 0.9, 'Notebook\nPhase', ha='center',
            fontsize=9, alpha=0.7, style='italic')
    ax.text(2015.5, ax.get_ylim()[1] * 0.9, 'Crucible', ha='center',
            fontsize=9, alpha=0.7, style='italic')
    ax.text(2021.5, ax.get_ylim()[1] * 0.9, 'Institution', ha='center',
            fontsize=9, alpha=0.7, style='italic')

    # Legend outside
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), frameon=False)

    # Clean up spines
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_yticks([])

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'ch02_topic_migration.svg', bbox_inches='tight')
    plt.savefig(FIGURES_DIR / 'ch02_topic_migration.png', bbox_inches='tight')
    plt.close()
    print("  Created: ch02_topic_migration.svg")


# =============================================================================
# Chapter 9: The Evolution of a Blog
# =============================================================================

def fig_09_small_multiples(df):
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
    plt.savefig(FIGURES_DIR / 'ch09_small_multiples.svg')
    plt.savefig(FIGURES_DIR / 'ch09_small_multiples.png')
    plt.close()
    print("  Created: ch09_small_multiples.svg")


def fig_09_scatterplot_eras(df):
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
    plt.savefig(FIGURES_DIR / 'ch09_scatterplot_eras.svg')
    plt.savefig(FIGURES_DIR / 'ch09_scatterplot_eras.png')
    plt.close()
    print("  Created: ch09_scatterplot_eras.svg")


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
        2: [fig_02_category_treemap, fig_02_category_packing, fig_02_topic_migration],
        3: [fig_03_weekday_radial],
        4: [fig_04_constants_dumbbell, fig_04_functions_timeline],
        5: [fig_05_languages_stacked, fig_05_languages_bar],
        6: [fig_06_crypto_line, fig_06_crypto_dumbbell],
        7: [fig_07_category_network],
        9: [fig_09_small_multiples, fig_09_scatterplot_eras],
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
