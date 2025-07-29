import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv', parse_dates=['Date'])

# Extract year and month
df['year_month'] = df['Date'].dt.to_period('M')

# Sort by date to ensure correct order
df = df.sort_values('Date')

# Group by year_month
result = []
for ym, group in df.groupby('year_month'):
    # Check if every day's close is greater than the previous day's close
    closes = group['Close'].values
    if all(closes[i] > closes[i-1] for i in range(1, len(closes))):
        result.append(str(ym))

if result:
    print("Months where the closing price consistently increased:", result)
else:
    print("No month found where the closing price consistently increased every trading day.")