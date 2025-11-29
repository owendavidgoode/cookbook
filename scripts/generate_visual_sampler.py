import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
import re

# --- File Paths ---
CALENDAR_FACTS_PATH = "data/johndcook_calendar_candidates_filtered.csv"
METADATA_PATH = "data/posts_metadata.csv"
ENRICHED_POSTS_PATH = "data/johndcook_posts_enriched.jsonl"
OUTPUT_DIR = "book/visual_sampler/images"

def setup_plot_style(style_name='seaborn-v0_8-whitegrid', title='Visualization Title', xlabel='X-axis', ylabel='Y-axis', figsize=(10, 6)):
    plt.style.use(style_name)
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(title, fontsize=16, pad=15)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    return fig, ax

def save_and_close(fig, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {filepath}")

# --- Helper for Stylized "Tweet" Graphic ---
def create_stylized_tweet(fact_text, author="John D. Cook", handle="@johndcook", date="Nov 28, 2025",
                          likes="~1.2K", retweets="~250", filename="stylized_tweet.png"):
    fig, ax = plt.subplots(figsize=(8, 4), facecolor='#1DA1F2') # Twitter Blue
    ax.set_facecolor('#1DA1F2') # Twitter Blue
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Profile Picture (simple circle)
    circle = plt.Circle((0.1, 0.8), 0.08, color='white', transform=ax.transAxes, clip_on=False)
    ax.add_patch(circle)

    # Name and Handle
    ax.text(0.2, 0.85, author, color='white', fontsize=12, fontweight='bold', transform=ax.transAxes)
    ax.text(0.2, 0.78, handle, color='#BDCCD6', fontsize=10, transform=ax.transAxes) # Light grey

    # Date
    ax.text(0.7, 0.78, date, color='#BDCCD6', fontsize=10, transform=ax.transAxes, ha='right')

    # Fact Text
    # Use textwrap to break long lines
    # Wrapped for display within the 'tweet' box
    wrapped_text = '\n'.join(re.findall('.{1,60}(?:\s|$)', fact_text)) # roughly 60 chars per line
    ax.text(0.1, 0.65, wrapped_text, color='white', fontsize=11, wrap=True, transform=ax.transAxes, va='top')

    # Engagement
    ax.text(0.1, 0.05, f"❤️ {likes}  🔁 {retweets}", color='#BDCCD6', fontsize=9, transform=ax.transAxes)

    save_and_close(fig, filename)


# --- Visualization 1: Top Categories (from 'quirk' facts) ---
def visualize_top_categories(calendar_facts_df):
    quirk_facts = calendar_facts_df[calendar_facts_df['type'] == 'quirk'].copy()
    
    # Extract category name and count from the 'fact' string
    # e.g., "The 'Math' category contains 2378 posts."
    category_pattern = re.compile(r"The '(.*?)' category contains (\d+) posts.")
    
    data = []
    for fact_text in quirk_facts['fact']:
        match = category_pattern.match(fact_text)
        if match:
            category_name = match.group(1)
            post_count = int(match.group(2))
            data.append({'category': category_name, 'count': post_count})
            
    if not data:
        print("No 'quirk' facts found for category visualization.")
        return

    df_categories = pd.DataFrame(data).sort_values(by='count', ascending=False).head(15) # Top 15

    fig, ax = setup_plot_style(style_name='fivethirtyeight',
                               title='Top 15 Categories by Post Count (from "Quirk" Facts)',
                               xlabel='Number of Posts',
                               ylabel='Category',
                               figsize=(12, 8))

    sns.barplot(x='count', y='category', data=df_categories, ax=ax, palette='viridis')

    # Add data labels
    for index, row in df_categories.iterrows():
        ax.text(row['count'] + 50, index, f"{row['count']}", color='black', ha="left", va='center')

    ax.set_xlim(right=df_categories['count'].max() * 1.1) # Extend x-axis for labels
    save_and_close(fig, "top_categories_quirk.png")

# --- Visualization 2: Post Word Count Distribution (from 'density' facts) ---
def visualize_word_count_distribution(calendar_facts_df, posts_metadata_df):
    density_facts = calendar_facts_df[calendar_facts_df['type'] == 'density'].copy()

    # Extract word counts from the fact text, e.g., "The #1 longest post is ... with 1,926 words"
    word_count_pattern = re.compile(r".*?with ([\d,]+) words.*?")
    longest_posts = []
    for fact_text in density_facts['fact']:
        match = word_count_pattern.match(fact_text)
        if match:
            longest_posts.append(int(match.group(1).replace(',', '')))
    
    # Get all word counts from metadata for distribution
    all_word_counts = posts_metadata_df['word_count'].dropna()

    fig, ax = setup_plot_style(style_name='ggplot',
                               title='Distribution of Blog Post Word Counts',
                               xlabel='Word Count',
                               ylabel='Density',
                               figsize=(12, 7))

    sns.histplot(all_word_counts, bins=50, kde=True, ax=ax, color='skyblue', edgecolor='black', stat='density')
    
    # Highlight the longest posts from facts, if they are in the all_word_counts
    for wc in longest_posts:
        if wc in all_word_counts.values: # Check if the specific word count exists in the actual data
            ax.axvline(wc, color='red', linestyle='--', linewidth=1, label=f'Longest Post ({wc} words)')

    if longest_posts:
        handles, labels = ax.get_legend_handles_labels()
        if not labels: # Add legend only if no labels exist
            ax.legend()
    
    save_and_close(fig, "word_count_distribution.png")


# --- Visualization 3: Topic Spans (from 'span' facts) ---
def visualize_topic_spans(calendar_facts_df):
    span_facts = calendar_facts_df[calendar_facts_df['type'] == 'span'].copy()
    
    # Extract topic, start_year, end_year from fact string
    # e.g., "'Gamma Function' spans the blog from 2008 to 2025: first in..."
    span_pattern = re.compile(r"'(.*?)' spans the blog from (\d{4}) to (\d{4}):.*")
    
    data = []
    for fact_text in span_facts['fact']:
        match = span_pattern.match(fact_text)
        if match:
            topic = match.group(1)
            start_year = int(match.group(2))
            end_year = int(match.group(3))
            data.append({'topic': topic, 'start_year': start_year, 'end_year': end_year})
            
    if not data:
        print("No 'span' facts found for topic span visualization.")
        return

    df_spans = pd.DataFrame(data).sort_values(by='start_year').head(10) # Top 10 for clarity

    # Create a simple timeline (Gantt-like) chart
    fig, ax = setup_plot_style(style_name='seaborn-v0_8-pastel',
                               title='Topic Longevity on the Blog (Sample from "Span" Facts)',
                               xlabel='Year',
                               ylabel='Topic',
                               figsize=(14, 8))

    # Plotting horizontal bars for each topic's span
    for i, row in df_spans.reset_index().iterrows():
        ax.barh(y=row['topic'], width=(row['end_year'] - row['start_year'] + 1), left=row['start_year'], height=0.6,
                color=sns.color_palette('tab10')[i % 10])
        # Add text for start and end years
        ax.text(row['start_year'] - 0.5, i, str(row['start_year']), va='center', ha='right', fontsize=9)
        ax.text(row['end_year'] + 0.5, i, str(row['end_year']), va='center', ha='left', fontsize=9)

    ax.set_yticks(df_spans['topic'])
    ax.set_yticklabels(df_spans['topic'], fontsize=10)
    ax.set_xticks(range(df_spans['start_year'].min() - 1, df_spans['end_year'].max() + 2, 2)) # Adjust x-ticks
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    save_and_close(fig, "topic_spans.png")


# --- Main Function to Generate All Visuals for Sampler ---
def generate_sampler_visuals():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load dataframes
    calendar_facts_df = pd.read_csv(CALENDAR_FACTS_PATH)
    posts_metadata_df = pd.read_csv(METADATA_PATH)
    # enriched_posts_df = pd.read_json(ENRICHED_POSTS_PATH, lines=True) # Will load when needed for tweet

    # Generate Visualizations
    visualize_top_categories(calendar_facts_df)
    visualize_word_count_distribution(calendar_facts_df, posts_metadata_df)
    visualize_topic_spans(calendar_facts_df)
    
    # Example for stylized tweet: Take a fact and visualize it
    tweet_fact = calendar_facts_df[calendar_facts_df['type'] == 'otd'].iloc[0]['fact']
    create_stylized_tweet(tweet_fact, filename="otd_tweet_example.png")


if __name__ == "__main__":
    generate_sampler_visuals()
