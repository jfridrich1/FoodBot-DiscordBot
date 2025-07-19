import requests
import datetime
from bs4 import BeautifulSoup

def scrapping():
    url = "https://eatandmeet.sk/"
    html_response = requests.get(url)
    soup = BeautifulSoup(html_response.text, 'html.parser')

    today_menu_div = soup.find("div", class_="tab-pane fade  active  in")
    menu_description = today_menu_div.find_all("div", class_="menu-description")
    meals = []

    for desc_div in menu_description:
        p_tag = desc_div.find("p", class_="desc")
        if p_tag:
            text = p_tag.find(text=True, recursive=False).strip()
            meals.append(text)


    with open("test_scrap.txt", "w", encoding="utf-8") as f:
        for meal in meals:
            f.write(meal + "\n")

    return meals