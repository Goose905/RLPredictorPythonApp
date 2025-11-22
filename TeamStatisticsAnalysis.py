#Author: Luke Zurad
#Last Modified: 1/20/2025
#Purspose:
# identifies which team statistics most influence match outcomes. Filters incomplete games data, computes team level 
# differential statistics for both the winning and losing team, and analyzes the relationships with match results. Calculations performed are
# Win correlations – correlations of each statistic with winning, showing direction and strength.
# Mann-Whitney U test – Statistical significance of each metric in distinguishing winning from losing.
# Results are saved to two seperate CSV files 


import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
from io import StringIO
import csv



# LOAD & CLEAN DATA
good_rows = []
with open("Sorted_Matches.csv", 'r', encoding='utf-8') as f:
    for line in f:
        values = line.strip().split(',')
        if len(values) != 427 or ',,' in line:
            continue
        good_rows.append(line)

df = pd.read_csv(StringIO(''.join(good_rows)))
df.columns = df.columns.str.strip()



# SELECT NUMERIC COLUMNS (exclude player names, car names, car ids)
numeric_cols = [c for c in df.columns if any(
    c.startswith(f"P{i} ") and 
    not c.endswith("player name") and 
    not c.endswith("car name") and 
    "car id" not in c
    for i in range(1, 7)
)]
# Split into winning/losing team columns
win_cols  = [c for c in numeric_cols if c.startswith(("P4 ", "P5 ", "P6 "))]
lose_cols = [c for c in numeric_cols if c.startswith(("P1 ", "P2 ", "P3 "))]
# Convert all to numeric
df[win_cols + lose_cols] = df[win_cols + lose_cols].apply(pd.to_numeric, errors="coerce").fillna(0)



# COMPUTE TEAM DIFFERENTIALS
team_diffs = []
for _, row in df.iterrows():
    win_stats  = row[win_cols].values
    lose_stats = row[lose_cols].values
    diff_vals  = win_stats - lose_stats
    # Winning team perspective
    diff_win = {f"diff_{win_cols[i][3:]}": diff_vals[i] for i in range(len(win_cols))}
    diff_win["win"] = 1
    team_diffs.append(diff_win)
    # Losing team perspective
    diff_lose = {f"diff_{win_cols[i][3:]}": -diff_vals[i] for i in range(len(win_cols))}
    diff_lose["win"] = 0
    team_diffs.append(diff_lose)
team_df = pd.DataFrame(team_diffs)



# REMOVE CONSTANT COLUMNS
numeric_team_cols = team_df.select_dtypes(include=np.number).columns
team_df = team_df.loc[:, numeric_team_cols[team_df[numeric_team_cols].std() != 0]]
# Remove any column containing 'car id'
team_df = team_df[[c for c in team_df.columns if "car id" not in c.lower()]]



# SAVE WIN CORRELATIONS
corr = team_df.corr(numeric_only=True)["win"].sort_values(ascending=False)
corr.to_csv("win_correlations.csv")



# MANN-WHITNEY U TESTS
results = []
for col in team_df.columns:
    if col in ["win", "match_id"]:
        continue
    winners = team_df[team_df["win"] == 1][col]
    losers  = team_df[team_df["win"] == 0][col]
    u, p = mannwhitneyu(winners, losers)
    results.append((col, u, p))
# Save to CSV
with open("win_mannwhitney.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["statistic", "U_statistic", "p_value"])
    for col, u, p in results:
        writer.writerow([col, u, p])