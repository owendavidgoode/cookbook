import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define file paths
METADATA_PATH = "data/posts_metadata.csv"
OUTPUT_DIR = "book/01-17-years-in-numbers/images"
YEARLY_CHART_PATH = os.path.join(OUTPUT_DIR, "posts_per_year.png")
MONTHLY_CHART_PATH = os.path.join(OUTPUT_DIR, "posts_per_month.png")

def generate_visuals():
    """
    Analyzes post metadata and generates visualizations for Chapter 1.
    """
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load the data
    try:
        df = pd.read_csv(METADATA_PATH)
    except FileNotFoundError:
        print(f"Error: Metadata file not found at {METADATA_PATH}")
        return

    # Convert 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'])

    # --- Generate Posts per Year Chart ---
    yearly_counts = df['year'].value_counts().sort_index()

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    sns.barplot(x=yearly_counts.index, y=yearly_counts.values, ax=ax, color='#3498db')

    ax.set_title('Blog Posts per Year (2008-2025)', fontsize=18, pad=20)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Posts', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add data labels
    for i, v in enumerate(yearly_counts.values):
        ax.text(i, v + 10, str(v), color='black', ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(YEARLY_CHART_PATH, dpi=300)
    print(f"Saved yearly chart to {YEARLY_CHART_PATH}")

    plt.close(fig) # Close the figure to free memory

    # --- Generate Posts per Month Chart ---
    monthly_counts = df['month'].value_counts().sort_index()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_counts.index = [month_names[i-1] for i in monthly_counts.index]


    fig, ax = plt.subplots(figsize=(12, 7))

    sns.barplot(x=monthly_counts.index, y=monthly_counts.values, ax=ax, palette='viridis')

    ax.set_title('Total Blog Posts by Month (All Years)', fontsize=18, pad=20)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Total Number of Posts', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Add data labels
    for i, v in enumerate(monthly_counts.values):
        ax.text(i, v + 10, str(v), color='black', ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(MONTHLY_CHART_PATH, dpi=300)
    print(f"Saved monthly chart to {MONTHLY_CHART_PATH}")
    plt.close(fig)


if __name__ == "__main__":
    generate_visuals()
