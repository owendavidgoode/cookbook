#!/usr/bin/env python3
"""
Visual Sampler v2: Publication-Quality Visualization Showcase
For "The Endeavour by the Numbers" book project

Demonstrates 12+ visualization techniques with professional styling.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from collections import Counter
import re
import os
import json
from datetime import datetime
import textwrap

# --- Configuration ---
DATA_DIR = "data"
OUTPUT_DIR = "book/visual_sampler_v2/images"
CALENDAR_FACTS_PATH = f"{DATA_DIR}/johndcook_calendar_candidates_filtered.csv"
METADATA_PATH = f"{DATA_DIR}/posts_metadata.csv"
ENRICHED_POSTS_PATH = f"{DATA_DIR}/johndcook_posts_enriched.jsonl"

# Professional color palettes
ENDEAVOUR_COLORS = {
    'primary': '#1a365d',      # Deep navy
    'secondary': '#2c5282',    # Medium blue
    'accent': '#ed8936',       # Warm orange
    'accent2': '#48bb78',      # Green
    'accent3': '#9f7aea',      # Purple
    'light': '#edf2f7',        # Light gray
    'text': '#2d3748',         # Dark gray
    'muted': '#718096',        # Muted gray
}

# Custom colormap for the project
endeavour_cmap = LinearSegmentedColormap.from_list(
    'endeavour',
    ['#1a365d', '#2c5282', '#4299e1', '#63b3ed', '#bee3f8']
)

def setup_style():
    """Configure matplotlib for publication-quality output."""
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': False,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'savefig.facecolor': 'white',
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
    })

def save_figure(fig, filename):
    """Save figure with consistent settings."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  ✓ Saved: {filename}")

def load_data():
    """Load all data sources."""
    facts_df = pd.read_csv(CALENDAR_FACTS_PATH)
    metadata_df = pd.read_csv(METADATA_PATH)
    metadata_df['date'] = pd.to_datetime(metadata_df['date'])

    # Load enriched posts
    posts = []
    with open(ENRICHED_POSTS_PATH, 'r') as f:
        for line in f:
            posts.append(json.loads(line))
    enriched_df = pd.DataFrame(posts)

    return facts_df, metadata_df, enriched_df

