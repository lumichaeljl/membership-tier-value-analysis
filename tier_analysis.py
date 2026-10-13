"""
Membership tier value analysis
Dataset: Telco Customer Churn (Kaggle, blastchar)
Tiers = Contract type (Month-to-month, One year, Two year)

Run:  python tier_analysis.py
Needs: pip install pandas matplotlib
Put WA_Fn-UseC_-Telco-Customer-Churn.csv in the same folder.
"""
import pandas as pd
import matplotlib.pyplot as plt

FILE = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
log = []  # cleaning log = your proof for "job #1"

# ---------- 1. LOAD ----------
df = pd.read_csv(FILE)
log.append(f"Loaded {len(df)} rows, {df.shape[1]} columns.")

# ---------- 2. CLEAN ----------
# duplicates
dupes = df.duplicated(subset="customerID").sum()
df = df.drop_duplicates(subset="customerID")
log.append(f"Removed {dupes} duplicate customerIDs.")

# TotalCharges is text in the raw file; blanks become NaN
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
blank = df["TotalCharges"].isna().sum()
log.append(
    f"Found {blank} blank TotalCharges (customers with tenure 0, no bill yet). "
    "Dropped them since they have no revenue history."
)
df = df.dropna(subset=["TotalCharges"])

# trim whitespace in text columns so categories match
text_cols = df.select_dtypes(include=["object", "string"]).columns
df[text_cols] = df[text_cols].apply(lambda s: s.str.strip())

# churn Yes/No -> 1/0
df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)
log.append("Converted Churn Yes/No to 1/0 (ChurnFlag).")
log.append(f"Final clean rows: {len(df)}.")

# ---------- 3. TIER METRICS ----------
order = ["Month-to-month", "One year", "Two year"]
g = df.groupby("Contract")
tiers = pd.DataFrame({
    "customers": g.size(),
    "pct_of_customers": (g.size() / len(df) * 100).round(1),
    "avg_monthly_charge": g["MonthlyCharges"].mean().round(2),
    "avg_tenure_months": g["tenure"].mean().round(1),
    "churn_rate_pct": (g["ChurnFlag"].mean() * 100).round(1),
    "avg_total_revenue": g["TotalCharges"].mean().round(2),
    "total_revenue": g["TotalCharges"].sum().round(0),
}).reindex(order)

# rough value per customer = avg monthly charge x avg tenure
tiers["est_value_per_customer"] = (
    tiers["avg_monthly_charge"] * tiers["avg_tenure_months"]
).round(2)
tiers["pct_of_revenue"] = (
    tiers["total_revenue"] / tiers["total_revenue"].sum() * 100
).round(1)

tiers.to_csv("tier_summary.csv")
df.to_csv("clean_customers.csv", index=False)

# ---------- 4. CHARTS ----------
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
colors = ["#c0392b", "#e0a030", "#2e8b57"]

tiers["est_value_per_customer"].plot(kind="bar", ax=axes[0], color=colors)
axes[0].set_title("Est. value per customer ($)")

tiers["churn_rate_pct"].plot(kind="bar", ax=axes[1], color=colors)
axes[1].set_title("Churn rate (%)")

tiers["pct_of_revenue"].plot(kind="bar", ax=axes[2], color=colors)
axes[2].set_title("Share of total revenue (%)")

for ax in axes:
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=15)
plt.tight_layout()
plt.savefig("tier_charts.png", dpi=150)

# ---------- 5. WRITE-UP DRAFT ----------
best = tiers["est_value_per_customer"].idxmax()
worst_churn = tiers["churn_rate_pct"].idxmax()
summary = f"""# Membership Tier Value Analysis

## Data
Telco Customer Churn (Kaggle), tiers = contract type.

## Cleaning log
""" + "\n".join(f"- {x}" for x in log) + f"""

## Results
{tiers.to_markdown()}

## Findings
- Highest value per customer: **{best}** (${tiers.loc[best, 'est_value_per_customer']}).
- Highest churn: **{worst_churn}** ({tiers.loc[worst_churn, 'churn_rate_pct']}%).
- (Add your own takeaway + recommendation here.)

## Caveats
- Data is a snapshot, so tenure is time so far, not full lifetime.
- Value = avg monthly charge x avg tenure, a rough estimate.
- With real winery data I'd tier by actual club membership level
  and use real renewal dates for retention.
"""
with open("summary.md", "w") as f:
    f.write(summary)

print("\n".join(log))
print()
print(tiers.T)
print("\nSaved: tier_summary.csv, clean_customers.csv, tier_charts.png, summary.md")