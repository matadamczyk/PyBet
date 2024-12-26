import pandas as pd
import numpy as np
import requests
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

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

def get_team_standings(team_id, season="2023"):
    response = requests.get(f"{API_URL}/standings?season={season}&team={team_id}", headers=HEADERS)
    data = response.json()
    if data["response"]:
        standings = data["response"][0]["league"]["standings"][0]
        for team in standings:
            if team["team"]["id"] == team_id:
                return team["rank"], team["points"]
    return None, None

season_stats = pd.read_csv('seasonstats.csv')

season_stats = season_stats[['Season', 'Squad', 'Pts', 'W', 'D', 'L', 'GF', 'GA']]

season_stats['Rank'] = season_stats.groupby('Season')['Pts'].rank(ascending=False)
season_stats['Form'] = season_stats.groupby('Squad')['Pts'].rolling(window=10).mean().reset_index(0, drop=True)

season_stats['Form'].fillna(season_stats['Pts'].mean(), inplace=True)

matches = pd.read_csv('matches.csv')

matches = matches.merge(season_stats, left_on=['Season', 'Home'], right_on=['Season', 'Squad'], suffixes=('', '_Home'))
matches = matches.merge(season_stats, left_on=['Season', 'Away'], right_on=['Season', 'Squad'], suffixes=('_Home', '_Away'))

features = matches[['Rank_Home', 'Pts_Home', 'Form_Home', 'Rank_Away', 'Pts_Away', 'Form_Away']]

matches['Result'] = matches.apply(lambda row: 1 if row['Home Goals'] > row['Away Goals'] else (-1 if row['Home Goals'] < row['Away Goals'] else 0), axis=1)

X_train, X_test, y_train, y_test = train_test_split(features, matches['Result'], test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')

def calculate_odds(probabilities):
    return [1 / prob for prob in probabilities]

tottenham_id = get_team_id("Tottenham")
chelsea_id = get_team_id("Chelsea")

tottenham_last_10_matches = get_last_10_matches(tottenham_id)
chelsea_last_10_matches = get_last_10_matches(chelsea_id)

tottenham_form = calculate_form(tottenham_last_10_matches, tottenham_id)
chelsea_form = calculate_form(chelsea_last_10_matches, chelsea_id)

tottenham_rank, tottenham_points = get_team_standings(tottenham_id)
chelsea_rank, chelsea_points = get_team_standings(chelsea_id)

if None in [tottenham_rank, tottenham_points, tottenham_form, chelsea_rank, chelsea_points, chelsea_form]:
    print("Error: One or more values are missing. Please check the API responses.")
else:
    tottenham_vs_chelsea = pd.DataFrame({
        'Rank_Home': [tottenham_rank], 'Pts_Home': [tottenham_points], 'Form_Home': [tottenham_form],
        'Rank_Away': [chelsea_rank], 'Pts_Away': [chelsea_points], 'Form_Away': [chelsea_form]
    })

    predictions = model.predict_proba(tottenham_vs_chelsea)
    home_win_prob, draw_prob, away_win_prob = predictions[0]
    home_win_odds, draw_odds, away_win_odds = calculate_odds([home_win_prob, draw_prob, away_win_prob])

    print(f'Tottenham vs Chelsea - Home Win Odds: {home_win_odds:.2f}, Draw Odds: {draw_odds:.2f}, Away Win Odds: {away_win_odds:.2f}')