import pandas as pd
import os

def load_destinations():
    """
    Loads destination data from the CSV file and ensures all
    cost columns are numeric so calculations don't fail silently.
    Returns a clean pandas DataFrame.
    """
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'destinations.csv')
    try:
        df = pd.read_csv(csv_path)

        # Cast all numeric columns explicitly — prevents "string + int" errors
        numeric_cols = [
            'Avg_Travel_Cost', 'Avg_Hotel_Per_Day',
            'Avg_Food_Per_Day_Per_Person', 'Avg_Local_Travel_Per_Day',
            'Avg_Shopping_Cost', 'Recommended_Days'
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Standardize text columns so comparisons are case-insensitive
        if 'Type' in df.columns:
            df['Type'] = df['Type'].str.strip().str.capitalize()
        if 'Budget_Level' in df.columns:
            df['Budget_Level'] = df['Budget_Level'].str.strip().str.capitalize()

        return df
    except FileNotFoundError:
        print(f"Error: {csv_path} not found.")
        return pd.DataFrame()
