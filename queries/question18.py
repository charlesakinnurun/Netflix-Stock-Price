import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv')

# Count the number of trading days
num_days = len(df)

print(f"Number of trading days in the dataset: {num_days}")