import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv')

# Count gains and losses
gains = (df['Close'] > df['Open']).sum()
losses = (df['Close'] < df['Open']).sum()
equal = (df['Close'] == df['Open']).sum()

print(f"Number of gain days (Close > Open): {gains}")
print(f"Number of loss days (Close < Open): {losses}")
print(f"Number of days with no change (Close == Open): {equal}")

if gains > losses:
    print("There were more gains than losses over the dataset.")
elif losses > gains:
    print("There were more losses than gains over the dataset.")
else:
    print("The number of gains and losses were equal over the dataset.")