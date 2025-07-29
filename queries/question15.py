import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv')

# Calculate the standard deviation of the closing price
std_close = df['Close'].std()

print(f"Standard deviation of the closing price: {std_close:.2f}")