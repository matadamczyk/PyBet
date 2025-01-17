from bs4 import BeautifulSoup
import requests

def get_bts(url):
    return (0, 0)

def get_data(url, site_name="sts"):
    response = requests.get(url)
    content = response.text

    soup = BeautifulSoup(content, "html.parser")

    team_list = soup.find_all(class_="match-tile-event-details-teams__team match-tile-event-details-teams__team--1")

    teams1 = []
    teams2 = []
    courses = []

    for team in team_list:
        text = team.getText()
        teams1.append(text)

    team_list = soup.find_all(class_="match-tile-event-details-teams__team match-tile-event-details-teams__team--2")

    for team in team_list:
        text = team.getText()
        teams2.append(text)

    course_data = soup.find_all(class_="odds-button__odd-value ng-star-inserted")

    flag = True
    i = 0
    for course in course_data:
        if i == 3:
            i = 0
            flag = not flag
        if flag:
            text = course.getText()
            courses.append(text)
        i += 1

    tile_list = soup.find_all("bb-prematch-match-tile", class_="ng-star-inserted")

    links = []
    bts = []

    for tile in tile_list:
        link = tile.find("a")
        if link:
            url = link.get("href")
            links.append(url)

    for link in links:
        bts.append(get_bts(f"https://www.sts.pl{link}"))

    data = []

    for i in range(len(teams1)):
        temp = {
            "identifier": f"{teams1[i]}:{teams2[i]}",
            "team1": teams1[i],
            "team2": teams2[i],
            "course1": courses[i],
            "courseX": courses[i + 1],
            "course2": courses[i + 2],
            "courseBTS": bts[i][0],
            "courseNBTS": bts[i][1],
            "site_name": site_name
        }

        data.append(temp)

    return data

if __name__ == "__main__":
    data = get_data("https://www.sts.pl/zaklady-bukmacherskie/pilka-nozna/anglia/premier-league/184/30862/86451")
    print(data)
    print()
    data = get_data("https://www.sts.pl/zaklady-bukmacherskie/pilka-nozna/anglia/2-liga/184/30862/86456")
    print(data)

