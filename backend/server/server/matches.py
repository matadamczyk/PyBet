import requests
from bs4 import BeautifulSoup
import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from algorithms.optimized_algorithm import predict_match_outcome
from datacollection.bookmakers.normalize import normalize_team_name


def get_all_matches(url):
    print(f"Fetching matches from: {url}")

    def correct_team_name(team_name):
        if team_name.startswith("Man."):
            return "Manchester " + team_name.split(".")[1]
        return team_name

    def get_match_links(url):
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Błąd pobierania strony: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        event_links = []
        for link in soup.find_all("a", class_="event-link js-event-link"):
            href = link.get("href")
            if href:
                event_links.append("https://www.efortuna.pl" + href)

        return event_links

    def get_match_teams_and_odds(event_url):
        response = requests.get(event_url)
        if response.status_code != 200:
            print(f"Błąd pobierania strony wydarzenia: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        market_name = soup.find("span", class_="market-name")
        if market_name:
            match_text = market_name.get_text(strip=True)
            if " - " in match_text:
                team1, team2 = match_text.split(" - ")
                team1 = correct_team_name(team1)
                team2 = correct_team_name(team2)

                norm_team1 = normalize_team_name(team1)
                norm_team2 = normalize_team_name(team2)

                try:
                    _, home_win_prob, draw_prob, away_win_prob = predict_match_outcome(
                        norm_team1, norm_team2
                    )

                    home_odds = round(1 / home_win_prob, 2) if home_win_prob > 0 else 0
                    draw_odds = round(1 / draw_prob, 2) if draw_prob > 0 else 0
                    away_odds = round(1 / away_win_prob, 2) if away_win_prob > 0 else 0

                    return {
                        "identifier": f"{team1}:{team2}",
                        "team1": team1,
                        "team2": team2,
                        "course1": format(home_odds, ".2f"),
                        "courseX": format(draw_odds, ".2f"),
                        "course2": format(away_odds, ".2f"),
                    }
                except Exception as e:
                    print(f"Error predicting odds for {team1} vs {team2}: {str(e)}")
                    return None

        return None

    event_links = get_match_links(url)
    matches = []

    for event_url in event_links:
        match_data = get_match_teams_and_odds(event_url)
        if match_data:
            matches.append(match_data)

    return matches
