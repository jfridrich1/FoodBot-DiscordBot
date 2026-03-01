import re
import requests
from bs4 import BeautifulSoup
from utils.exceptions import WeekendError, MenuNotFoundError, MenuBodyNotFoundError
from datetime import date

DRUZBA_PAGE_URL = "https://www.druzbacatering.sk/jedalny-listok/"

def fetch_druzba_page() -> BeautifulSoup:
    response = requests.get(DRUZBA_PAGE_URL)
    return BeautifulSoup(response.text, "html.parser")

def get_today_table(soup: BeautifulSoup):
    date_today = date.today()
    formatted_date = date_today.strftime("%d.%m.%Y")
    weekday_number = date_today.isoweekday()

    all_week = soup.select(".heading-title h2")
    current_h2 = None
    current_table = None

    for h2 in all_week:
        if formatted_date in h2.get_text(strip=True):
            current_h2 = h2.get_text(strip=True).split(" ")[1]
            current_div = h2.find_parent("div", class_="heading-title text-center")
            current_table = current_div.find_next_sibling("table")
            if not current_table:
                raise MenuBodyNotFoundError("Ponuka z dneska sa nepodarila. (D)")
            break

    if formatted_date != current_h2:
        if weekday_number in (6, 7):
            raise WeekendError("Víkendové menu sa nenašlo. (D)")
        raise MenuNotFoundError(formatted_date, current_h2)

    return current_table

def parse_menu_table(table):
    meal_names, main_prices, secondary_prices, allergens, meal_categories = [], [], [], [], []

    rows = table.find_all("tr")

    for row in rows[1:]:
        cols = row.find_all("td")
        if not cols:
            continue

        meal_text = cols[0].get_text(" ", strip=True)

        if len(cols) > 1:
            price_text = cols[1].get_text(" ", strip=True)
        else:
            price_text = ""

        # kategória
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

        allergen_match = re.search(r"\(([\d,]+)\)", meal_text)
        allergen_list = f"({allergen_match.group(1)})" if allergen_match else ""

        meal_clean = re.sub(
            r"^(Polievka:?\s*\d+,\d+l:?|I\.|II\.|III\.)",
            "",
            meal_text,
        ).strip()
        meal_clean = re.sub(r"\([\d,]+\)", "", meal_clean).strip()

        price_main, price_secondary = None, None
        prices = re.findall(r"\d+,\d+€", price_text)
        if prices:
            if len(prices) >= 1:
                price_main = prices[0]
            if len(prices) >= 2:
                price_secondary = prices[1]
        elif price_text:
            price_main = ""
            price_secondary = ""

        if category:
            meal_categories.append(category)
            meal_names.append(meal_clean)
            allergens.append(allergen_list)
            main_prices.append(price_secondary)
            secondary_prices.append(price_main)

    return meal_categories, meal_names, allergens, main_prices, secondary_prices

def get_druzba_menu():
    soup = fetch_druzba_page()
    table = get_today_table(soup)
    return parse_menu_table(table)
