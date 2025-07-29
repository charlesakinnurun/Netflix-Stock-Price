import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def clean_netflix_data(file_path):
    """
    Clean Netflix stock data by handling missing values, outliers, and data quality issues.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    print("Loading Netflix stock data...")
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    print(f"Original data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Display initial data info
    print("\nInitial data info:")
    print(df.info())
    print("\nFirst few rows:")
    print(df.head())
    print("\nLast few rows:")
    print(df.tail())
    
    # 1. Check for missing values
    print("\n=== Checking for missing values ===")
    missing_values = df.isnull().sum()
    print("Missing values per column:")
    print(missing_values)
    
    # 2. Convert Date column to datetime
    print("\n=== Converting Date column to datetime ===")
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
    
    # Check for invalid dates
    invalid_dates = df[df['Date'].isnull()]
    if len(invalid_dates) > 0:
        print(f"Found {len(invalid_dates)} rows with invalid dates")
        print(invalid_dates)
        # Remove rows with invalid dates
        df = df.dropna(subset=['Date'])
    
    # 3. Convert numeric columns to appropriate data types
    print("\n=== Converting numeric columns ===")
    numeric_columns = ['Close', 'High', 'Low', 'Open', 'Volume']
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 4. Check for and handle outliers
    print("\n=== Checking for outliers ===")
    
    # Remove rows where any price is negative or zero
    price_columns = ['Close', 'High', 'Low', 'Open']
    for col in price_columns:
        invalid_prices = df[df[col] <= 0]
        if len(invalid_prices) > 0:
            print(f"Found {len(invalid_prices)} rows with invalid {col} prices (<= 0)")
            df = df[df[col] > 0]
    
    # Check for logical inconsistencies (High < Low, etc.)
    logical_errors = df[
        (df['High'] < df['Low']) |
        (df['Open'] < 0) |
        (df['Close'] < 0) |
        (df['Volume'] < 0)
    ]
    
    if len(logical_errors) > 0:
        print(f"Found {len(logical_errors)} rows with logical errors")
        print(logical_errors)
        # Remove logically inconsistent rows
        df = df[
            (df['High'] >= df['Low']) &
            (df['Open'] >= 0) &
            (df['Close'] >= 0) &
            (df['Volume'] >= 0)
        ]
    
    # 5. Handle extreme outliers using IQR method
    print("\n=== Handling extreme outliers ===")
    
    for col in numeric_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        if len(outliers) > 0:
            print(f"Found {len(outliers)} outliers in {col} column")
            # For stock data, we'll be more conservative and only remove extreme outliers
            extreme_lower = Q1 - 3 * IQR
            extreme_upper = Q3 + 3 * IQR
            extreme_outliers = df[(df[col] < extreme_lower) | (df[col] > extreme_upper)]
            if len(extreme_outliers) > 0:
                print(f"Removing {len(extreme_outliers)} extreme outliers from {col}")
                df = df[(df[col] >= extreme_lower) & (df[col] <= extreme_upper)]
    
    # 6. Sort by date
    print("\n=== Sorting by date ===")
    df = df.sort_values('Date').reset_index(drop=True)
    
    # 7. Check for duplicate dates
    print("\n=== Checking for duplicate dates ===")
    duplicates = df[df.duplicated(subset=['Date'], keep=False)]
    if len(duplicates) > 0:
        print(f"Found {len(duplicates)} duplicate dates")
        print(duplicates)
        # Keep the first occurrence of each date
        df = df.drop_duplicates(subset=['Date'], keep='first')
    
    # 8. Add derived columns
    print("\n=== Adding derived columns ===")
    
    # Daily return
    df['Daily_Return'] = df['Close'].pct_change()
    
    # Price range
    df['Price_Range'] = df['High'] - df['Low']
    
    # Price change
    df['Price_Change'] = df['Close'] - df['Open']
    
    # Volume moving average (7-day)
    df['Volume_MA7'] = df['Volume'].rolling(window=7).mean()
    
    # Price moving averages
    df['Close_MA7'] = df['Close'].rolling(window=7).mean()
    df['Close_MA30'] = df['Close'].rolling(window=30).mean()
    
    # 9. Final data quality check
    print("\n=== Final data quality check ===")
    print(f"Final data shape: {df.shape}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Total trading days: {len(df)}")
    
    # Check for any remaining missing values
    final_missing = df.isnull().sum()
    print("\nFinal missing values:")
    print(final_missing)
    
    # Summary statistics
    print("\n=== Summary statistics ===")
    print(df.describe())
    
    # 10. Save cleaned data
    output_file = file_path.replace('.csv', '_cleaned.csv')
    df.to_csv(output_file, index=False)
    print(f"\nCleaned data saved to: {output_file}")
    
    return df

def main():
    """Main function to clean the Netflix stock data."""
    file_path = "datasets/Netflix_stock_data.csv"
    
    try:
        cleaned_df = clean_netflix_data(file_path)
        
        print("\n=== Data Cleaning Summary ===")
        print("✅ Date column converted to datetime")
        print("✅ Numeric columns converted to appropriate types")
        print("✅ Invalid prices (<= 0) removed")
        print("✅ Logical inconsistencies removed")
        print("✅ Extreme outliers removed")
        print("✅ Duplicate dates removed")
        print("✅ Data sorted by date")
        print("✅ Derived columns added")
        print("✅ Cleaned data saved")
        
        print(f"\nFinal dataset contains {len(cleaned_df)} trading days")
        print(f"Date range: {cleaned_df['Date'].min().strftime('%Y-%m-%d')} to {cleaned_df['Date'].max().strftime('%Y-%m-%d')}")
        
    except Exception as e:
        print(f"Error during data cleaning: {str(e)}")
        raise

if __name__ == "__main__":
    main() 