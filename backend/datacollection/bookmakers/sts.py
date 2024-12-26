from bs4 import BeautifulSoup
import requests



def get_bts(url):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Optional: for compatibility with some environments
    chrome_options.add_argument("--no-sandbox")  # Optional: for environments like Linux servers

    # Set up Selenium WebDriver
    driver = webdriver.Chrome(options=chrome_options)  # Ensure the WebDriver path is correct
    driver.get(url)

    try:
        # Wait for the parent element to be visible
        wait = WebDriverWait(driver, 30)
        parent_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/app-mweb/div/div/div/div[1]/div/div[2]/app-match-detail-prematch/app-match-detail/div/div[4]/app-prematch-odds/div/app-odds-page/app-match-details-group[2]"))
        )
        
        # Retrieve all text within the parent element
        text_content = parent_element.text.split("\n")

        # Print the extracted text
        # print("Extracted Text:")
        # print(text_content)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()

    return (text_content[2],text_content[4])


def get_data(url):
    response = requests.get(url)
    content = response.text

    soup = BeautifulSoup(content, "html.parser")

    team_list = soup.find_all(class_="match-tile-event-details-teams__team match-tile-event-details-teams__team--1")

    # "match-tile-event-details-teams__team match-tile-event-details-teams__team--1"

    # "match-opportunity-wrapper__grid match-opportunity-wrapper__grid--three-columns"

    # "odds-value"

    # "odds-button__odd-value ng-star-inserted"

    # "odds-button__odd-value ng-star-inserted"

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
    i=0
    for course in course_data:
        if i==3:
            i=0
            flag = not flag
        if(flag):
            text = course.getText()
            courses.append(text)
        i+=1

    tile_list = soup.find_all("bb-prematch-match-tile", class_="ng-star-inserted")

    links = []
    bts = []

    for tile in tile_list:
        link = tile.find("a")  
        if link:  
            url = link.get("href")
            links.append(url)
        
    for link in links:
        # print(f"https://www.sts.pl{link}")
        bts.append(get_bts(f"https://www.sts.pl{link}"))
        # content = response.text

        # soup = BeautifulSoup(content, "html.parser")
        # print(response)
        # goal = soup.find_all(name="span", class_="odds-button__odd-value ng-star-inserted")
        # print(goal)
        # for i in goal:
        #     print(i)
        #     print(i.getText())
        

    data = []

    for i in range(len(teams1)):
        temp = {
            "identifier": f"{teams1[i]}:{teams2[i]}",
            "team1": teams1[i],
            "team2": teams2[i],
            "course1": courses[i],
            "courseX": courses[i+1],
            "course2": courses[i+2],
            "bts": bts[i][0],
            "nbts": bts[i][1]
        }

        data.append(temp)

    return data

if __name__ == "__main__":
    data = get_data("https://www.sts.pl/zaklady-bukmacherskie/pilka-nozna/anglia/premier-league/184/30862/86451")

    print(data)

    print()

    data = get_data("https://www.sts.pl/zaklady-bukmacherskie/pilka-nozna/anglia/2-liga/184/30862/86456")

    print(data)




# response = requests.get("https://www.sts.pl/zaklady-bukmacherskie/pilka-nozna/anglia/2-liga/184/30862/86456")
# content = response.text

# soup = BeautifulSoup(content, "html.parser")

# tile_list = soup.find_all("bb-prematch-match-tile", class_="ng-star-inserted")

# links = []

# for tile in tile_list:
#     link = tile.find("a")  
#     if link:  
#         url = link.get("href")
#         links.append(url)
    
# for link in links:
#     print(f"https://www.sts.pl{link}")
#     response = get_bts(f"https://www.sts.pl{link}")
#     # content = response.text

#     # soup = BeautifulSoup(content, "html.parser")
#     print(response)
#     # goal = soup.find_all(name="span", class_="odds-button__odd-value ng-star-inserted")
#     # print(goal)
#     # for i in goal:
#     #     print(i)
#     #     print(i.getText())
    
