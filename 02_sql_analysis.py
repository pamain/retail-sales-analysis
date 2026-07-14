"""
Retail Sales Performance Analysis
Step 2: SQL Analysis (SQLite)
"""
import sqlite3
import pandas as pd

# Load cleaned data into SQLite
conn = sqlite3.connect(':memory:')
df = pd.read_csv('cleaned_superstore.csv', parse_dates=['Order Date', 'Ship Date'])
df.to_sql('sales', conn, index=False, if_exists='replace')

def run_query(title, query):
    print(f"\n{'='*70}\n{title}\n{'='*70}")
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))
    return result

# 1. Top 10 products by revenue
q1 = run_query("TOP 10 PRODUCTS BY REVENUE", """
    SELECT "Product Name", Category,
           ROUND(SUM(Sales), 2) AS total_revenue,
           ROUND(SUM(Profit), 2) AS total_profit,
           SUM(Quantity) AS units_sold
    FROM sales
    GROUP BY "Product Name", Category
    ORDER BY total_revenue DESC
    LIMIT 10
""")

# 2. Monthly sales trend
q2 = run_query("MONTHLY SALES TREND (first 12 rows)", """
    SELECT "Order YearMonth" AS month,
           ROUND(SUM(Sales), 2) AS revenue,
           ROUND(SUM(Profit), 2) AS profit,
           COUNT(DISTINCT "Order ID") AS num_orders
    FROM sales
    GROUP BY month
    ORDER BY month
    LIMIT 12
""")

# 3. Regional performance
q3 = run_query("REGIONAL PERFORMANCE", """
    SELECT Region,
           ROUND(SUM(Sales), 2) AS total_revenue,
           ROUND(SUM(Profit), 2) AS total_profit,
           ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin_pct,
           ROUND(AVG(Discount), 3) AS avg_discount,
           COUNT(DISTINCT "Order ID") AS num_orders
    FROM sales
    GROUP BY Region
    ORDER BY total_revenue DESC
""")

# 4. Category / Sub-category profitability
q4 = run_query("CATEGORY & SUB-CATEGORY PROFITABILITY", """
    SELECT Category, "Sub-Category",
           ROUND(SUM(Sales), 2) AS total_revenue,
           ROUND(SUM(Profit), 2) AS total_profit,
           ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin_pct
    FROM sales
    GROUP BY Category, "Sub-Category"
    ORDER BY total_profit ASC
    LIMIT 10
""")

# 5. Customer segment analysis
q5 = run_query("CUSTOMER SEGMENT ANALYSIS", """
    SELECT Segment,
           COUNT(DISTINCT "Customer ID") AS num_customers,
           ROUND(SUM(Sales), 2) AS total_revenue,
           ROUND(SUM(Sales) / COUNT(DISTINCT "Customer ID"), 2) AS revenue_per_customer,
           ROUND(SUM(Profit), 2) AS total_profit
    FROM sales
    GROUP BY Segment
    ORDER BY total_revenue DESC
""")

# 6. Discount impact on profit
q6 = run_query("DISCOUNT IMPACT ON PROFITABILITY", """
    SELECT
        CASE
            WHEN Discount = 0 THEN '0% (no discount)'
            WHEN Discount <= 0.2 THEN '1-20%'
            WHEN Discount <= 0.4 THEN '21-40%'
            ELSE '41%+'
        END AS discount_band,
        COUNT(*) AS num_orders,
        ROUND(SUM(Sales), 2) AS total_revenue,
        ROUND(SUM(Profit), 2) AS total_profit,
        ROUND(AVG(Profit), 2) AS avg_profit_per_order
    FROM sales
    GROUP BY discount_band
    ORDER BY discount_band
""")

# 7. Region + discount cross-analysis (to find the underperforming region insight)
q7 = run_query("REGION x DISCOUNT BAND (avg discount per region)", """
    SELECT Region,
           ROUND(AVG(Discount), 3) AS avg_discount,
           ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin_pct,
           ROUND(SUM(Sales), 2) AS revenue
    FROM sales
    GROUP BY Region
    ORDER BY profit_margin_pct ASC
""")

conn.close()
print("\n\nAll queries executed successfully.")
