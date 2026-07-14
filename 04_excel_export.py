"""
Retail Sales Performance Analysis
Step 4: Export summary tables to Excel (for Power BI / recruiter-friendly deliverable)
"""
import pandas as pd

df = pd.read_csv('cleaned_superstore.csv', parse_dates=['Order Date', 'Ship Date'])

with pd.ExcelWriter('Superstore_Analysis_Summary.xlsx', engine='openpyxl') as writer:
    # Cleaned raw data (for Power BI import)
    df.to_excel(writer, sheet_name='Cleaned_Data', index=False)

    # Regional performance
    region = df.groupby('Region').agg(
        Total_Revenue=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Avg_Discount=('Discount', 'mean'),
        Orders=('Order ID', 'nunique')
    ).reset_index()
    region['Profit_Margin_%'] = round(region['Total_Profit'] / region['Total_Revenue'] * 100, 2)
    region.to_excel(writer, sheet_name='Regional_Performance', index=False)

    # Category/Sub-category profitability
    cat = df.groupby(['Category', 'Sub-Category']).agg(
        Total_Revenue=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum')
    ).reset_index()
    cat['Profit_Margin_%'] = round(cat['Total_Profit'] / cat['Total_Revenue'] * 100, 2)
    cat = cat.sort_values('Total_Profit')
    cat.to_excel(writer, sheet_name='Category_Profitability', index=False)

    # Monthly trend
    monthly = df.groupby('Order YearMonth').agg(
        Revenue=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index()
    monthly.to_excel(writer, sheet_name='Monthly_Trend', index=False)

    # Customer segment
    seg = df.groupby('Segment').agg(
        Customers=('Customer ID', 'nunique'),
        Total_Revenue=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum')
    ).reset_index()
    seg['Revenue_per_Customer'] = round(seg['Total_Revenue'] / seg['Customers'], 2)
    seg.to_excel(writer, sheet_name='Customer_Segments', index=False)

    # Discount bands
    df['Discount_Band'] = pd.cut(
        df['Discount'], bins=[-0.01, 0, 0.2, 0.4, 1],
        labels=['0% (none)', '1-20%', '21-40%', '41%+']
    )
    disc = df.groupby('Discount_Band', observed=True).agg(
        Orders=('Order ID', 'nunique'),
        Total_Revenue=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum')
    ).reset_index()
    disc.to_excel(writer, sheet_name='Discount_Impact', index=False)

print("Excel workbook saved: Superstore_Analysis_Summary.xlsx")
print("Sheets: Cleaned_Data, Regional_Performance, Category_Profitability, Monthly_Trend, Customer_Segments, Discount_Impact")
