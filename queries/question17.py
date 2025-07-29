import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv')

# Calculate the correlation between Volume and Price_Change
correlation = df['Volume'].corr(df['Price_Change'])

print(f"Correlation between trading volume and price change: {correlation:.4f}")