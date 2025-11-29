import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import defaultdict

# --- File Paths ---
METADATA_PATH = "data/posts_metadata.csv"
CATEGORIES_JSON_PATH = "data/wp_taxonomies/categories.json"
OUTPUT_DIR = "book/02-the-category-landscape/images"
TOP_CATEGORIES_CHART_PATH = os.path.join(OUTPUT_DIR, "top_categories.png")
CATEGORY_COOCCURRENCE_CHART_PATH = os.path.join(OUTPUT_DIR, "category_cooccurrence.png")

def get_category_names_from_string(category_str, id_to_name_map):
    """
    Parses a comma-separated string of category IDs or names and returns a list of category names.
    Handles mixed cases and attempts to resolve IDs to names.
    """
    if pd.isna(category_str) or category_str == '':
        return []

    parts = [x.strip() for x in category_str.split(',')]
    resolved_names = []

    for part in parts:
        if part.isdigit(): # Appears to be an ID
            cat_id = int(part)
            if cat_id in id_to_name_map:
                resolved_names.append(id_to_name_map[cat_id])
            # else: print(f"Warning: Category ID '{part}' not found in categories.json. Skipping.")
        else: # Appears to be a name
            # Check if the name exists in our map (case-insensitive for robustness)
            found = False
            for stored_id, stored_name in id_to_name_map.items():
                if stored_name.lower() == part.lower():
                    resolved_names.append(stored_name)
                    found = True
                    break
            # else: print(f"Warning: Category name '{part}' not found in categories.json. Skipping.")
    return resolved_names


def generate_chapter_2_visuals():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load categories map
    with open(CATEGORIES_JSON_PATH, 'r') as f:
        categories_data = json.load(f)
    category_id_to_name = {cat['id']: cat['name'] for cat in categories_data}
    category_name_to_id = {cat['name']: cat['id'] for cat in categories_data} # For reverse lookup if needed


    # Load post metadata
    df = pd.read_csv(METADATA_PATH)

    # --- Category Frequency Analysis ---
    all_post_categories = []
    for _, row in df.iterrows():
        post_cat_names = get_category_names_from_string(row['categories'], category_id_to_name)
        all_post_categories.extend(post_cat_names)
        
    category_counts = pd.Series(all_post_categories).value_counts().head(20) # Top 20 categories

    # --- Plot Top Categories ---
    plt.figure(figsize=(12, 8))
    sns.barplot(y=category_counts.index, x=category_counts.values, palette='viridis')
    plt.title('Top 20 Blog Categories by Post Count', fontsize=16)
    plt.xlabel('Number of Posts', fontsize=12)
    plt.ylabel('Category', fontsize=12)
    plt.tight_layout()
    plt.savefig(TOP_CATEGORIES_CHART_PATH, dpi=300)
    plt.close()
    print(f"Saved top categories chart to {TOP_CATEGORIES_CHART_PATH}")

    # --- Category Co-occurrence Analysis for specific categories ---
    # Target categories from BOOK_PLAN.md - ensure they match names in category_id_to_name
    # Mapping to canonical names to avoid case issues
    canonical_target_category_names = []
    for target_name in ['Math', 'Music', 'Clinical trials', 'Typography']:
        found = False
        for stored_name in category_name_to_id.keys():
            if stored_name.lower() == target_name.lower():
                canonical_target_category_names.append(stored_name)
                found = True
                break
        if not found:
            print(f"Warning: Target category '{target_name}' not found in canonical list. Skipping.")

    # Filter posts to only those containing at least one target category
    posts_with_target_categories_names = []
    for _, row in df.iterrows():
        post_cat_names = get_category_names_from_string(row['categories'], category_id_to_name)
        
        # Check if any of the post's categories are in our canonical target list
        if any(name in canonical_target_category_names for name in post_cat_names):
            posts_with_target_categories_names.append([name for name in post_cat_names if name in canonical_target_category_names])
    
    # Build co-occurrence matrix
    cooccurrence_matrix = defaultdict(lambda: defaultdict(int))
    for cat_list in posts_with_target_categories_names:
        # Create a unique set of categories for this post to avoid double counting if a category is listed multiple times
        unique_cats_in_post = list(set(cat_list)) 
        for i, cat1 in enumerate(unique_cats_in_post):
            for j, cat2 in enumerate(unique_cats_in_post):
                if i <= j: # Avoid double counting and ensure symmetry
                    cooccurrence_matrix[cat1][cat2] += 1
                    if cat1 != cat2: # Ensure symmetry
                        cooccurrence_matrix[cat2][cat1] += 1

    # Convert to DataFrame for heatmap
    cooccurrence_df = pd.DataFrame(cooccurrence_matrix).fillna(0)
    # Reindex to ensure consistent order
    cooccurrence_df = cooccurrence_df.reindex(index=canonical_target_category_names, columns=canonical_target_category_names, fill_value=0)

    # --- Plot Category Co-occurrence Heatmap ---
    plt.figure(figsize=(8, 7))
    sns.heatmap(cooccurrence_df, annot=True, fmt='g', cmap='Blues', linewidths=.5, linecolor='gray')
    plt.title('Co-occurrence of Key Categories', fontsize=16)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Category', fontsize=12)
    plt.tight_layout()
    plt.savefig(CATEGORY_COOCCURRENCE_CHART_PATH, dpi=300)
    plt.close()
    print(f"Saved co-occurrence chart to {CATEGORY_COOCCURRENCE_CHART_PATH}")


if __name__ == "__main__":
    generate_chapter_2_visuals()