# =============================================================================
# VISUALIZATION 1: Posting Activity Heatmap (GitHub-style)
# =============================================================================
def viz_01_activity_heatmap(metadata_df):
    """GitHub-style contribution heatmap showing posting frequency."""
    print("1. Activity Heatmap...")

    # Get last 3 years of data
    recent = metadata_df[metadata_df['year'] >= 2022].copy()
    recent['week'] = recent['date'].dt.isocalendar().week
    recent['weekday'] = recent['date'].dt.weekday

    # Count posts per day
    daily_counts = recent.groupby(['year', 'week', 'weekday']).size().reset_index(name='count')

    fig, axes = plt.subplots(3, 1, figsize=(14, 6), gridspec_kw={'hspace': 0.4})

    for idx, year in enumerate([2023, 2024, 2025]):
        ax = axes[idx]
        year_data = daily_counts[daily_counts['year'] == year]

        # Create grid
        grid = np.zeros((7, 53))
        for _, row in year_data.iterrows():
            if row['week'] <= 53:
                grid[int(row['weekday']), int(row['week'])-1] = row['count']

        # Plot
        cmap = LinearSegmentedColormap.from_list('activity', ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39'])
        im = ax.imshow(grid, cmap=cmap, aspect='auto', vmin=0, vmax=max(3, grid.max()))

        ax.set_title(f'{year}', loc='left', fontweight='bold', fontsize=12)
        ax.set_yticks(range(7))
        ax.set_yticklabels(['Mon', '', 'Wed', '', 'Fri', '', 'Sun'], fontsize=9)
        ax.set_xticks([0, 13, 26, 39, 52])
        ax.set_xticklabels(['Jan', 'Apr', 'Jul', 'Oct', 'Dec'], fontsize=9)
        ax.tick_params(length=0)

        for spine in ax.spines.values():
            spine.set_visible(False)

    # Colorbar
    cbar = fig.colorbar(im, ax=axes, orientation='vertical', shrink=0.5, pad=0.02)
    cbar.set_label('Posts per day', fontsize=10)
    cbar.ax.tick_params(labelsize=9)

    fig.suptitle('Posting Activity Over Time', fontsize=14, fontweight='bold', y=1.02)
    save_figure(fig, '01_activity_heatmap.png')

# =============================================================================
# VISUALIZATION 2: Category Treemap
# =============================================================================
def viz_02_category_treemap(metadata_df):
    """Treemap showing category distribution."""
    print("2. Category Treemap...")
    import matplotlib.patches as mpatches

    # Count categories
    all_cats = metadata_df['categories'].dropna().str.split(';').explode()
    cat_counts = all_cats.value_counts().head(20)

    # Simple treemap using squarify algorithm
    def squarify(values, x, y, width, height):
        """Simple squarify algorithm for treemap."""
        if len(values) == 0:
            return []

        total = sum(values)
        rects = []

        if width >= height:
            # Lay out horizontally
            curr_x = x
            for val in values:
                w = (val / total) * width
                rects.append((curr_x, y, w, height))
                curr_x += w
        else:
            # Lay out vertically
            curr_y = y
            for val in values:
                h = (val / total) * height
                rects.append((x, curr_y, width, h))
                curr_y += h

        return rects

    fig, ax = plt.subplots(figsize=(12, 8))

    values = cat_counts.values.tolist()
    labels = cat_counts.index.tolist()

    # Normalize and create rectangles
    total = sum(values)
    normalized = [v/total for v in values]

    # Use a simple row-based layout
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(values)))

    # Calculate rectangles manually with better algorithm
    rects = []
    x, y = 0, 0
    row_height = 0.25
    row_width = 0
    row_items = []

    for i, (val, label) in enumerate(zip(normalized, labels)):
        width = val * 4  # Scale factor
        if row_width + width > 1.0:
            # New row
            curr_x = 0
            for item in row_items:
                rects.append((curr_x, y, item[0], row_height, item[1], item[2]))
                curr_x += item[0]
            y += row_height
            row_items = []
            row_width = 0
        row_items.append((width, label, values[i]))
        row_width += width

    # Last row
    if row_items:
        curr_x = 0
        for item in row_items:
            rects.append((curr_x, y, item[0], row_height, item[1], item[2]))
            curr_x += item[0]

    # Draw rectangles
    for i, (rx, ry, rw, rh, label, count) in enumerate(rects):
        color = plt.cm.Blues(0.3 + 0.6 * (count / max(values)))
        rect = mpatches.FancyBboxPatch(
            (rx, ry), rw - 0.005, rh - 0.01,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            facecolor=color, edgecolor='white', linewidth=2
        )
        ax.add_patch(rect)

        # Add label if rectangle is big enough
        if rw > 0.08:
            text_color = 'white' if count > max(values) * 0.3 else ENDEAVOUR_COLORS['text']
            ax.text(rx + rw/2, ry + rh/2, f'{label}\n({count:,})',
                   ha='center', va='center', fontsize=9, fontweight='bold',
                   color=text_color)

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, y + row_height + 0.02)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Category Distribution: A Treemap View', fontsize=14, fontweight='bold', pad=20)

    save_figure(fig, '02_category_treemap.png')

