import requests
from bs4 import BeautifulSoup
from scraper.exceptions import MenuNotFoundError, MenuBodyNotFoundError
from datetime import date
import re

enm_page_url = "https://eatandmeet.sk/"

def enmScrap():
    # Zoznamy na uloženie získaných dát
    meal_names, main_prices, secondary_prices, allergens, meal_categories = [], [], [], [], []
    html_response = requests.get(enm_page_url)
    soup = BeautifulSoup(html_response.text, 'html.parser')

    # Active menu = dnešné menu
    active_menu_div = soup.select_one("div.tab-pane.fade.active.in")
    if not active_menu_div:
        raise MenuNotFoundError("Dnešné menu sa nenašlo.")
    
    # Vyberanie položiek z dnešného menu
    items_div = active_menu_div.select("div.menu-body.menu-left")
    if not items_div:
        raise MenuBodyNotFoundError("Nenašli sa položky z menu.")
    
    for item in items_div:
        # Získanie názvov jedák z <p>
        desc_tag = item.find("p", class_="desc")
        desc_text = desc_tag.find(text=True, recursive=False).strip()

        # Získanie alergénov zo <span>
        allergen_span = desc_tag.find("span").get_text(strip=True)

        # Získanie kategórií z <h4>
        title_text = item.find("h4").get_text(strip=True)

        # Získanie cien zo <span>
        price_span = item.find("span", class_="price")
        main_price = price_span.find(text=True, recursive=False).strip()
        secondary_price = price_span.find("span").get_text(strip=True)

        meal_names.append(desc_text)
        main_prices.append(main_price)
        secondary_prices.append(secondary_price)
        allergens.append(allergen_span)
        meal_categories.append(title_text.upper())

    return meal_names, main_prices, secondary_prices, allergens, meal_categories