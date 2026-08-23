"""
Personal Life Analytics: Full Analysis
------------------------------------------
Analyzes combined (real + synthetic) multi-participant behavioral data.
Produces summary stats, correlation analysis (including 1-day lag), and
visualizations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# -----------------------------
# 1. LOAD DATA
# -----------------------------
df = pd.read_csv("combined_data.csv", parse_dates=["date"])
print("Shape:", df.shape)
print(df["data_source"].value_counts())

# -----------------------------
# 2. SUMMARY STATS
# -----------------------------
print("\n--- Summary Statistics ---")
print(df[["sleep_hours", "sleep_quality", "spend_inr", "screen_time"]].describe())

print("\n--- Category Breakdown ---")
print(df["category"].value_counts())

# -----------------------------
# 3. SAME-DAY CORRELATION
# -----------------------------
corr = df[["sleep_hours", "sleep_quality", "spend_inr", "screen_time", "worked_out"]].corr()
print("\n--- Same-day Correlation Matrix ---")
print(corr)

# -----------------------------
# 4. LAG CORRELATION (per person: yesterday's sleep vs today's spend/screen time)
# -----------------------------
df = df.sort_values(["name", "date"])
df["prev_sleep_hours"] = df.groupby("name")["sleep_hours"].shift(1)

lag_corr_spend = df["prev_sleep_hours"].corr(df["spend_inr"])
lag_corr_screen = df["prev_sleep_hours"].corr(df["screen_time"])

print(f"\nLag correlation (previous day's sleep vs today's spend): {lag_corr_spend:.3f}")
print(f"Lag correlation (previous day's sleep vs today's screen time): {lag_corr_screen:.3f}")

# -----------------------------
# 5. VISUALIZATIONS
# -----------------------------

# --- Correlation heatmap ---
plt.figure(figsize=(7, 5))
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.title("Same-Day Correlation: Sleep, Spend, Screen Time, Workout")
plt.tight_layout()
plt.savefig("chart_correlation_heatmap.png", dpi=150)
plt.close()

# --- Lag scatter: previous day's sleep vs today's spend ---
plt.figure(figsize=(7, 5))
sns.regplot(data=df, x="prev_sleep_hours", y="spend_inr",
            scatter_kws={"alpha": 0.4}, line_kws={"color": "red"})
plt.title(f"Previous Day's Sleep vs Today's Spend (r = {lag_corr_spend:.2f})")
plt.xlabel("Previous Day's Sleep Hours")
plt.ylabel("Today's Spend (₹)")
plt.tight_layout()
plt.savefig("chart_lag_sleep_vs_spend.png", dpi=150)
plt.close()

# --- Average sleep hours by person ---
plt.figure(figsize=(10, 5))
avg_sleep = df.groupby("name")["sleep_hours"].mean().sort_values()
sns.barplot(x=avg_sleep.values, y=avg_sleep.index, palette="Blues_d")
plt.title("Average Sleep Hours by Person")
plt.xlabel("Avg Sleep Hours")
plt.tight_layout()
plt.savefig("chart_avg_sleep_by_person.png", dpi=150)
plt.close()

# --- Spending by category ---
plt.figure(figsize=(7, 5))
category_totals = df.groupby("category")["spend_inr"].sum().sort_values(ascending=False)
sns.barplot(x=category_totals.index, y=category_totals.values, palette="Greens_d")
plt.title("Total Spending by Category (₹)")
plt.ylabel("Total Spend (₹)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("chart_spend_by_category.png", dpi=150)
plt.close()

# --- Weekday vs weekend spend/sleep ---
df["is_weekend"] = df["date"].dt.dayofweek >= 5
weekday_compare = df.groupby("is_weekend")[["sleep_hours", "spend_inr", "screen_time"]].mean()
weekday_compare.index = ["Weekday", "Weekend"]
print("\n--- Weekday vs Weekend Averages ---")
print(weekday_compare)

plt.figure(figsize=(8, 5))
weekday_compare.plot(kind="bar", ax=plt.gca())
plt.title("Weekday vs Weekend: Sleep, Spend, Screen Time")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart_weekday_vs_weekend.png", dpi=150)
plt.close()

print("\nAll charts saved. Analysis complete.")
