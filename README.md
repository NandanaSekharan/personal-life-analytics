# Personal Life Analytics: A Data-Driven Behavioral Pattern Study

A multi-participant analytics project examining relationships between sleep,
spending, screen time, and workout habits, using a custom data collection
pipeline (Google Forms) combined with a modeled dataset to enable
time-based pattern analysis.

## ⚠️ Data Note (read first)
This dataset combines **9 real responses** collected via a Google Form from
friends/family (`data_source = "real"`) with **216 synthetically generated
daily records** (`data_source = "synthetic"`) built around each real
participant's baseline habits. The synthetic data was generated because
long-term (multi-week) self-tracking was still in progress at submission
time. A built-in behavioral rule (poor sleep → higher next-day spending and
screen time) was intentionally coded into the generator to demonstrate the
lag-correlation analysis technique — the specific correlation values below
partly reflect this designed pattern, not an independently verified
real-world effect. The pipeline (form → cleaning → analysis) is real and
reusable; as more real responses come in, the synthetic portion can be
phased out.

## Project Overview
- Built a data collection pipeline using Google Forms + Sheets to gather
  daily behavioral data from multiple participants.
- Cleaned inconsistent real-world survey data (mixed date formats,
  free-text sleep entries, spending ranges) with Python and pandas.
- Generated a companion synthetic dataset to extend single-day snapshots
  into a 24-day time series per participant, enabling lag-correlation
  analysis.
- Performed same-day and next-day (lag) correlation analysis, plus
  weekday-vs-weekend comparison.

## Tech Stack
- Python (pandas, numpy, matplotlib, seaborn)
- Google Forms + Google Sheets (real data collection)

## Files
- `generate_combined_data.py` — cleans real form data and generates the
  synthetic multi-day dataset
- `analyze_combined.py` — full analysis script (stats, correlation, charts)
- `combined_data.csv` — combined dataset (`data_source` column marks
  real vs. synthetic rows)
- `chart_correlation_heatmap.png` — same-day correlation across variables
- `chart_lag_sleep_vs_spend.png` — previous day's sleep vs. today's spend
- `chart_avg_sleep_by_person.png` — average sleep hours per participant
- `chart_spend_by_category.png` — spending breakdown by category
- `chart_weekday_vs_weekend.png` — weekday vs. weekend comparison

## Key Findings (on the combined dataset)
- Same-day sleep hours and spending show a weak negative correlation
  (r ≈ -0.09); sleep hours and screen time show a weak negative
  correlation (r ≈ -0.15).
- Previous day's sleep hours vs. today's spend: r ≈ -0.25 (by design,
  since the synthetic generator encodes this relationship).
- Previous day's sleep hours vs. today's screen time: r ≈ -0.17.
- Food was the most common spending category, followed by Shopping.
- Weekday vs. weekend averages were similar in this dataset, with slightly
  higher weekday spending and screen time.

## Next Steps
- Replace synthetic rows with real daily responses as data collection
  continues (target: 3-4 weeks per participant).
- Once enough real data exists, re-run the analysis on real-only data and
  compare against the synthetic-informed results here.
- Build an interactive Streamlit dashboard for exploring individual
  participant trends.

## Author
Built as part of a personal data analytics portfolio project.
