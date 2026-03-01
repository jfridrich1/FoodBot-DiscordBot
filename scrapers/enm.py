import requests
from bs4 import BeautifulSoup
from utils.exceptions import MenuNotFoundError, MenuBodyNotFoundError

ENM_PAGE_URL = "https://eatandmeet.sk/"

def fetch_enm_page() -> BeautifulSoup:
    response = requests.get(ENM_PAGE_URL)
    return BeautifulSoup(response.text, "html.parser")

def get_active_menu_block(soup: BeautifulSoup):
    active_menu_div = soup.select_one("div.tab-pane.fade.active.in")
    if not active_menu_div:
        raise MenuNotFoundError("", "")

    items_div = active_menu_div.select("div.menu-body.menu-left")
    if not items_div:
        raise MenuBodyNotFoundError("Nenašli sa položky z menu. (EM)")

    return items_div

def parse_menu_items(items_div):
    meal_names, main_prices, secondary_prices, allergens, meal_categories = [], [], [], [], []

    for item in items_div:
        desc_tag = item.find("p", class_="desc")
        meal_name = desc_tag.find(text=True, recursive=False).strip()

        allergen_text = desc_tag.find("span").get_text(strip=True)

        category = item.find("h4").get_text(strip=True)

        price_span = item.find("span", class_="price")
        main_price = price_span.find(text=True, recursive=False).strip()
        secondary_price = price_span.find("span").get_text(strip=True)

        meal_names.append(meal_name)
        main_prices.append(main_price)
        secondary_prices.append(secondary_price)
        allergens.append(allergen_text)
        meal_categories.append(category.upper())

    return meal_names, main_prices, secondary_prices, allergens, meal_categories

def get_enm_menu():
    soup = fetch_enm_page()
    items_div = get_active_menu_block(soup)
    return parse_menu_items(items_div)