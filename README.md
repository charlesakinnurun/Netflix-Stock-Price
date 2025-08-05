# Introduction
![Netflix](assets/netflix.jpg)
***
This dataset, named Netflix_stock_data_cleaned.csv, contains daily stock information for Netflix (NFLX) from May 2002 to June 2025. It includes key financial metrics and calculated indicators that are essential for stock market analysis.
🔍 SQL queries? Check them out [here](/queries/):
# Background
Driven by a quest to understand and analyze the historical performance of Netflix stock. Leveraging comprehensive Netflix stock data, the aim is to pinpoint key metrics impacting its stock price, identify trends, and uncover actionable insights into its market behavior. This analysis focuses on daily stock prices, trading volume, and calculated indicators such as daily returns and moving averages, to maximize understanding of Netflix's stock dynamics.
# Questions
Here are 20 questions you can ask based on your uploaded dataset Netflix_stock_data_cleaned.csv. These cover a variety of data analysis categories including trends, comparisons, statistics, and predictions:
### 📊 Descriptive Analysis
1. What is the average closing price of Netflix stock in the dataset?
2. What is the highest and lowest closing price recorded?
3. How many days did the stock price close above $500?
4. What is the average daily trading volume?
5. On which date did Netflix have the highest trading volume?
### 📈 Trend & Time Series Analysis
6. How did the stock price trend over time — was there a general upward or downward trend?
7. Which year/month had the highest average closing price?
8. What was the percentage change in closing price from the beginning to the end of the dataset?
9. Was there any month where the stock price consistently increased?
10. During which months did Netflix stock show the most volatility (highest price range)?
### 📊 Comparative Analysis
11. What is the average open vs. close price? Did it usually close higher or lower?
12. Compare the average trading volume across different years.
13. Were there more gains (Close > Open) or losses (Close < Open) over the dataset?
14. On which days of the week does Netflix stock tend to perform best?
### 🧮 Statistical Questions
15. What is the standard deviation of the closing price?
16. What is the correlation between opening and closing prices?
17. What is the correlation between volume and price change?
### 📅 Time-based Questions
18. How many trading days are in the dataset?
19. What was the closing price on the first and last date in the dataset?
20. Which quarter of the year had the highest stock growth historically?
# Tools I Used
For my deep dive into the digital advertising strategies, I harnessed the power of several key tools:
- **Pandas:** Essential python library used for data manipulation, analysis, and cleaning.
- **SQL:** The backbone of my analysis, allowing me to query the database and unearth critical insights.
- **MySQL:** The chosen database management system, ideal for handling the job posting data.
- **Visual Studio Code:** My go-to for database management and executing SQL queries.
- **Git & GitHub:** Essential for version control and sharing my SQL scripts and analysis, ensuring collaboration and project tracking.
- **Numpy:** Essential for numerical and scientific computing. It's especially important in data analysis,data science and machine Learning.
# Database Creation
```sql
CREATE SCHEMA `netflix_stock_data` ;
```
# Table Creation
```sql
CREATE TABLE netflix(
    Date DATE,
    Close FLOAT,
    High FLOAT,
    Low FLOAT,
    Open FLOAT,
    Volume FLOAT,
    Daily_Return FLOAT,
    Price_Range FLOAT,
    Price_Change FLOAT,
    Volume_MA7 INT,
    Close_MA7 FLOAT,
    Close_MA30 FLOAT
);
```
# The Cleaning
```python
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
```
# The Analysis
### Were there more gains (Close > Open) or losses (Close < Open) over the dataset?
```python
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
```
### What is the standard deviation of the closing price?
```python
import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv')

# Calculate the standard deviation of the closing price
std_close = df['Close'].std()

print(f"Standard deviation of the closing price: {std_close:.2f}")
```
### What is the correlation between volume and price change?
```python
import pandas as pd

# Load the data
df = pd.read_csv('datasets/Netflix_stock_data_cleaned.csv')

# Calculate the correlation between Volume and Price_Change
correlation = df['Volume'].corr(df['Price_Change'])

print(f"Correlation between trading volume and price change: {correlation:.4f}")
```
The remaining queries are provided below.
[Queries](/queries/)
# What I Learned
Throughout this adventure, I've turbocharged my data analysis toolkit with some serious firepower using Pandas:
- **🧩 Advanced Data Manipulation:** Mastered the art of advanced data handling, filtering, and transforming DataFrames like a pro, wielding methods for complex data restructuring and cleaning.
- **📊 Data Aggregation:** Got cozy with groupby() and turned aggregate functions like count(), mean(), and sum() into my data-summarizing sidekicks, along with pivot_table for comprehensive data views.
- **💡 Analytical Wizardry:** Leveled up my real-world puzzle-solving skills, turning questions into actionable, insightful Pandas operations and analyses.
# Conclusions
This project, by analyzing the Netflix stock data, has provided valuable insights into understanding its historical performance and market behavior. The findings from this analysis serve as a guide to identifying key metrics and trends that impact stock value. Investors and analysts can gain a deeper understanding of market dynamics by focusing on high-impact indicators like daily returns, trading volume, and moving averages. This exploration highlights the importance of continuous data analysis and adaptation to emerging market trends to ensure informed decision-making and a deeper understanding of market dynamics.
