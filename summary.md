# Membership Tier Value Analysis

## Data
Telco Customer Churn (Kaggle), tiers = contract type.

## Cleaning log
- Loaded 7043 rows, 21 columns.
- Removed 0 duplicate customerIDs.
- Found 11 blank TotalCharges (customers with tenure 0, no bill yet). Dropped them since they have no revenue history.
- Converted Churn Yes/No to 1/0 (ChurnFlag).
- Final clean rows: 7032.

## Results
| Contract       |   customers |   pct_of_customers |   avg_monthly_charge |   avg_tenure_months |   churn_rate_pct |   avg_total_revenue |   total_revenue |   est_value_per_customer |   pct_of_revenue |
|:---------------|------------:|-------------------:|---------------------:|--------------------:|-----------------:|--------------------:|----------------:|-------------------------:|-----------------:|
| Month-to-month |        3875 |               55.1 |                66.4  |                18   |             42.7 |             1369.25 |     5.30586e+06 |                  1195.2  |             33   |
| One year       |        1472 |               20.9 |                65.08 |                42.1 |             11.3 |             3034.68 |     4.46705e+06 |                  2739.87 |             27.8 |
| Two year       |        1685 |               24   |                60.87 |                57.1 |              2.8 |             3728.93 |     6.28325e+06 |                  3475.68 |             39.1 |

## Findings
- Highest value per customer: **Two year** ($3475.68).
- Highest churn: **Month-to-month** (42.7%).
- (Add your own takeaway + recommendation here.)

## Caveats
- Data is a snapshot, so tenure is time so far, not full lifetime.
- Value = avg monthly charge x avg tenure, a rough estimate.
- With real winery data I'd tier by actual club membership level
  and use real renewal dates for retention.
