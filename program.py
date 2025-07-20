import requests
from bs4 import BeautifulSoup
from exceptions import MenuNotFoundError, MenuBodyNotFoundError

def scrapping():
    meals, main_prices, secondary_prices = [], [], []
    url = "https://eatandmeet.sk/"
    html_response = requests.get(url)
    soup = BeautifulSoup(html_response.text, 'html.parser')

    today_menu_div = soup.select_one("div.tab-pane.fade.active.in")
    if not today_menu_div:
        raise MenuNotFoundError("Dnešné menu sa nenašlo.")
    
    menu_body = today_menu_div.select("div.menu-body.menu-left")
    if not menu_body:
        raise MenuBodyNotFoundError("Nenašli sa položky z menu.")
    
    for body_div in menu_body:
        desc_tag = body_div.find("p", class_="desc")
        desc_text = desc_tag.find(text=True, recursive=False).strip()

        price_tag = body_div.find("span", class_="price")
        main_price = price_tag.find(text=True, recursive=False).strip()
        secondary_price = price_tag.find("span").get_text(strip=True)

        meals.append(desc_text)
        main_prices.append(main_price)
        secondary_prices.append(secondary_price)

    return meals, main_prices, secondary_prices