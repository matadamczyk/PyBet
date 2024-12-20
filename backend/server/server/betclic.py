import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def fetch_matches_overview(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    matches = []
    match_elements = soup.find_all("a", class_="cardEvent ng-star-inserted")

    for element in match_elements:
        relative_link = element["href"]
        match_link = urljoin(base_url, relative_link)

        scoreboard = element.find(
            "scoreboards-scoreboard-global", class_="scoreboard_wrapper"
        )
        if scoreboard:
            druzyna1 = scoreboard.find(
                "div", {"data-qa": "contestant-1-label"}
            ).text.strip()
            druzyna2 = scoreboard.find(
                "div", {"data-qa": "contestant-2-label"}
            ).text.strip()
        else:
            continue

        details = fetch_match_details_retry(match_link)
        if details:
            match_data = {
                "identifier": f"{druzyna1}:{druzyna2}",
                "team1": druzyna1,
                "team2": druzyna2,
            }
            match_data.update(details)
            matches.append(match_data)

    return matches

def fetch_match_details_retry(match_url, delay=5):
    # nie zdazylo sie zeby byly potrzebne wiecej niz 2 attempty
    for i in range(5):
        try:
            details = fetch_match_details(match_url)
            if details:
                return details
        except Exception as e:
            print(f"Attempt {i + 1} failed: {e}")
        time.sleep(delay)
    print(f"Failed to fetch details for {match_url} after 5 attempts.")
    return None

def fetch_match_details(match_url):
    response = requests.get(match_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    market_boxes_1x2 = soup.find_all("div", class_="marketBox_lineSelection")
    if len(market_boxes_1x2) < 3:
        raise ValueError("Insufficient 1x2 market data")

    kurs1 = float(
        market_boxes_1x2[0]
        .find("span", class_="btn_label ng-star-inserted")
        .text.replace(",", ".")
    )
    kursX = float(
        market_boxes_1x2[1]
        .find("span", class_="btn_label ng-star-inserted")
        .text.replace(",", ".")
    )
    kurs2 = float(
        market_boxes_1x2[2]
        .find("span", class_="btn_label ng-star-inserted")
        .text.replace(",", ".")
    )

    market_boxes_bts = soup.find_all("div", class_="marketBox")
    bts_section = None
    for box in market_boxes_bts:
        header = box.find("h2", class_="marketBox_headTitle ng-star-inserted")
        if header and header.text.strip() == "Oba zespoły strzelą gola":
            bts_section = box
            break

    if not bts_section:
        raise ValueError("BTS market data not found")

    bts_boxes = bts_section.find_all("span", class_="btn_label ng-star-inserted")
    if len(bts_boxes) != 2:
        raise ValueError("Incomplete BTS market data")

    kursBTS = float(bts_boxes[0].text.replace(",", "."))
    kursNBTS = float(bts_boxes[1].text.replace(",", "."))

    return {
        "course1": kurs1,
        "courseX": kursX,
        "course2": kurs2,
        "courseBTS": kursBTS,
        "courseNBTS": kursNBTS,
    }

def main(url):
    # url = "https://www.betclic.pl/pilka-nozna-sfootball/premier-league-c3"
    matches = fetch_matches_overview(url)
    l = []
    for match in matches:
        l.append(match)
    return l