import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv', parse_dates=['Date'])

# Extract year and quarter
df['Year'] = df['Date'].dt.year
df['Quarter'] = df['Date'].dt.quarter

# Calculate daily return if not present
if 'Daily_Return' not in df.columns or df['Daily_Return'].isnull().all():
    df['Daily_Return'] = df['Close'].pct_change()

# Group by year and quarter, then sum the daily returns to get total growth per quarter
quarterly_growth = df.groupby(['Year', 'Quarter'])['Daily_Return'].sum().reset_index()

# Calculate the average growth per quarter across all years
avg_growth_by_quarter = quarterly_growth.groupby('Quarter')['Daily_Return'].mean().sort_values(ascending=False)

print("Average stock growth by quarter (highest to lowest):")
print(avg_growth_by_quarter)