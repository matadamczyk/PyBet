import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, classification_report, roc_curve
from sklearn.pipeline import Pipeline
import requests

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

API_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "2b7bfc08bffdd8d9edd0015c7c32f477"
}

def get_team_id(team_name):
    response = requests.get(f"{API_URL}/teams?search={team_name}", headers=HEADERS)
    data = response.json()
    if data["response"]:
        return data["response"][0]["team"]["id"]
    return None

def get_last_10_matches(team_id):
    response = requests.get(f"{API_URL}/fixtures?team={team_id}&last=10", headers=HEADERS)
    data = response.json()
    return data["response"]

def calculate_form(matches, team_id):
    form = 0
    for match in matches:
        if match["teams"]["home"]["id"] == team_id:
            if match["teams"]["home"]["winner"]:
                form += 3
            elif match["teams"]["home"]["winner"] is None:
                form += 1
        else:
            if match["teams"]["away"]["winner"]:
                form += 3
            elif match["teams"]["away"]["winner"] is None:
                form += 1
    return form

df = pd.read_csv("results_with_form.csv", encoding='latin1')

df = df.dropna()

df['HomeWin'] = (df['FTR'] == 'H').astype(int)
df['Draw'] = (df['FTR'] == 'D').astype(int)
df['AwayWin'] = (df['FTR'] == 'A').astype(int)

df['GoalDiff'] = df['FTHG'] - df['FTAG']
df['ShotsDiff'] = df['HS'] - df['AS']
df['ShotsOnTargetDiff'] = df['HST'] - df['AST']
df['CornersDiff'] = df['HC'] - df['AC']
df['FoulsDiff'] = df['HF'] - df['AF']
df['YellowsDiff'] = df['HY'] - df['AY']
df['RedsDiff'] = df['HR'] - df['AR']

features = ['GoalDiff', 'ShotsDiff', 'ShotsOnTargetDiff', 'CornersDiff', 'FoulsDiff', 'YellowsDiff', 'RedsDiff', 'HomeTeamForm', 'AwayTeamForm']

X = df[features]  # Cechy
y_home_win = df['HomeWin']  # Etykiety dla wygranej gospodarzy
y_draw = df['Draw']  # Etykiety dla remisu
y_away_win = df['AwayWin']  # Etykiety dla wygranej gości

X_train, X_test, y_train_home, y_test_home = train_test_split(X, y_home_win, test_size=0.2, random_state=42, stratify=y_home_win)
_, _, y_train_draw, y_test_draw = train_test_split(X, y_draw, test_size=0.2, random_state=42, stratify=y_draw)
_, _, y_train_away, y_test_away = train_test_split(X, y_away_win, test_size=0.2, random_state=42, stratify=y_away_win)

scaler = StandardScaler()

models = {
    "Logistic Regression": LogisticRegression(random_state=42, C=0.00001),
    "Random Forest": RandomForestClassifier(random_state=42, n_estimators=10),
    "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=3),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42, n_estimators=10)
}

pipelines = {}
for model_name, model in models.items():
    pipelines[model_name] = Pipeline([
        ('scaler', scaler),
        ('model', model)
    ])

for model_name, pipeline in pipelines.items():
    pipeline.fit(X_train, y_train_home)

for model_name, pipeline in pipelines.items():
    y_pred_home = pipeline.predict(X_test)
    y_pred_proba_home = pipeline.predict_proba(X_test)[:, 1]  
    accuracy_home = accuracy_score(y_test_home, y_pred_home)
    roc_auc_home = roc_auc_score(y_test_home, y_pred_proba_home)
    conf_matrix_home = confusion_matrix(y_test_home, y_pred_home)
    
    print(f"\n{model_name} - Accuracy (Home Win):", accuracy_home)
    print(f"{model_name} - ROC AUC Score (Home Win):", roc_auc_home)
    print(f"\n{model_name} - Confusion Matrix (Home Win):\n", conf_matrix_home)
    print(f"\n{model_name} - Classification Report (Home Win):\n", classification_report(y_test_home, y_pred_home))
    
    fpr, tpr, _ = roc_curve(y_test_home, y_pred_proba_home)
    plt.figure()
    plt.plot(fpr, tpr, lw=2, label=f'{model_name} ROC curve (area = {roc_auc_home:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'{model_name} - Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()

team1_id = get_team_id("Tottenham")
team2_id = get_team_id("Chelsea")

team1_last_10_matches = get_last_10_matches(team1_id)
team2_last_10_matches = get_last_10_matches(team2_id)

team1_form = calculate_form(team1_last_10_matches, team1_id)
team2_form = calculate_form(team2_last_10_matches, team2_id)

tottenham_vs_chelsea = pd.DataFrame({
    'HomeTeam': ['Tottenham'],
    'AwayTeam': ['Chelsea'],
    'HomeTeamForm': [team1_form],
    'AwayTeamForm': [team2_form]
})

tottenham_vs_chelsea['GoalDiff'] = 0
tottenham_vs_chelsea['ShotsDiff'] = 0
tottenham_vs_chelsea['ShotsOnTargetDiff'] = 0
tottenham_vs_chelsea['CornersDiff'] = 0
tottenham_vs_chelsea['FoulsDiff'] = 0
tottenham_vs_chelsea['YellowsDiff'] = 0
tottenham_vs_chelsea['RedsDiff'] = 0

X_future = tottenham_vs_chelsea[features]

for model_name, pipeline in pipelines.items():
    future_predictions_proba_home = pipeline.predict_proba(X_future)[:, 1]
    future_predictions_proba_draw = pipeline.predict_proba(X_future)[:, 1]
    future_predictions_proba_away = pipeline.predict_proba(X_future)[:, 1]
    
    print(f"{model_name} - Szanse na wygraną Tottenhamu:", future_predictions_proba_home.mean())
    print(f"{model_name} - Szanse na remis:", future_predictions_proba_draw.mean())
    print(f"{model_name} - Szanse na wygraną Chelsea:", future_predictions_proba_away.mean())

    odds_home = 1 / future_predictions_proba_home.mean()
    odds_draw = 1 / future_predictions_proba_draw.mean()
    odds_away = 1 / future_predictions_proba_away.mean()

    print(f"{model_name} - Kurs na wygraną Tottenhamu:", odds_home)
    print(f"{model_name} - Kurs na remis:", odds_draw)
    print(f"{model_name} - Kurs na wygraną Chelsea:", odds_away)