# =============================================================================
# VISUALIZATION 3: Posting Rhythm (Radial/Clock)
# =============================================================================
def viz_03_posting_rhythm(metadata_df):
    """Radial chart showing posting patterns by day of week and time."""
    print("3. Posting Rhythm...")

    # Extract hour from datetime
    metadata_df['hour'] = pd.to_datetime(metadata_df['date']).dt.hour
    weekday_hour = metadata_df.groupby(['weekday', 'hour']).size().reset_index(name='count')

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})

    # Create radial bar chart
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    theta = np.linspace(0, 2*np.pi, 7, endpoint=False)

    # Aggregate by weekday
    weekday_totals = metadata_df['weekday'].value_counts().sort_index()
    radii = weekday_totals.values

    # Normalize
    radii_norm = radii / radii.max()

    colors = plt.cm.Blues(radii_norm * 0.6 + 0.3)
    bars = ax.bar(theta, radii_norm, width=0.7, bottom=0.2, color=colors,
                  edgecolor='white', linewidth=2)

    # Customize
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_xticks(theta)
    ax.set_xticklabels(days, fontsize=11, fontweight='bold')
    ax.set_yticks([])
    ax.set_ylim(0, 1.3)

    # Add value labels
    for bar, val, angle in zip(bars, radii, theta):
        ax.text(angle, bar.get_height() + 0.25, f'{val:,}',
               ha='center', va='bottom', fontsize=10, fontweight='bold',
               color=ENDEAVOUR_COLORS['primary'])

    ax.set_title('Posting Rhythm by Day of Week', fontsize=14, fontweight='bold', pad=20, y=1.05)
    ax.spines['polar'].set_visible(False)

    save_figure(fig, '03_posting_rhythm.png')

# =============================================================================
# VISUALIZATION 4: Word Count Distribution (Violin + Strip)
# =============================================================================
def viz_04_word_distribution(metadata_df):
    """Violin plot with overlaid strip plot showing word count distribution."""
    print("4. Word Count Distribution...")

    # Filter outliers for better visualization
    df = metadata_df[metadata_df['word_count'] < 2000].copy()
    df['year_group'] = pd.cut(df['year'], bins=[2007, 2012, 2017, 2022, 2026],
                              labels=['2008-2012', '2013-2017', '2018-2022', '2023-2025'])

    fig, ax = plt.subplots(figsize=(12, 6))

    # Violin plot
    parts = ax.violinplot([df[df['year_group'] == g]['word_count'].dropna()
                           for g in df['year_group'].unique() if pd.notna(g)],
                          positions=range(4), showmeans=True, showmedians=True)

    # Color the violins
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(plt.cm.Blues(0.4 + i * 0.15))
        pc.set_edgecolor(ENDEAVOUR_COLORS['primary'])
        pc.set_alpha(0.7)

    parts['cmeans'].set_color(ENDEAVOUR_COLORS['accent'])
    parts['cmedians'].set_color(ENDEAVOUR_COLORS['primary'])

    # Add jittered points
    for i, g in enumerate(['2008-2012', '2013-2017', '2018-2022', '2023-2025']):
        subset = df[df['year_group'] == g]['word_count'].dropna().sample(min(100, len(df[df['year_group'] == g])))
        jitter = np.random.normal(0, 0.05, len(subset))
        ax.scatter(i + jitter, subset, alpha=0.3, s=10, color=ENDEAVOUR_COLORS['accent2'])

    ax.set_xticks(range(4))
    ax.set_xticklabels(['2008-2012', '2013-2017', '2018-2022', '2023-2025'])
    ax.set_xlabel('Time Period', fontsize=12)
    ax.set_ylabel('Word Count', fontsize=12)
    ax.set_title('Evolution of Post Length Over Time', fontsize=14, fontweight='bold')

    # Add annotation
    ax.annotate('Longest posts cluster\nin middle period',
                xy=(1.5, 1500), xytext=(2.5, 1700),
                arrowprops=dict(arrowstyle='->', color=ENDEAVOUR_COLORS['muted']),
                fontsize=10, color=ENDEAVOUR_COLORS['muted'])

    save_figure(fig, '04_word_distribution.png')

