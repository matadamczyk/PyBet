import csv
from pathlib import Path

def load_odds_from_csv(csv_file):
    odds_data = []
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            id = row[0]
            t1 = row[1]
            t2 = row[2]
            event_data = {
                'id': id,
                't1': t1,
                't2': t2,
                'odds': []
            }
            t = (len(row) - 3) // 5
            
            for i in range(t):
                j = 3 + i * 5
                bookmaker_data = {
                    '1': float(row[j]),
                    'X': float(row[j + 1]),
                    '2': float(row[j + 2])
                }
                event_data['odds'].append(bookmaker_data)
        
            odds_data.append(event_data)
        #print(odds_data)
    return odds_data

def find_profitable_events(odds_data, fchances, tax=0.88):
    chances_data = {}
    with open(fchances, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            chances_data[row[0]] = {
                'chance1': float(row[1]) / 100,
                'chanceX': float(row[2]) / 100,
                'chance2': float(row[3]) / 100
            }

    profitable = []

    for row in odds_data:
        id = row['id']
        if id not in chances_data:
            continue

        chances = chances_data[id]
        for bookmaker_data in row['odds']:
            for outcome, chance_key in zip(['1', 'X', '2'], ['chance1', 'chanceX', 'chance2']):
                odds = bookmaker_data[outcome]
                chance = chances[chance_key]
                prof = chance * odds
                taxed_prof = prof * tax

                if prof > 1 or taxed_prof > 1:
                    profitable.append({
                        'id': id,
                        't1': row['t1'],
                        't2': row['t2'],
                        'outcome': outcome,
                        'chance': chance,
                        'odds': odds,
                        'prof': prof,
                        'taxed_prof': taxed_prof
                    })

    return profitable

def save_to_csv(profitable, fout):
    columns = ['id', 't1', 't2', 'outcome', 'chance', 'odds', 'prof', 'taxed_prof']
    with open(fout, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(profitable)

if __name__ == "__main__":
    fodds = 'backend/data/odds/odds.csv'
    fchances = 'backend/data/API/chances.csv'
    fout = 'backend/data/profitable/profitable.csv'
    save_to_csv(find_profitable_events(load_odds_from_csv(fodds), fchances), fout)