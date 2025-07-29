import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv')

# Calculate averages
avg_open = df['Open'].mean()
avg_close = df['Close'].mean()

print(f"Average Open Price: {avg_open:.2f}")
print(f"Average Close Price: {avg_close:.2f}")

# Determine how often it closed higher or lower than it opened
higher = (df['Close'] > df['Open']).sum()
lower = (df['Close'] < df['Open']).sum()
equal = (df['Close'] == df['Open']).sum()

print(f"Days closed higher than open: {higher}")
print(f"Days closed lower than open: {lower}")
print(f"Days closed equal to open: {equal}")

if avg_close > avg_open:
    print("On average, Netflix stock closed higher than it opened.")
elif avg_close < avg_open:
    print("On average, Netflix stock closed lower than it opened.")
else:
    print("On average, Netflix stock closed at the same price as it opened.")