# =============================================================================
# VISUALIZATION 5: Topic Evolution (Streamgraph-style)
# =============================================================================
def viz_05_topic_evolution(metadata_df):
    """Area chart showing evolution of major topics over time."""
    print("5. Topic Evolution...")

    # Get top categories
    top_cats = ['Math', 'Computing', 'Statistics', 'Science']

    yearly_cats = []
    for year in range(2008, 2026):
        year_data = metadata_df[metadata_df['year'] == year]
        row = {'year': year}
        for cat in top_cats:
            row[cat] = year_data['categories'].str.contains(cat, na=False).sum()
        yearly_cats.append(row)

    df = pd.DataFrame(yearly_cats)

    fig, ax = plt.subplots(figsize=(14, 6))

    colors = [ENDEAVOUR_COLORS['primary'], ENDEAVOUR_COLORS['accent'],
              ENDEAVOUR_COLORS['accent2'], ENDEAVOUR_COLORS['accent3']]

    ax.stackplot(df['year'], [df[cat] for cat in top_cats],
                 labels=top_cats, colors=colors, alpha=0.8)

    ax.set_xlim(2008, 2025)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Posts', fontsize=12)
    ax.set_title('Topic Evolution: The Rise and Flow of Ideas', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', frameon=False)

    # Add subtle grid
    ax.yaxis.grid(True, alpha=0.3, linestyle='--')

    save_figure(fig, '05_topic_evolution.png')

# =============================================================================
# VISUALIZATION 6: Lollipop Chart (Top Posts by Word Count)
# =============================================================================
def viz_06_lollipop_chart(metadata_df):
    """Lollipop chart showing longest posts."""
    print("6. Lollipop Chart (Longest Posts)...")

    top_posts = metadata_df.nlargest(15, 'word_count')[['title', 'word_count', 'year']].copy()
    top_posts['title'] = top_posts['title'].apply(lambda x: x[:40] + '...' if len(str(x)) > 40 else x)
    top_posts = top_posts.iloc[::-1]  # Reverse for bottom-to-top

    fig, ax = plt.subplots(figsize=(12, 8))

    y_pos = range(len(top_posts))
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(top_posts)))

    # Stems
    ax.hlines(y=y_pos, xmin=0, xmax=top_posts['word_count'], color=ENDEAVOUR_COLORS['muted'],
              alpha=0.4, linewidth=1)

    # Dots
    scatter = ax.scatter(top_posts['word_count'], y_pos, s=100, c=colors,
                        edgecolors=ENDEAVOUR_COLORS['primary'], linewidths=2, zorder=3)

    # Labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_posts['title'], fontsize=10)
    ax.set_xlabel('Word Count', fontsize=12)
    ax.set_title('The Long Reads: 15 Most Substantial Posts', fontsize=14, fontweight='bold')

    # Add word count labels
    for i, (wc, year) in enumerate(zip(top_posts['word_count'], top_posts['year'])):
        ax.annotate(f'{wc:,} ({year})', (wc + 30, i), va='center', fontsize=9,
                   color=ENDEAVOUR_COLORS['muted'])

    ax.set_xlim(0, top_posts['word_count'].max() * 1.15)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)

    save_figure(fig, '06_lollipop_longest.png')

