import pandas as pd

df = pd.read_csv("results.csv", encoding='latin1')

def calculate_team_form(team, date, df):
    team_matches = df[((df['HomeTeam'] == team) | (df['AwayTeam'] == team)) & (df['DateTime'] < date)]
    team_matches = team_matches.sort_values(by='DateTime', ascending=False)
    last_10_matches = team_matches.head(10)
    

    form = 0
    for _, match in last_10_matches.iterrows():
        if match['HomeTeam'] == team:
            if match['FTR'] == 'H':
                form += 3
            elif match['FTR'] == 'D':
                form += 1
        else:
            if match['FTR'] == 'A':
                form += 3
            elif match['FTR'] == 'D':
                form += 1
    return form

df['HomeTeamForm'] = df.apply(lambda row: calculate_team_form(row['HomeTeam'], row['DateTime'], df), axis=1)
df['AwayTeamForm'] = df.apply(lambda row: calculate_team_form(row['AwayTeam'], row['DateTime'], df), axis=1)

df.to_csv("results_with_form.csv", index=False, encoding='latin1')

print("Dodano kolumny z formą drużyn i zapisano do pliku results_with_form.csv")