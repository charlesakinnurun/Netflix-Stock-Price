import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv')

# Find the row with the highest 'Volume'
highest_volume_day = df.loc[df['Volume'].idxmax()]

# Get the date and the volume
date_highest_volume = highest_volume_day['Date']
highest_volume = highest_volume_day['Volume']

print(f"Netflix had the highest trading volume of {highest_volume:,.0f} on {date_highest_volume}.")