# =============================================================================
# VISUALIZATION 7: Bump Chart (Category Rankings Over Time)
# =============================================================================
def viz_07_bump_chart(metadata_df):
    """Bump chart showing how category rankings changed over time."""
    print("7. Bump Chart (Category Rankings)...")

    # Get rankings per year for top categories
    top_cats = ['Math', 'Computing', 'Statistics', 'Science', 'Uncategorized']
    years = range(2010, 2025, 2)

    rankings = []
    for year in years:
        year_data = metadata_df[(metadata_df['year'] >= year-1) & (metadata_df['year'] <= year+1)]
        counts = {}
        for cat in top_cats:
            counts[cat] = year_data['categories'].str.contains(cat, na=False).sum()
        sorted_cats = sorted(counts.items(), key=lambda x: -x[1])
        for rank, (cat, _) in enumerate(sorted_cats, 1):
            rankings.append({'year': year, 'category': cat, 'rank': rank})

    df = pd.DataFrame(rankings)

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = {
        'Math': ENDEAVOUR_COLORS['primary'],
        'Computing': ENDEAVOUR_COLORS['accent'],
        'Statistics': ENDEAVOUR_COLORS['accent2'],
        'Science': ENDEAVOUR_COLORS['accent3'],
        'Uncategorized': ENDEAVOUR_COLORS['muted']
    }

    for cat in top_cats:
        cat_data = df[df['category'] == cat]
        ax.plot(cat_data['year'], cat_data['rank'], 'o-', linewidth=3, markersize=10,
               color=colors[cat], label=cat)

    ax.set_xlim(2009, 2025)
    ax.set_ylim(5.5, 0.5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1st', '2nd', '3rd', '4th', '5th'])
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Ranking', fontsize=12)
    ax.set_title('Category Rankings Through the Years', fontsize=14, fontweight='bold')
    ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), frameon=False)
    ax.xaxis.grid(True, alpha=0.3, linestyle='--')

    save_figure(fig, '07_bump_chart.png')

# =============================================================================
# VISUALIZATION 8: Waffle Chart (Fact Type Distribution)
# =============================================================================
def viz_08_waffle_chart(facts_df):
    """Waffle chart showing distribution of fact types."""
    print("8. Waffle Chart (Fact Types)...")

    type_counts = facts_df['type'].value_counts()
    total = type_counts.sum()

    # Normalize to 100 squares
    squares = (type_counts / total * 100).round().astype(int)

    # Adjust to exactly 100
    while squares.sum() != 100:
        if squares.sum() > 100:
            squares.loc[squares.idxmax()] -= 1
        else:
            squares.loc[squares.idxmax()] += 1

    fig, ax = plt.subplots(figsize=(10, 10))

    colors = {
        'otd': ENDEAVOUR_COLORS['primary'],
        'quirk': ENDEAVOUR_COLORS['accent'],
        'rarity': ENDEAVOUR_COLORS['accent2'],
        'density': ENDEAVOUR_COLORS['accent3'],
        'span': '#e53e3e',
        'constant': '#805ad5',
        'links': '#dd6b20',
        'first': '#38a169'
    }

    # Create grid
    square_idx = 0
    for row in range(10):
        for col in range(10):
            # Find which category this square belongs to
            cumsum = 0
            for cat, count in squares.items():
                cumsum += count
                if square_idx < cumsum:
                    color = colors.get(cat, ENDEAVOUR_COLORS['muted'])
                    break

            rect = mpatches.FancyBboxPatch(
                (col, 9-row), 0.9, 0.9,
                boxstyle="round,pad=0.02,rounding_size=0.1",
                facecolor=color, edgecolor='white', linewidth=1
            )
            ax.add_patch(rect)
            square_idx += 1

    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Fact Types at a Glance (each square = 1%)', fontsize=14, fontweight='bold', pad=20)

    # Legend
    legend_elements = [mpatches.Patch(facecolor=colors.get(cat, ENDEAVOUR_COLORS['muted']),
                                       label=f'{cat} ({count}%)')
                       for cat, count in squares.items()]
    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.02, 0.5),
             frameon=False, fontsize=10)

    save_figure(fig, '08_waffle_chart.png')

