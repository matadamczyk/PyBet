import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import warnings
import os

warnings.filterwarnings("ignore")


def train_and_save_model():
    df_dirty = pd.read_csv("oczyszczonyDataSet.csv")
    df = df_dirty[
        [
            "Date",
            "HomeTeam",
            "AwayTeam",
            "FTHG",
            "FTAG",
            "FTR",
            "HTHG",
            "HTAG",
            "HTR",
            "HS",
            "AS",
            "HST",
            "AST",
            "HF",
            "AF",
            "HC",
            "AC",
            "HY",
            "AY",
            "HR",
            "AR",
        ]
    ]
    avg_home_scored = float(df.FTHG.sum()) / len(df)
    avg_away_scored = df.FTAG.sum() / len(df)
    table = pd.DataFrame(
        columns=("Team", "HGS", "AGS", "HAS", "AAS", "HGC", "AGC", "HDS", "ADS")
    )
    res_home = df.groupby("HomeTeam")
    res_away = df.groupby("AwayTeam")
    table.Team = list(res_home.groups.keys())
    table.HGS = res_home.FTHG.sum().values
    table.HGC = res_home.FTAG.sum().values
    table.AGS = res_away.FTAG.sum().values
    table.AGC = res_away.FTHG.sum().values
    table.HAS = (table.HGS / len(res_home)) / avg_home_scored
    table.AAS = (table.AGS / len(res_away)) / avg_away_scored
    table.HDS = (table.HGC / len(res_home)) / avg_home_scored
    table.ADS = (table.AGC / len(res_away)) / avg_away_scored
    feature_table = df[["HomeTeam", "AwayTeam", "FTR", "HST", "AST", "HC", "AC"]]
    f_HAS, f_HDS, f_AAS, f_ADS = [], [], [], []
    for index, row in feature_table.iterrows():
        f_HAS.append(table[table["Team"] == row["HomeTeam"]]["HAS"].values[0])
        f_HDS.append(table[table["Team"] == row["HomeTeam"]]["HDS"].values[0])
        f_AAS.append(table[table["Team"] == row["AwayTeam"]]["AAS"].values[0])
        f_ADS.append(table[table["Team"] == row["AwayTeam"]]["ADS"].values[0])
    feature_table["HAS"] = f_HAS
    feature_table["HDS"] = f_HDS
    feature_table["AAS"] = f_AAS
    feature_table["ADS"] = f_ADS

    def transformResult(row):
        if row.FTR == "H":
            return 1
        elif row.FTR == "A":
            return -1
        else:
            return 0

    feature_table["Result"] = feature_table.apply(
        lambda row: transformResult(row), axis=1
    )
    X_train_2 = feature_table[["HAS", "HDS", "AAS", "ADS", "HST", "AST", "HC", "AC"]]
    y_train = feature_table["Result"]
    scaler = StandardScaler()
    X_train_2_scaled = scaler.fit_transform(X_train_2)
    best_params = {"hidden_layer_sizes": (16,), "max_iter": 600}
    model = MLPClassifier(random_state=42, **best_params)
    model.fit(X_train_2_scaled, y_train)
    joblib.dump(model, "mlp_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    joblib.dump(table, "team_strengths.pkl")


def predict_match_outcome(home_team, away_team):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    model = joblib.load(os.path.join(current_dir, "mlp_model.pkl"))
    scaler = joblib.load(os.path.join(current_dir, "scaler.pkl"))
    table = joblib.load(os.path.join(current_dir, "team_strengths.pkl"))

    home_HAS = table[table["Team"] == home_team]["HAS"].values[0]
    home_HDS = table[table["Team"] == home_team]["HDS"].values[0]
    away_AAS = table[table["Team"] == away_team]["AAS"].values[0]
    away_ADS = table[table["Team"] == away_team]["ADS"].values[0]

    match_features = [[home_HAS, home_HDS, away_AAS, away_ADS, 0, 0, 0, 0]]
    match_features_scaled = scaler.transform(match_features)
    probabilities = model.predict_proba(match_features_scaled)[0]
    home_win_prob = probabilities[2]
    draw_prob = probabilities[1]
    away_win_prob = probabilities[0]
    match_id = f"{home_team}:{away_team}"

    return [match_id, home_win_prob, draw_prob, away_win_prob]


if __name__ == "__main__":
    train_and_save_model() 
    # predict_match_outcome('Liverpool', 'Fulham')
    # print(predict_match_outcome("Liverpool", "Fulham"))
    # print(predict_match_outcome("Nott'm Forest", "Brighton"))
