import pandas as pd

# Load the spreadsheet
file_path = 'nutritions.csv'  # Update with the actual path to your CSV file
nutrient_data = pd.read_csv(file_path)

def search_ingredient_by_name(ingredient_name, nutrient_data):
    # Iterate through each part to find matching ingredients
    matches = nutrient_data[nutrient_data['ingredient_description'].str.contains(f"^{ingredient_name}", case=False, na=False, regex=True)]
    if not matches.empty:
        return matches.drop_duplicates()  # Return the first match found and stop searching
    
    return pd.DataFrame()

