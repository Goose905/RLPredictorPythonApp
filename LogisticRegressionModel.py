#Author Luke Zurad
#Last Modified: 11/12/2025
#Purpose: Identifies the most impact in game statistic utilizing logistic regression modeling


import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from io import StringIO


#Remove incomplete games from dataframe
print("Filtering games with incomplete data...")
good_rows = []
bad_count = 0
with open("Sorted_Matches.csv", 'r', encoding='utf-8') as f:
    for line in f:
        values = line.strip().split(',')
        if len(values) != 427:
            bad_count += 1
            continue
        if ',,' in line:
            bad_count += 1
            continue
        good_rows.append(line)
print(f"Kept: {len(good_rows):,} | Dropped: {bad_count}")
df = pd.read_csv(StringIO(''.join(good_rows)))
print(f"Clean DataFrame: {df.shape}")



#Seperates winning and losing teams data
win_cols = [c for c in df.columns if c.startswith(('P1 ', 'P2 ', 'P3 '))]
lose_cols = [c for c in df.columns if c.startswith(('P4 ', 'P5 ', 'P6 '))]
win_df = df[['replay id', 'team name', 'opposing team name'] + win_cols].copy()
win_df['win'] = 1
lose_df = df[['replay id', 'opposing team name', 'team name'] + lose_cols].copy()
lose_df['win'] = 0
lose_df.rename(columns={'opposing team name': 'team name', 'team name': 'opposing team name'}, inplace=True)
model_df = pd.concat([win_df, lose_df], ignore_index=True)



# Cleans numeric data
print("\nCleaning numeric values...")
def clean_numeric_column(col):
    return pd.to_numeric(
        col.astype(str)
           .str.strip()
           .str.replace(',', '', regex=False)
           .str.replace(r'[^0-9.\-]', '0', regex=True)
           .replace(['', 'nan', 'inf', '-inf', 'null', 'None', 'N/A'], '0'),
        errors='coerce'
    ).fillna(0)
feature_cols = [c for c in model_df.columns if c not in ['replay id', 'team name', 'opposing team name', 'win']]
X = model_df[feature_cols].apply(clean_numeric_column)
y = model_df['win']
print(f"Final: {X.shape[1]} features × {len(y):,} samples | NaNs: {X.isna().sum().sum()}")



# Trains data with standard scaling (75% training, 25% testing) and 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)
model = LogisticRegression(max_iter=3000, n_jobs=-1, random_state=42)
model.fit(X_train_s, y_train)



# Displays Model Statisitc
y_pred = model.predict(X_test_s)
print(f"\nAccuracy Score: {accuracy_score(y_test, y_pred):.1%}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Lose', 'Win']))



# Displays Top 60 Features Correlation
coef_df = pd.DataFrame({'feature': X.columns, 'coef': model.coef_[0]})
print("\nTOP 60 WIN PREDICTORS:")
print(coef_df.reindex(coef_df.coef.abs().sort_values(ascending=False).index).head(60)[['feature', 'coef']].round(4))
