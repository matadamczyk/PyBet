from datacollection.bookmakers.betclic import fetch_matches_overview
from datacollection.bookmakers.sts import get_data
from datacollection.bookmakers.fortuna import get_all_matches
from datacollection.bookmakers.write_odds_to_CSV import save_odds_to_csv
from utils.find_profitable_odds import load_odds_from_csv
from utils.find_profitable_odds import save_to_json
from utils.find_profitable_odds import find_profitable_events


from algorithms.optimized_algorithm import predict_match_outcome

def save_chances_to_csv(data, filename):
    import csv
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for match in data:
            writer.writerow(match)

if __name__ == "__main__":
    bookmakers = [
        ("betclic", "https://www.betclic.pl/pilka-nozna-sfootball/premier-league-c3", fetch_matches_overview),
        ("sts", "https://www.sts.pl/zaklady-bukmacherskie/pilka-nozna/anglia/premier-league/184/30862/86451", get_data),
        ("fortuna", "https://www.efortuna.pl/zaklady-bukmacherskie/pilka-nozna/1-anglia", get_all_matches),
    ]

    for site_name, url, func in bookmakers:
        data = func(url)
        save_odds_to_csv(data, site_name)

    chances_data = []
    odds_data = load_odds_from_csv("backend/data/odds/odds.csv")
    for match in odds_data:
        t1=match['t1']
        t2=match['t2']
        chance_data = predict_match_outcome(t1,t2)
        chances_data.append(chance_data)
    save_chances_to_csv(chances_data, 'backend/data/API/chances.csv')
    profitable = find_profitable_events(odds_data, 'backend/data/API/chances.csv')
    save_to_json(profitable, 'backend/data/profitable/profitable.json')