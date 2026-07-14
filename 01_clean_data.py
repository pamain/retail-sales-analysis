"""
Retail Sales Performance Analysis
Step 1: Data Cleaning
"""
import pandas as pd
import numpy as np

# Load raw data
df = pd.read_csv('raw_data.csv', encoding='utf-8-sig')

print("=== RAW DATA OVERVIEW ===")
print(f"Shape: {df.shape}")
print(f"\nColumn dtypes:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"\nDuplicate rows: {df.duplicated().sum()}")

# --- Cleaning steps ---

# 1. Parse dates (format is D/M/YYYY based on inspection, e.g. 16/1/2016)
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')

# 2. Drop exact duplicate rows if any
before = len(df)
df = df.drop_duplicates()
print(f"\nDropped {before - len(df)} duplicate rows")

# 3. Standardize text columns (strip whitespace)
text_cols = ['Customer Name', 'Segment', 'Country', 'City', 'State', 'Region',
             'Category', 'Sub-Category', 'Product Name']
for col in text_cols:
    df[col] = df[col].astype(str).str.strip()

# 4. Feature engineering for analysis
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order YearMonth'] = df['Order Date'].dt.to_period('M').astype(str)
df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
df['Profit Margin'] = df['Profit'] / df['Sales']
df['Profit Margin'] = df['Profit Margin'].replace([np.inf, -np.inf], np.nan)

# 5. Sanity checks
print(f"\nDate range: {df['Order Date'].min()} to {df['Order Date'].max()}")
print(f"Negative sales rows: {(df['Sales'] < 0).sum()}")
print(f"Rows with negative profit: {(df['Profit'] < 0).sum()}")

# Save cleaned data
df.to_csv('cleaned_superstore.csv', index=False)
print(f"\nCleaned data saved: {df.shape[0]} rows, {df.shape[1]} columns")
print("=> cleaned_superstore.csv")
