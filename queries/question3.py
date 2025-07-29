import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv')

# Filter the DataFrame to include only rows where 'Close' price is above $500
above_500_days = df[df['Close'] > 500]

# Count the number of days
num_days = len(above_500_days)

print(f"The stock price closed above $500 on {num_days} days.")