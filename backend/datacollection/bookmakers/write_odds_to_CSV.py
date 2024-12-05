import csv
import os
from betclic import fetch_matches_overview
from pathlib import Path


def save_odds_to_csv(data, site_name, csv_file="backend/data/odds/odds.csv"):
    csv_file = Path(csv_file)
    columns = [
        "identifier",
        "team1",
        "team2",
        f"{site_name}course1",
        f"{site_name}courseX",
        f"{site_name}course2",
        f"{site_name}courseBTS",
        f"{site_name}courseNBTS",
    ]

    file_exists = os.path.isfile(csv_file)

    existing_data = {}
    if file_exists:
        with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_data[row["identifier"]] = row

    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)

        if not file_exists:
            writer.writeheader()

        for entry in data:
            identifier = entry["identifier"]

            if identifier in existing_data:
                existing_row = existing_data[identifier]
                for key in columns:
                    if key in entry:
                        existing_row[key] = entry[key]
                existing_data[identifier] = existing_row
            else:
                new_row = {col: "" for col in columns}
                new_row.update(
                    {
                        "identifier": identifier,
                        "team1": entry["team1"],
                        "team2": entry["team2"],
                        f"{site_name}course1": entry.get("course1", ""),
                        f"{site_name}courseX": entry.get("courseX", ""),
                        f"{site_name}course2": entry.get("course2", ""),
                        f"{site_name}courseBTS": entry.get("courseBTS", ""),
                        f"{site_name}courseNBTS": entry.get("courseNBTS", ""),
                    }
                )
                existing_data[identifier] = new_row

        writer.writerows(existing_data.values())


if __name__ == "__main__":
    save_odds_to_csv(
        fetch_matches_overview(
            "https://www.betclic.pl/pilka-nozna-sfootball/premier-league-c3"
        ),
        "betclic",
    )
