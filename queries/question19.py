import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv', parse_dates=['Date'])

# Sort by date to ensure correct order
df = df.sort_values('Date')

# Get the first and last row
first_row = df.iloc[0]
last_row = df.iloc[-1]

print(f"First date: {first_row['Date'].date()}, Closing price: {first_row['Close']}")
print(f"Last date: {last_row['Date'].date()}, Closing price: {last_row['Close']}")