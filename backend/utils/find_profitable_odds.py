import json

def load_odds_from_data(data):
    odds_data = []
    for row in data:
        id = row['identifier']
        t1 = row['team1']
        t2 = row['team2']
        site_name = row['site_name']
        event_data = {
            'id': id,
            't1': t1,
            't2': t2,
            'odds': []
        }

        bookmaker_data = {
            '1': float(row.get('course1', 0)) if row.get('course1') else None,
            'X': float(row.get('courseX', 0)) if row.get('courseX') else None,
            '2': float(row.get('course2', 0)) if row.get('course2') else None,
            'BTS': float(row.get('courseBTS', 0)) if row.get('courseBTS') else None,
            'NBTS': float(row.get('courseNBTS', 0)) if row.get('courseNBTS') else None,
        }


        event_data['odds'].append({'bookmaker': site_name, 'data': bookmaker_data})

        odds_data.append(event_data)
    return odds_data

def find_profitable_events(odds_data, chances_data, tax=0.88):
    profitable = []

    for row in odds_data:
        id = row['id']
        if id not in chances_data:
            continue

        chances = chances_data[id]
        for bookmaker_data in row['odds']:
            bookmaker = bookmaker_data['bookmaker']
            for outcome, chance_index in zip(['1', 'X', '2'], [1, 2, 3]):
                odds = bookmaker_data['data'][outcome]
                if odds is None:
                    continue
                chance = chances[chance_index]
                prof = chance * odds
                taxed_prof = prof * tax

                if (prof > 1 or taxed_prof > 1) and bookmaker != 'sts':
                    profitable.append({
                        'id': id,
                        't1': row['t1'],
                        't2': row['t2'],
                        'outcome': outcome,
                        'chance': chance,
                        'odds': odds,
                        'prof': prof,
                        'taxed_prof': taxed_prof,
                        'bookmaker': bookmaker
                    })

    return profitable

def save_to_json(profitable, fout):
    with open(fout, mode='w', encoding='utf-8') as file:
        json.dump(profitable, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    fodds = 'backend/data/odds/odds.csv'
    fchances = 'backend/data/API/chances.csv'
    fout = 'backend/data/profitable/profitable.json'

    odds_data = load_odds_from_data(fodds)
    profitable = find_profitable_events(odds_data, fchances)
    save_to_json(profitable, fout)
