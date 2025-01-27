import requests
from bs4 import BeautifulSoup


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

                odds = {}
                odds_section = soup.find_all("td", class_="col-odds")
                if len(odds_section) >= 3:
                    odd1 = odds_section[0].find("span", class_="odds-value")
                    if odd1:
                        odds["course1"] = format(
                            float(odd1.text.strip().replace(",", ".")), ".2f"
                        )

                    oddX = odds_section[1].find("span", class_="odds-value")
                    if oddX:
                        odds["courseX"] = format(
                            float(oddX.text.strip().replace(",", ".")), ".2f"
                        )

                    odd2 = odds_section[2].find("span", class_="odds-value")
                    if odd2:
                        odds["course2"] = format(
                            float(odd2.text.strip().replace(",", ".")), ".2f"
                        )

                return {
                    "identifier": f"{team1}:{team2}",
                    "team1": team1,
                    "team2": team2,
                    **odds,
                }

        return None

    event_links = get_match_links(url)
    matches = []

    for event_url in event_links:
        match_data = get_match_teams_and_odds(event_url)
        if match_data:
            matches.append(match_data)

    return matches

if __name__ == "__main__":
    url = "https://www.efortuna.pl/zaklady-bukmacherskie/pilka-nozna/1-anglia"
    all_matches = get_all_matches(url)

    print(all_matches)
