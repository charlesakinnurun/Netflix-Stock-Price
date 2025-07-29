import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv', parse_dates=['Date'])

# Add a column for the day of the week (Monday=0, Sunday=6)
df['Weekday'] = df['Date'].dt.day_name()

# Calculate the average daily return for each weekday
avg_return_by_weekday = df.groupby('Weekday')['Daily_Return'].mean()

# Sort by average return (descending)
avg_return_by_weekday = avg_return_by_weekday.sort_values(ascending=False)

print("Average daily return by weekday (highest to lowest):")
print(avg_return_by_weekday)