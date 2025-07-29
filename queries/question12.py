import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv', parse_dates=['Date'])

# Extract the year from the Date column
df['Year'] = df['Date'].dt.year

# Group by year and calculate the average trading volume
avg_volume_by_year = df.groupby('Year')['Volume'].mean()

print("Average trading volume by year:")
print(avg_volume_by_year)