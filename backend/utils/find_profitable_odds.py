import csv
import json
from pathlib import Path

def load_odds_from_csv(csv_file):
    odds_data = []
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id = row['identifier']
            t1 = row['team1']
            t2 = row['team2']
            event_data = {
                'id': id,
                't1': t1,
                't2': t2,
                'odds': []
            }

            for bookmaker in ['betclic', 'sts', 'fortuna']:
                bookmaker_data = {
                    '1': float(row[f'{bookmaker}_course1']) if row[f'{bookmaker}_course1'] else None,
                    'X': float(row[f'{bookmaker}_courseX']) if row[f'{bookmaker}_courseX'] else None,
                    '2': float(row[f'{bookmaker}_course2']) if row[f'{bookmaker}_course2'] else None,
                    'BTS': float(row[f'{bookmaker}_courseBTS']) if row[f'{bookmaker}_courseBTS'] else None,
                    'NBTS': float(row[f'{bookmaker}_courseNBTS']) if row[f'{bookmaker}_courseNBTS'] else None,
                }
                event_data['odds'].append({'bookmaker': bookmaker, 'data': bookmaker_data})

            odds_data.append(event_data)
    return odds_data

def find_profitable_events(odds_data, fchances, tax=0.88):
    chances_data = {}
    with open(fchances, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            chances_data[row[0]] = {
                'chance1': float(row[1]),
                'chanceX': float(row[2]),
                'chance2': float(row[3])
            }

    profitable = []

    for row in odds_data:
        id = row['id']
        if id not in chances_data:
            continue

        chances = chances_data[id]
        for bookmaker_data in row['odds']:
            bookmaker = bookmaker_data['bookmaker']
            for outcome, chance_key in zip(['1', 'X', '2'], ['chance1', 'chanceX', 'chance2']):
                odds = bookmaker_data['data'][outcome]
                if odds is None:
                    continue
                chance = chances[chance_key]
                prof = chance * odds
                taxed_prof = prof * tax

                # print({
                #         'id': id,
                #         't1': row['t1'],
                #         't2': row['t2'],
                #         'outcome': outcome,
                #         'chance': chance,
                #         'odds': odds,
                #         'prof': prof,
                #         'taxed_prof': taxed_prof,
                #         'bookmaker': bookmaker
                #     })
                # print()

                # if prof > 1 or taxed_prof > 1:
                if (prof > 1 or taxed_prof > 1) and bookmaker!='sts':
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

    odds_data = load_odds_from_csv(fodds)
    profitable = find_profitable_events(odds_data, fchances)
    save_to_json(profitable, fout)
