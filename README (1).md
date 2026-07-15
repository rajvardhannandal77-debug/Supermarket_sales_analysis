# Supermarket Sales — Data Cleaning & Analysis

Data cleaning and exploratory analysis of a supermarket sales dataset (1,000 transactions
across 3 branches), prepared as a foundation for a BI dashboard (Power BI / Tableau / Looker Studio).

## Dataset

Source: `data/supermarket_sales.csv` — point-of-sale records with 17 fields including
invoice ID, branch, city, customer type, gender, product line, pricing, tax, payment
method, and customer rating.

## Project Structure

```
.
├── data/
│   ├── supermarket_sales.csv            # raw data
│   └── supermarket_sales_cleaned.csv    # cleaned output (generated)
├── supermarket_sales_analysis.ipynb     # full notebook: cleaning + EDA
├── data_cleaning.py                     # standalone cleaning script
├── requirements.txt
└── README.md
```

## Data Cleaning Steps

1. **Standardized column names** — lowercase, snake_case, no special characters.
2. **Removed duplicate rows** — checked with `.duplicated()` (0 found in this dataset,
   logic included for reusability on other extracts).
3. **Handled missing values** — numeric columns imputed with median, categorical
   columns with mode (0 nulls found in this dataset; logic included for reuse).
4. **Fixed data types** — merged `date` + `time` into a proper `datetime` column,
   cast numeric fields, cast categorical fields (`branch`, `city`, `customer_type`,
   `gender`, `product_line`, `payment`) to `category` dtype.
5. **Removed unnecessary columns** — dropped `gross_margin_percentage`, which is a
   constant 4.76% across every row and carries no analytical value.
6. **Feature engineering** — derived `hour`, `day_of_week`, `month`, and `is_weekend`
   from the transaction datetime to support time-based dashboard slicing.
7. **Outlier check** — boxplots included for visual inspection; outliers are **not**
   auto-removed by default since large totals may represent genuine bulk purchases
   (a commented-out IQR-based removal function is available in `data_cleaning.py`
   if you want a stricter version).

## How to Run

```bash
pip install -r requirements.txt
python data_cleaning.py          # runs the cleaning pipeline, outputs cleaned CSV
jupyter notebook supermarket_sales_analysis.ipynb   # full walkthrough + EDA
```

## Suggested Dashboard KPIs

**Revenue & Profitability**
- Total Revenue (`total`)
- Total Gross Income / Profit (`gross_income`)
- Total COGS
- Gross Margin % (income / revenue)
- Average Transaction Value (basket size)
- Revenue Growth Trend (day-over-day / month-over-month)

**Sales Volume**
- Total Transactions (invoice count)
- Total Units Sold (`quantity`)
- Average Units per Transaction

**Branch / Location Performance**
- Revenue by Branch (A/B/C)
- Revenue by City
- Best/worst performing branch by margin

**Product Performance**
- Revenue by Product Line
- Units Sold by Product Line
- Top 5 / Bottom 5 Product Lines by revenue
- Average Unit Price by Product Line

**Customer Insights**
- Revenue Split: Member vs. Normal customer
- Revenue Split: Male vs. Female
- Average Rating by Product Line / Branch
- Repeat vs. one-time customer behavior (if extended with customer IDs)

**Payment Behavior**
- Revenue Share by Payment Method (Cash / Credit Card / Ewallet)
- Average Transaction Value by Payment Method

**Time-Based Trends**
- Revenue by Hour of Day (peak hours)
- Revenue by Day of Week
- Weekday vs. Weekend Revenue
- Monthly Revenue Trend

**Customer Satisfaction**
- Average Rating overall
- Rating Trend over time
- Correlation between Rating and Spend

## Next Steps

- Connect `supermarket_sales_cleaned.csv` to Power BI / Tableau / Looker Studio.
- Build visuals for each KPI group above (cards for top-line metrics, bar/line
  charts for trends, a slicer panel for branch/city/product line/payment method).
- Optionally load the cleaned data into a database (PostgreSQL/BigQuery) for a
  live-connected dashboard instead of a static CSV import.
