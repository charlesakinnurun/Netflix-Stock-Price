import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv')

# Calculate the correlation between Open and Close prices
correlation = df['Open'].corr(df['Close'])

print(f"Correlation between opening and closing prices: {correlation:.4f}")