# =============================================================================
# VISUALIZATION 9: Connected Scatterplot (Posts vs Word Count Over Time)
# =============================================================================
def viz_09_connected_scatter(metadata_df):
    """Connected scatterplot showing relationship between posts and avg word count."""
    print("9. Connected Scatterplot...")

    yearly = metadata_df.groupby('year').agg({
        'id': 'count',
        'word_count': 'mean'
    }).reset_index()
    yearly.columns = ['year', 'posts', 'avg_words']

    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot line
    ax.plot(yearly['posts'], yearly['avg_words'], 'o-',
           color=ENDEAVOUR_COLORS['primary'], linewidth=2, markersize=8, alpha=0.7)

    # Add year labels
    for _, row in yearly.iterrows():
        offset = (5, 5) if row['year'] % 2 == 0 else (-5, -10)
        ax.annotate(str(int(row['year'])), (row['posts'], row['avg_words']),
                   textcoords='offset points', xytext=offset,
                   fontsize=9, color=ENDEAVOUR_COLORS['muted'])

    # Highlight interesting years
    ax.scatter(yearly[yearly['year'] == 2008]['posts'],
              yearly[yearly['year'] == 2008]['avg_words'],
              s=200, c=ENDEAVOUR_COLORS['accent'], zorder=5, label='2008 (Start)')
    ax.scatter(yearly[yearly['year'] == 2025]['posts'],
              yearly[yearly['year'] == 2025]['avg_words'],
              s=200, c=ENDEAVOUR_COLORS['accent2'], zorder=5, label='2025 (Latest)')

    ax.set_xlabel('Number of Posts', fontsize=12)
    ax.set_ylabel('Average Word Count', fontsize=12)
    ax.set_title('The Blog\'s Journey: Volume vs Depth', fontsize=14, fontweight='bold')
    ax.legend(frameon=False)

    save_figure(fig, '09_connected_scatter.png')

# =============================================================================
# VISUALIZATION 10: Dumbbell Chart (First vs Last Mention)
# =============================================================================
def viz_10_dumbbell_chart(facts_df):
    """Dumbbell chart showing span of topics from first to last mention."""
    print("10. Dumbbell Chart...")

    # Extract spans from facts
    span_facts = facts_df[facts_df['type'] == 'span'].copy()
    pattern = r"'(.+?)' spans the blog from (\d{4}) to (\d{4})"

    spans = []
    for fact in span_facts['fact']:
        match = re.search(pattern, fact)
        if match:
            spans.append({
                'topic': match.group(1),
                'start': int(match.group(2)),
                'end': int(match.group(3))
            })

    df = pd.DataFrame(spans).sort_values('start').head(12)

    fig, ax = plt.subplots(figsize=(12, 8))

    y_pos = range(len(df))

    # Draw connecting lines
    for i, row in df.iterrows():
        ax.plot([row['start'], row['end']], [list(df.index).index(i)] * 2,
               color=ENDEAVOUR_COLORS['muted'], linewidth=2, alpha=0.5)

    # Start points
    ax.scatter(df['start'], y_pos, s=120, c=ENDEAVOUR_COLORS['primary'],
              zorder=3, label='First Mention')

    # End points
    ax.scatter(df['end'], y_pos, s=120, c=ENDEAVOUR_COLORS['accent'],
              zorder=3, label='Last Mention')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(df['topic'], fontsize=10)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_title('Topic Longevity: First to Last Mention', fontsize=14, fontweight='bold')
    ax.legend(loc='lower right', frameon=False)
    ax.xaxis.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(2006, 2027)

    save_figure(fig, '10_dumbbell_chart.png')

