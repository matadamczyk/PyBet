import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, classification_report, roc_curve
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
import requests

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

features = ['ShotsDiff', 'ShotsOnTargetDiff', 'CornersDiff', 'FoulsDiff', 'YellowsDiff', 'RedsDiff']

X = df[features]  # Features
y_home_win = df['HomeWin']  # Labels for home win
y_draw = df['Draw']  # Labels for draw
y_away_win = df['AwayWin']  # Labels for away win

X_train, X_test, y_train_home, y_test_home = train_test_split(X, y_home_win, test_size=0.2, random_state=42, stratify=y_home_win)
_, _, y_train_draw, y_test_draw = train_test_split(X, y_draw, test_size=0.2, random_state=42, stratify=y_draw)
_, _, y_train_away, y_test_away = train_test_split(X, y_away_win, test_size=0.2, random_state=42, stratify=y_away_win)

smote = SMOTE(random_state=42)
X_train_smote, y_train_home_smote = smote.fit_resample(X_train, y_train_home)

scaler = StandardScaler()

log_reg = LogisticRegression(random_state=42, C=0.00001)

param_grid_rf = {
    'model__n_estimators': [10, 50, 100],
    'model__max_depth': [None, 10, 20, 30],
    'model__min_samples_split': [2, 5, 10],
    'model__min_samples_leaf': [1, 2, 4]
}
pipeline_rf = Pipeline([
    ('scaler', scaler),
    ('model', RandomForestClassifier(random_state=42))
])
grid_rf = GridSearchCV(pipeline_rf, param_grid_rf, cv=5, scoring='roc_auc')
grid_rf.fit(X_train_smote, y_train_home_smote)

param_grid_dt = {
    'model__max_depth': [3, 5, 10],
    'model__min_samples_split': [2, 5, 10],
    'model__min_samples_leaf': [1, 2, 4]
}
pipeline_dt = Pipeline([
    ('scaler', scaler),
    ('model', DecisionTreeClassifier(random_state=42))
])
grid_dt = GridSearchCV(pipeline_dt, param_grid_dt, cv=5, scoring='roc_auc')
grid_dt.fit(X_train_smote, y_train_home_smote)

param_grid_gb = {
    'model__n_estimators': [10, 50, 100],
    'model__learning_rate': [0.01, 0.1, 0.5],
    'model__max_depth': [3, 5, 7],
    'model__min_samples_split': [2, 5, 10],
    'model__min_samples_leaf': [1, 2, 4]
}
pipeline_gb = Pipeline([
    ('scaler', scaler),
    ('model', GradientBoostingClassifier(random_state=42))
])
grid_gb = GridSearchCV(pipeline_gb, param_grid_gb, cv=5, scoring='roc_auc')
grid_gb.fit(X_train_smote, y_train_home_smote)

def display_grid_search_results(grid_search, model_name):
    print(f"\n{model_name} - Best Parameters:", grid_search.best_params_)
    print(f"{model_name} - Best ROC AUC Score:", grid_search.best_score_)
    print("\nGrid Scores:\n")
    means = grid_search.cv_results_['mean_test_score']
    stds = grid_search.cv_results_['std_test_score']
    params = grid_search.cv_results_['params']
    for mean, std, param in zip(means, stds, params):
        print(f"{mean:.3f} (+/-{std * 2:.3f}) for {param}")

display_grid_search_results(grid_rf, "Random Forest")
display_grid_search_results(grid_dt, "Decision Tree")
display_grid_search_results(grid_gb, "Gradient Boosting")

best_rf = grid_rf.best_estimator_
best_dt = grid_dt.best_estimator_
best_gb = grid_gb.best_estimator_

for model_name, model in [("Logistic Regression", log_reg), 
                          ("Random Forest", best_rf), 
                          ("Decision Tree", best_dt), 
                          ("Gradient Boosting", best_gb)]:
    model.fit(X_train_smote, y_train_home_smote)
    y_pred_home = model.predict(X_test)
    y_pred_proba_home = model.predict_proba(X_test)[:, 1]
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


everton_id = get_team_id("Everton")
chelsea_id = get_team_id("Chelsea")

everton_last_10_matches = get_last_10_matches(everton_id)
chelsea_last_10_matches = get_last_10_matches(chelsea_id)

everton_form = calculate_form(everton_last_10_matches, everton_id)
chelsea_form = calculate_form(chelsea_last_10_matches, chelsea_id)

everton_vs_chelsea = pd.DataFrame({
    'HomeTeam': ['Everton'],
    'AwayTeam': ['Chelsea'],
    'FTHG': [0],  
    'FTAG': [0],  
    'HS': [0],    
    'AS': [0],    
    'HST': [0],   
    'AST': [0],   
    'HC': [0],    
    'AC': [0],    
    'HF': [0],    
    'AF': [0],    
    'HY': [0],    
    'AY': [0],    
    'HR': [0],    
    'AR': [0],    
    'HomeTeamForm': [everton_form],
    'AwayTeamForm': [chelsea_form]
})

everton_vs_chelsea['GoalDiff'] = everton_vs_chelsea['FTHG'] - everton_vs_chelsea['FTAG']
everton_vs_chelsea['ShotsDiff'] = everton_vs_chelsea['HS'] - everton_vs_chelsea['AS']
everton_vs_chelsea['ShotsOnTargetDiff'] = everton_vs_chelsea['HST'] - everton_vs_chelsea['AST']
everton_vs_chelsea['CornersDiff'] = everton_vs_chelsea['HC'] - everton_vs_chelsea['AC']
everton_vs_chelsea['FoulsDiff'] = everton_vs_chelsea['HF'] - everton_vs_chelsea['AF']
everton_vs_chelsea['YellowsDiff'] = everton_vs_chelsea['HY'] - everton_vs_chelsea['AY']
everton_vs_chelsea['RedsDiff'] = everton_vs_chelsea['HR'] - everton_vs_chelsea['AR']

X_future = everton_vs_chelsea[features]

for model_name, model in [("Logistic Regression", log_reg), 
                          ("Random Forest", best_rf), 
                          ("Decision Tree", best_dt), 
                          ("Gradient Boosting", best_gb)]:
    future_predictions_proba_home = model.predict_proba(X_future)[:, 1]
    future_predictions_proba_draw = model.predict_proba(X_future)[:, 1]
    future_predictions_proba_away = model.predict_proba(X_future)[:, 1]

    print(f"\n{model_name} - Everton vs Chelsea")
    print("Chances of Everton winning:", future_predictions_proba_home.mean())
    print("Chances of draw:", future_predictions_proba_draw.mean())
    print("Chances of Chelsea winning:", future_predictions_proba_away.mean())

    odds_home = 1 / future_predictions_proba_home.mean()
    odds_draw = 1 / future_predictions_proba_draw.mean()
    odds_away = 1 / future_predictions_proba_away.mean()

    print("Betting odds for Everton win:", odds_home)
    print("Betting odds for draw:", odds_draw)
    print("Betting odds for Chelsea win:", odds_away)