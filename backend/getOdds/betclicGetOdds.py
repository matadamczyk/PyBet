# ZROBIC TO BEATIFULSUOP NIE TAK POZDRO
import urllib.request
import re
import match

betclic_url = "https://www.betclic.pl/pilka-nozna-s1/premier-league-c3"
betclic_pattern = r"<sports-events-event[^>]*>(.*?)</sports-events-event>"
betclic_html = urllib.request.urlopen(betclic_url).read()
with open('betclic.html','wb') as file:
    file.write(betclic_html)
html_content = betclic_html.decode('utf-8')
premier_test_list=[]

for i in re.findall(betclic_pattern,html_content):
    team1_match = re.search(r'data-qa="contestant-1-label".*?class="scoreboard_contestantLabel.*?">(.*?)</div>', i)
    team2_match = re.search(r'data-qa="contestant-2-label".*?class="scoreboard_contestantLabel.*?">(.*?)</div>', i)
    time_match = re.search(r'class="event_infoTime.*?">(.*?)</div>', i)
    odd1_match = re.search(r'btn is-odd is-large has-trends ng-star-inserted".*?btn_label is-top ng-star-inserted.*?<span class="ng-star-inserted">.*?</span>.*?btn_label ng-star-inserted">(.*?)</span>', i)
    oddX_match = re.search(r'btn is-odd is-large has-trends ng-star-inserted".*?btn_label is-top ng-star-inserted.*?<span class="ng-star-inserted">Remis</span>.*?btn_label ng-star-inserted">(.*?)</span>', i)
    odd2_match = re.search(r'btn is-odd is-large has-trends ng-star-inserted".*?btn_label is-top ng-star-inserted.*?<span class="ng-star-inserted">.*?</span>.*?btn_label ng-star-inserted">(.*?)</span>', i)
    team1 = team1_match.group(1) if team1_match else None
    team2 = team2_match.group(1) if team2_match else None
    time = time_match.group(1) if time_match else None
    odd1 = odd1_match.group(1) if odd1_match else None
    oddX = oddX_match.group(1) if oddX_match else None
    odd2 = odd2_match.group(1) if odd2_match else None
    premier_test_list.append(match.Match(team1,team2,time,odd1,odd2,oddX))

print(len(premier_test_list))
for i in premier_test_list:
    print(i)