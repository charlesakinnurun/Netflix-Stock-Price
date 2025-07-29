import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv', parse_dates=['Date'])

# Extract year and month
df['year_month'] = df['Date'].dt.to_period('M')

# Calculate average price range (volatility) per month
monthly_volatility = df.groupby('year_month')['Price_Range'].mean()

# Find the month(s) with the highest average price range
max_volatility = monthly_volatility.max()
most_volatile_months = monthly_volatility[monthly_volatility == max_volatility]

print("Month(s) with the highest average price range (volatility):")
print(most_volatile_months)