# =============================================================================
# VISUALIZATION 11: Stylized Quote Card
# =============================================================================
def viz_11_quote_card(enriched_df):
    """Stylized quote card for memorable excerpts."""
    print("11. Quote Card...")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Background card
    card = FancyBboxPatch((0.5, 0.5), 9, 5,
                          boxstyle="round,pad=0.05,rounding_size=0.2",
                          facecolor=ENDEAVOUR_COLORS['light'],
                          edgecolor=ENDEAVOUR_COLORS['primary'],
                          linewidth=3)
    ax.add_patch(card)

    # Quote marks
    ax.text(1, 4.5, '"', fontsize=80, color=ENDEAVOUR_COLORS['primary'],
           alpha=0.3, fontfamily='serif', fontweight='bold')

    # Quote text
    quote = "The intersection of mathematics and computing\nis where the most interesting problems live."
    ax.text(5, 3.2, quote, fontsize=14, ha='center', va='center',
           color=ENDEAVOUR_COLORS['text'], style='italic', fontfamily='serif',
           linespacing=1.5)

    # Attribution
    ax.text(7, 1.2, "— John D. Cook", fontsize=12, ha='right',
           color=ENDEAVOUR_COLORS['muted'], fontweight='bold')

    # Accent line
    ax.plot([2, 8], [2, 2], color=ENDEAVOUR_COLORS['accent'], linewidth=3)

    ax.set_title('Stylized Quote Cards', fontsize=14, fontweight='bold', pad=20)

    save_figure(fig, '11_quote_card.png')

# =============================================================================
# VISUALIZATION 12: Circular Packing (Category Relationships)
# =============================================================================
def viz_12_circular_packing(metadata_df):
    """Simple circular packing showing category sizes."""
    print("12. Circular Packing...")

    # Count categories
    all_cats = metadata_df['categories'].dropna().str.split(';').explode()
    cat_counts = all_cats.value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 10))

    # Simple circle packing (approximate positions)
    positions = [
        (0, 0, 1.0),      # Math (largest, center)
        (1.5, 0.5, 0.5),  # Computing
        (-1.3, 0.8, 0.4), # Statistics
        (0.3, -1.5, 0.35),# Science
        (-1.2, -0.8, 0.3),
        (1.3, -0.8, 0.25),
        (-0.5, 1.3, 0.22),
        (1.5, 1.2, 0.2),
        (-1.5, -1.5, 0.18),
        (0.8, 1.5, 0.15),
    ]

    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(cat_counts)))

    for i, ((x, y, r), (cat, count)) in enumerate(zip(positions, cat_counts.items())):
        # Scale radius by count
        scaled_r = r * (count / cat_counts.max()) ** 0.5
        circle = plt.Circle((x, y), scaled_r, color=colors[i], alpha=0.8)
        ax.add_patch(circle)

        # Add label if big enough
        if scaled_r > 0.2:
            ax.text(x, y, f'{cat}\n{count:,}', ha='center', va='center',
                   fontsize=9 if scaled_r < 0.5 else 11, fontweight='bold',
                   color='white' if i < 5 else ENDEAVOUR_COLORS['text'])

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Category Universe: Proportional Representation', fontsize=14, fontweight='bold', pad=20)

    save_figure(fig, '12_circular_packing.png')

# =============================================================================
# MAIN
# =============================================================================
def main():
    """Generate all visualizations."""
    print("\n" + "="*60)
    print("VISUAL SAMPLER V2: Publication-Quality Showcase")
    print("="*60 + "\n")

    setup_style()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Loading data...")
    facts_df, metadata_df, enriched_df = load_data()
    print(f"  • {len(facts_df):,} facts")
    print(f"  • {len(metadata_df):,} posts")
    print(f"  • {len(enriched_df):,} enriched records\n")

    print("Generating visualizations...\n")

    viz_01_activity_heatmap(metadata_df)
    viz_02_category_treemap(metadata_df)
    viz_03_posting_rhythm(metadata_df)
    viz_04_word_distribution(metadata_df)
    viz_05_topic_evolution(metadata_df)
    viz_06_lollipop_chart(metadata_df)
    viz_07_bump_chart(metadata_df)
    viz_08_waffle_chart(facts_df)
    viz_09_connected_scatter(metadata_df)
    viz_10_dumbbell_chart(facts_df)
    viz_11_quote_card(enriched_df)
    viz_12_circular_packing(metadata_df)

    print("\n" + "="*60)
    print("✓ All 12 visualizations generated successfully!")
    print(f"  Output: {OUTPUT_DIR}/")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
