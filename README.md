# Retail Sales Performance Analysis

Analysis of ~10,000 orders from a US retail Superstore (2014–2017) to identify
revenue drivers, regional profitability gaps, and the impact of discounting
on margins. Built using Python, SQL, Excel, and Power BI.

## Tools Used
- **Python** (Pandas, NumPy, Matplotlib) — data cleaning, feature engineering, exploratory analysis
- **SQL** (SQLite) — aggregation queries for revenue, profit, and segment analysis
- **Excel** — summary workbook with pivot-ready tables
- **Power BI** — interactive dashboard (see `/dashboard` screenshot)

## Key Insights
- **Central region underperforms despite steady revenue**: it carries the highest
  average discount rate (24%) of any region and the lowest profit margin (7.9%),
  compared to the West region's 14.9% margin at a 10.9% average discount —
  suggesting discounting strategy, not demand, is driving the profit gap.
- **Deep discounts destroy margin**: orders discounted above 20% are net
  unprofitable as a group (-$35.8K and -$99.6K in total profit for the
  21–40% and 41%+ discount bands respectively), while undiscounted orders
  generated $321K in profit.
- **Furniture Tables is a loss-making sub-category**: -8.6% profit margin
  on $207K in revenue, driven by heavy discounting on high-ticket items.
- **Q4 (Sep–Dec) consistently drives the highest revenue months** across
  all four years, useful for inventory and staffing planning.

## Files
- `01_clean_data.py` — data cleaning & feature engineering
- `02_sql_analysis.py` — SQL queries (SQLite) for core business questions
- `03_charts.py` — exploratory visualizations
- `04_excel_export.py` — Excel summary workbook generator
- `cleaned_superstore.csv` — cleaned dataset (Power BI data source)
- `Superstore_Analysis_Summary.xlsx` — summary tables by region, category, segment
- `/charts` — exported PNG visualizations

## Recommendation
Cap discounts on the Central region and Furniture > Tables sub-category at
~15% (in line with the West region's profitable discount range), and
re-evaluate pricing on high-ticket furniture items before offering
promotional discounts.
