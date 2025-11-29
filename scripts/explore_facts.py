import pandas as pd

def explore_facts_data():
    """
    Analyzes the calendar facts data to understand the types of facts available.
    """
    try:
        df = pd.read_csv("data/johndcook_calendar_candidates_filtered.csv")
    except FileNotFoundError:
        print("Error: The facts file was not found.")
        return

    print("--- Fact Types and Counts ---")
    print(df['type'].value_counts())
    print("\n" + "="*30 + "\n")

    for fact_type in df['type'].unique():
        print(f"--- Sample of '{fact_type}' facts ---")
        sample_facts = df[df['type'] == fact_type].head(5)
        for _, row in sample_facts.iterrows():
            print(f"  - {row['fact']}")
        print("\n" + "="*30 + "\n")


if __name__ == "__main__":
    explore_facts_data()
