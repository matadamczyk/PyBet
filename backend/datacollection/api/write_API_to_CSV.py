import csv
from collections import defaultdict
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

# API_URL = "https://v3.football.api-sports.io"
# HEADERS = {
#     "x-rapidapi-host": "v3.football.api-sports.io",
#     "x-rapidapi-key": "2b7bfc08bffdd8d9edd0015c7c32f477"  
# }

API_URL = os.getenv("API_URL")
HEADERS = {
    "x-rapidapi-host": API_URL.split("//")[1],
    "x-rapidapi-key": os.getenv("API_KEY")
}

def get_team_id(team_name):
    response = requests.get(f"{API_URL}/teams?search={team_name}", headers=HEADERS)
    data = response.json()
    if data['response']:
        return data['response'][0]['team']['id']
    return None

def get_match_history(team1, team2):
    team1_id = get_team_id(team1)
    team2_id = get_team_id(team2)
    response = requests.get(f"{API_URL}/fixtures/headtohead?h2h={team1_id}-{team2_id}", headers=HEADERS)
    data = response.json()
    match_data = get_last_10_matches(data, team1, team2)
    return match_data

def get_last_10_matches(data, team1, team2):
    match_dict = {'team1_wins': 0, 'draws': 0, 'team2_wins': 0}
    
    matches = sorted(data['response'], key=lambda x: x['fixture']['date'], reverse=True)
    valid_matches = [match for match in matches if match['goals']['home'] is not None and match['goals']['away'] is not None][:10]
    
    for match in valid_matches:
        goals_home = match['goals']['home']
        goals_away = match['goals']['away']
        
        if goals_home > goals_away:
            if match['teams']['home']['name'] == team1:
                match_dict['team1_wins'] += 1
            else:
                match_dict['team2_wins'] += 1
        elif goals_away > goals_home:
            if match['teams']['away']['name'] == team1:
                match_dict['team1_wins'] += 1
            else:
                match_dict['team2_wins'] += 1
        else:
            match_dict['draws'] += 1

    return match_dict

def save_match_history_to_csv(id, team1, team2, data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Team1 Wins', 'Draws', 'Team2 Wins'])
        writer.writerow([id, data['team1_wins'], data['draws'], data['team2_wins']])

def get_api_data(id, team1, team2):
    match_history = get_match_history(team1, team2)
    save_match_history_to_csv(id, team1, team2, match_history, 'match_history.csv')

team1 = "Manchester City"
team2 = "Manchester United"
id = 1  # Example ID
# jeszcze bilans ostatnich 10 meczy i pozycje w tabeli
match_history = get_match_history(team1, team2)
save_match_history_to_csv(id, team1, team2, match_history, 'match_history.csv')