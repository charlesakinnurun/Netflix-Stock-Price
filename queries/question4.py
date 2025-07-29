import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv')

# Calculate the average daily trading volume
average_volume = df['Volume'].mean()

print(f"The average daily trading volume is: {average_volume:,.2f}")