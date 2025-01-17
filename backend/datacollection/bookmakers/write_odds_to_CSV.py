import csv
import os
# from betclic import fetch_matches_overview
# from sts import get_data
# from fortuna import get_all_matches
from pathlib import Path

def normalize_team_name(team_name):
    if "nottingham" in team_name.lower():
        return "Nott'm Forest"
    if "utd" in team_name.lower():
        return "Man United"
    if "manchester" in team_name.lower():
        return team_name.replace("Manchester","Man")
    if "wolverhampton" in team_name.lower():
        return "Wolves"
    return team_name

def normalize_identifier(identifier):

    if "nottingham" in identifier.lower():
        if "forest" in identifier.lower():
            identifier=identifier.replace(" Forest", "")
        return identifier.replace("Nottingham","Nott'm Forest")
    if "utd" in identifier.lower():
        return identifier.replace("Manchester Utd","Man United")
    if "manchester" in identifier.lower():
        return identifier.replace("Manchester","Man")
    if "wolverhampton" in identifier.lower():
        return identifier.replace("Wolverhampton","Wolves")
    return identifier

def save_odds_to_csv(data, site_name, csv_file="backend/data/odds/odds.csv"):
    csv_file = Path(csv_file)
    temp = ["betclic", "sts", "fortuna"]
    all_sites_columns = [
        "identifier",
        "team1",
        "team2",
    ] + [
        f"{site}_course1" for site in temp
    ] + [
        f"{site}_courseX" for site in temp
    ] + [
        f"{site}_course2" for site in temp
    ] + [
        f"{site}_courseBTS" for site in temp
    ] + [
        f"{site}_courseNBTS" for site in temp
    ]

    file_exists = os.path.isfile(csv_file)

    existing_data = {}
    if file_exists:
        with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_data[row["identifier"]] = row

    for entry in data:
        team1_normalized = normalize_team_name(entry["team1"])
        team2_normalized = normalize_team_name(entry["team2"])
        identifier_normalized = normalize_identifier(entry["identifier"])

        if identifier_normalized in existing_data:
            row = existing_data[identifier_normalized]
        else:
            row = {col: "" for col in all_sites_columns}
            row["identifier"] = identifier_normalized
            row["team1"] = team1_normalized
            row["team2"] = team2_normalized

        row[f"{site_name}_course1"] = entry.get("course1", "")
        row[f"{site_name}_courseX"] = entry.get("courseX", "")
        row[f"{site_name}_course2"] = entry.get("course2", "")
        row[f"{site_name}_courseBTS"] = entry.get("courseBTS", "")
        row[f"{site_name}_courseNBTS"] = entry.get("courseNBTS", "")

        existing_data[identifier_normalized] = row

    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=all_sites_columns)
        writer.writeheader()
        writer.writerows(existing_data.values())



if __name__ == "__main__":
    bookmakers = [
        ("betclic", "https://www.betclic.pl/pilka-nozna-sfootball/premier-league-c3", fetch_matches_overview),
        ("sts", "https://www.sts.pl/zaklady-bukmacherskie/pilka-nozna/anglia/premier-league/184/30862/86451", get_data),
        ("fortuna", "https://www.efortuna.pl/zaklady-bukmacherskie/pilka-nozna/1-anglia", get_all_matches),
    ]

    for site_name, url, func in bookmakers:
        data = func(url)
        save_odds_to_csv(data, site_name)
