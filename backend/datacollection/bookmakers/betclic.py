import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_matches_overview(base_url):

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    matches = []
    
    match_elements = soup.find_all('a', class_='cardEvent ng-star-inserted')
    
    for element in match_elements:
        relative_link = element['href'] 
        match_link = urljoin(base_url, relative_link)
        
        scoreboard = element.find('scoreboards-scoreboard-global', class_='scoreboard_wrapper')
        if scoreboard:
            druzyna1 = scoreboard.find('div', {'data-qa': 'contestant-1-label'}).text.strip()
            druzyna2 = scoreboard.find('div', {'data-qa': 'contestant-2-label'}).text.strip()
        else:
            continue 
        
        match_data = {
            "identifier": f"{druzyna1}:{druzyna2}",
            "team1": druzyna1,
            "team2": druzyna2,
            "link": match_link
        }
        matches.append(match_data)
    
    data=[]

    for match in matches:
        details = fetch_match_details(match["link"])
        del match["link"]
        if details is not None:
            match.update(details)
            data.append(match)
        print(match)

    return data


def fetch_match_details(match_url):

    response = requests.get(match_url)
    if response.status_code != 200:
        print("Nie udalo sie pobrac strony")
        raise Exception(f"Blad przy pobieraniu")
    
    soup = BeautifulSoup(response.text, 'html.parser')

    market_boxes_1x2 = soup.find_all('div', class_='marketBox_lineSelection')

    if len(market_boxes_1x2) == 0:
        return

    kurs1 = float(market_boxes_1x2[0].find('span', class_='btn_label ng-star-inserted').text.replace(',', '.'))
    kursX = float(market_boxes_1x2[1].find('span', class_='btn_label ng-star-inserted').text.replace(',', '.'))
    kurs2 = float(market_boxes_1x2[2].find('span', class_='btn_label ng-star-inserted').text.replace(',', '.'))

    market_boxes_bts = soup.find_all('div', class_='marketBox')
    bts_section = None
    for box in market_boxes_bts:
        header = box.find('h2', class_='marketBox_headTitle ng-star-inserted')
        if header.text.strip() == "Oba zespoły strzelą gola":
            bts_section = box
            break

    if not bts_section:
        raise ValueError("Nie 1")

    bts_boxes = bts_section.find_all('span', class_='btn_label ng-star-inserted')
    if len(bts_boxes) != 2:
        raise ValueError("Nie 2")

    kursBTS = float(bts_boxes[0].text.replace(',', '.'))
    kursNBTS = float(bts_boxes[1].text.replace(',', '.'))

    return {
        "course1": kurs1,
        "courseX": kursX,
        "course2": kurs2,
        "courseBTS": kursBTS,
        "courseNBTS": kursNBTS
    }

if __name__ == "__main__":
    url = "https://www.betclic.pl/pilka-nozna-sfootball/premier-league-c3"
    fetch_matches_overview(url)
    
