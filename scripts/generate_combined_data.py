"""
Personal Life Analytics: Data Generation
------------------------------------------
Combines real Google Form responses (9 entries, single-day snapshot) with
synthetic multi-day data per participant, so the dataset supports realistic
time-based (lag) correlation analysis.

IMPORTANT: The synthetic portion is clearly flagged via the `data_source`
column ("real" vs "synthetic") so the distinction is never hidden.
"""

import pandas as pd
import numpy as np
import re
from datetime import timedelta

np.random.seed(42)

# -----------------------------
# 1. LOAD REAL DATA
# -----------------------------
df_real = pd.read_csv("Untitled form.csv")
df_real.columns = [
    "timestamp", "name", "date_raw", "sleep_raw", "sleep_quality",
    "spend_raw", "category", "screen_time", "workout"
]

def clean_sleep(x):
    m = re.search(r'(\d+\.?\d*)', str(x))
    return float(m.group(1)) if m else None

def spend_midpoint(x):
    x = str(x).replace("₹", "").replace(",", "")
    nums = [int(n) for n in re.findall(r'\d+', x)]
    if len(nums) == 2:
        return sum(nums) / 2
    elif len(nums) == 1:
        return nums[0]
    return None

df_real["sleep_hours"] = df_real["sleep_raw"].apply(clean_sleep)
df_real["name"] = df_real["name"].str.strip()
df_real["worked_out"] = df_real["workout"].str.strip().str.lower().map({"yes": 1, "no": 0})
df_real["spend_inr"] = df_real["spend_raw"].apply(spend_midpoint)
df_real["screen_time"] = pd.to_numeric(df_real["screen_time"], errors="coerce")
df_real["sleep_quality"] = pd.to_numeric(df_real["sleep_quality"], errors="coerce")
df_real["date"] = pd.to_datetime("2026-08-12")  # anchor date for the real snapshot
df_real["data_source"] = "real"

real_clean = df_real[["name", "date", "sleep_hours", "sleep_quality",
                       "spend_inr", "category", "screen_time",
                       "worked_out", "data_source"]].copy()

participants = real_clean["name"].unique().tolist()
print(f"Real participants found: {participants}")

# -----------------------------
# 2. GENERATE SYNTHETIC MULTI-DAY DATA PER PARTICIPANT
# -----------------------------
# Each participant gets a baseline profile (derived loosely around their
# real single-day entry) plus 24 additional synthetic days, with a built-in
# behavioral pattern: poor sleep -> higher next-day spending & screen time.

categories = ["Food", "Shopping", "Transport", "Entertainment", "Bills", "Other"]
n_days = 24
start_date = pd.to_datetime("2026-07-15")

synthetic_rows = []

for person in participants:
    base = real_clean[real_clean["name"] == person].iloc[0]
    base_sleep = base["sleep_hours"] if pd.notna(base["sleep_hours"]) else 7
    base_screen = base["screen_time"] if pd.notna(base["screen_time"]) else 6

    prev_sleep = base_sleep
    for d in range(n_days):
        date = start_date + timedelta(days=d)

        # Sleep hours: random walk around the person's baseline
        sleep_hours = np.clip(np.random.normal(base_sleep, 1.2), 3.5, 10.5)

        # Sleep quality loosely tracks sleep hours (1-5 scale)
        sleep_quality = int(np.clip(round(sleep_hours / 2), 1, 5))

        # Built-in pattern: less sleep YESTERDAY -> higher spend & screen time TODAY
        sleep_deficit = max(0, 7 - prev_sleep)
        spend_inr = max(0, np.random.normal(150 + sleep_deficit * 60, 80))
        screen_time = np.clip(np.random.normal(base_screen + sleep_deficit * 1.5, 2.5), 1, 14)

        worked_out = 1 if np.random.random() < (0.5 - 0.05 * sleep_deficit) else 0
        category = np.random.choice(categories, p=[0.35, 0.2, 0.15, 0.15, 0.1, 0.05])

        synthetic_rows.append({
            "name": person,
            "date": date,
            "sleep_hours": round(sleep_hours, 1),
            "sleep_quality": sleep_quality,
            "spend_inr": round(spend_inr),
            "category": category,
            "screen_time": round(screen_time, 1),
            "worked_out": worked_out,
            "data_source": "synthetic"
        })

        prev_sleep = sleep_hours

synthetic_df = pd.DataFrame(synthetic_rows)

# -----------------------------
# 3. COMBINE REAL + SYNTHETIC
# -----------------------------
combined = pd.concat([real_clean, synthetic_df], ignore_index=True)
combined = combined.sort_values(["name", "date"]).reset_index(drop=True)

print(f"\nTotal rows: {len(combined)} ({(combined['data_source']=='real').sum()} real, "
      f"{(combined['data_source']=='synthetic').sum()} synthetic)")

combined.to_csv("combined_data.csv", index=False)
print("Saved combined_data.csv")
