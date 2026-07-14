"""
Retail Sales Performance Analysis
Step 3: Exploratory Charts (matplotlib)
"""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned_superstore.csv', parse_dates=['Order Date'])

plt.style.use('seaborn-v0_8-whitegrid') if 'seaborn-v0_8-whitegrid' in plt.style.available else None

# Chart 1: Monthly revenue trend
monthly = df.groupby('Order YearMonth').agg(revenue=('Sales','sum')).reset_index()
fig, ax = plt.subplots(figsize=(12,5))
ax.plot(monthly['Order YearMonth'], monthly['revenue'], marker='o', linewidth=1.5, markersize=3, color='#2563eb')
ax.set_title('Monthly Revenue Trend (2014-2017)', fontsize=14, fontweight='bold')
ax.set_xlabel('Month')
ax.set_ylabel('Revenue ($)')
ax.set_xticks(ax.get_xticks()[::3])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('chart1_monthly_trend.png', dpi=150)
plt.close()

# Chart 2: Profit margin by region
region = df.groupby('Region').agg(revenue=('Sales','sum'), profit=('Profit','sum')).reset_index()
region['margin_pct'] = region['profit'] / region['revenue'] * 100
region = region.sort_values('margin_pct')
fig, ax = plt.subplots(figsize=(8,5))
colors = ['#dc2626' if m < 10 else '#2563eb' for m in region['margin_pct']]
ax.barh(region['Region'], region['margin_pct'], color=colors)
ax.set_title('Profit Margin by Region', fontsize=14, fontweight='bold')
ax.set_xlabel('Profit Margin (%)')
for i, v in enumerate(region['margin_pct']):
    ax.text(v + 0.2, i, f'{v:.1f}%', va='center')
plt.tight_layout()
plt.savefig('chart2_region_margin.png', dpi=150)
plt.close()

# Chart 3: Discount vs Profit relationship
fig, ax = plt.subplots(figsize=(8,5))
sample = df.sample(min(2000, len(df)), random_state=42)
ax.scatter(sample['Discount'], sample['Profit'], alpha=0.3, s=10, color='#2563eb')
ax.axhline(0, color='#dc2626', linestyle='--', linewidth=1)
ax.set_title('Discount vs Profit (per order)', fontsize=14, fontweight='bold')
ax.set_xlabel('Discount Rate')
ax.set_ylabel('Profit ($)')
plt.tight_layout()
plt.savefig('chart3_discount_vs_profit.png', dpi=150)
plt.close()

# Chart 4: Sub-category profit (top and bottom performers)
subcat = df.groupby('Sub-Category').agg(profit=('Profit','sum')).reset_index().sort_values('profit')
fig, ax = plt.subplots(figsize=(9,6))
colors = ['#dc2626' if p < 0 else '#16a34a' for p in subcat['profit']]
ax.barh(subcat['Sub-Category'], subcat['profit'], color=colors)
ax.set_title('Total Profit by Sub-Category', fontsize=14, fontweight='bold')
ax.set_xlabel('Profit ($)')
ax.axvline(0, color='black', linewidth=0.8)
plt.tight_layout()
plt.savefig('chart4_subcategory_profit.png', dpi=150)
plt.close()

print("4 charts saved: chart1_monthly_trend.png, chart2_region_margin.png, chart3_discount_vs_profit.png, chart4_subcategory_profit.png")
