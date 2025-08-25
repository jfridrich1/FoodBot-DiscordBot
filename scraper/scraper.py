import requests
from bs4 import BeautifulSoup
from scraper.exceptions import MenuNotFoundError, MenuBodyNotFoundError
from datetime import date
import re

enm_page_url = "https://eatandmeet.sk/"
ff_page_url = "https://www.freefood.sk/menu/#fiit-food"
druzba_page_url = "https://www.druzbacatering.sk/obedove-menu/"
#meal_names, main_prices, secondary_prices, allergens, meal_categories = [], [], [], [], []

def enm_scrap():
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

def druzba_scrap():
    html_response = requests.get(druzba_page_url)
    soup = BeautifulSoup(html_response.text, 'html.parser')

    # Kontrola správnosti dnešného dátumu
    date_today = date.today()
    formatted_date = date_today.strftime("%d.%m.%Y")

    current_date = soup.select_one(".heading-title h2").get_text(strip=True)
    current_date = current_date.split(" ")[1]

    if formatted_date != current_date:
        raise MenuNotFoundError("Dnešné menu sa nenašlo.")

    # Rozparsovanie tabuľky (všetky riadky)
    rows = soup.find_all("tr")

    meal_names, main_prices, secondary_prices, allergens, meal_categories = [], [], [], [], []

    for row in rows[1:]:  # preskočíme header
        cols = row.find_all("td")
        if not cols:
            continue  # prázdny riadok

        # jedlo (ľavý stĺpec)
        meal_text = cols[0].get_text(" ", strip=True)  # spojí texty do jedného stringu
        # cena (pravý stĺpec)
        if len(cols) > 1:
            price_text = cols[1].get_text(" ", strip=True)
        else:
            price_text = ""

        # Parsovanie
        # kategória (Polievka, I., II., III.)
        if meal_text.startswith("Polievka"):
            category = "Polievka"
        elif meal_text.startswith("I."):
            category = "I."
        elif meal_text.startswith("II."):
            category = "II."
        elif meal_text.startswith("III."):
            category = "III."
        else:
            category = ""

        # alergény v zátvorkách
        allergen_match = re.search(r"\(([\d,]+)\)", meal_text)
        if allergen_match:
            allergen_list = f"({allergen_match.group(1)})"
        else:
            allergen_list = ""

        # názov jedla (očistený o kategóriu a alergény)
        meal_clean = re.sub(r"^(Polievka.*?|I\.|II\.|III\.)", "", meal_text).strip()
        meal_clean = re.sub(r"\([\d,]+\)", "", meal_clean).strip()

        # ceny
        price_main, price_secondary = None, None
        prices = re.findall(r"\d+,\d+€", price_text)
        if prices:
            if len(prices) >= 1:
                price_main = prices[0]
            if len(prices) >= 2:
                price_secondary = prices[1]

        # "v cene menu"
        elif price_text:
            price_main = price_text.strip()
            price_secondary = price_text.strip()

        # filter na prazdny element
        if category is not "":
            meal_categories.append(category)
            meal_names.append(meal_clean)
            allergens.append(allergen_list)
            main_prices.append(price_main)
            secondary_prices.append(price_secondary)

    return meal_categories, meal_names, allergens, main_prices, secondary_prices
