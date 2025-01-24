from datacollection.bookmakers.betclic import fetch_matches_overview
from datacollection.bookmakers.sts import get_data
from datacollection.bookmakers.fortuna import get_all_matches
from utils.find_profitable_odds import load_odds_from_data
from utils.find_profitable_odds import save_to_json
from utils.find_profitable_odds import find_profitable_events
from datacollection.bookmakers.normalize import normalize_team_name, normalize_identifier

from algorithms.optimized_algorithm import predict_match_outcome

def main_func():
    bookmakers = [
        ("betclic", "https://www.betclic.pl/pilka-nozna-sfootball/premier-league-c3", fetch_matches_overview),
        ("sts", "https://www.sts.pl/zaklady-bukmacherskie/pilka-nozna/anglia/premier-league/184/30862/86451", get_data),
        ("fortuna", "https://www.efortuna.pl/zaklady-bukmacherskie/pilka-nozna/1-anglia", get_all_matches),
    ]

    all_data = []
    for site_name, url, func in bookmakers:
        data = func(url, site_name)
        all_data.extend(data)
    odds_data = load_odds_from_data(all_data)
    chances_data = {}
    for match in odds_data:
        t1 = normalize_team_name(match['t1'])
        t2 = normalize_team_name(match['t2'])
        match['id'] = normalize_identifier(match['id'])
        chance_data = predict_match_outcome(t1, t2)
        chances_data[match['id']] = chance_data
    profitable = find_profitable_events(odds_data, chances_data)
    save_to_json(profitable, 'backend/data/profitable/profitable.json')

if __name__ == "__main__":
    main_func()