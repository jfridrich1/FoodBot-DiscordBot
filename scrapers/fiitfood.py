import re
import requests
from bs4 import BeautifulSoup
from utils.exceptions import WeekendError, MenuNotFoundError, MenuBodyNotFoundError
from datetime import date

FIITFOOD_PAGE_URL = "http://www.freefood.sk/menu/#fiit-food"

def fetch_fiitfood_page() -> BeautifulSoup:
    response = requests.get(FIITFOOD_PAGE_URL)
    return BeautifulSoup(response.text, "html.parser")

def get_today_offer_block(soup: BeautifulSoup):
    date_today = date.today()
    formatted_date = f"{date_today.day}.{date_today.month}.{date_today.year}"
    weekday_number = date_today.isoweekday()

    fiitfood_block = soup.find("div", id="fiit-food")
    daily_offer = fiitfood_block.find("ul", class_="daily-offer")

    today_block = daily_offer.find(
        "span",
        class_="day-title",
        string=lambda t: t and formatted_date in t,
    )

    if not today_block:
        if weekday_number in (6, 7):
            raise WeekendError("Víkendové menu sa nenašlo. (FF)")
        raise MenuNotFoundError(formatted_date, date_today)

    offer_block = today_block.find_next("ul", class_="day-offer")
    if not offer_block:
        raise MenuBodyNotFoundError("Nenašli sa položky z menu. (FF)")

    return offer_block

def parse_offer_block(offer_block):
    meal_names, main_prices, allergens, meal_categories = [], [], [], []

    for li in offer_block.find_all("li"):
        meal_category = li.find("span", class_="brand").get_text()

        price_tag = li.find("span", class_="brand price")
        main_price = price_tag.get_text(strip=True)

        text_parts = [t for t in li.contents if t.name is None]
        meal_name = " ".join(p.strip() for p in text_parts if p.strip())

        allergen_match = re.search(r"A:([0-9,]+)(?:\s*\(V\))?", meal_name)
        if allergen_match:
            allergens.append(allergen_match.group(1))
            meal_name = meal_name.replace(allergen_match.group(0), "").strip()
            if "(V)" in allergen_match.group(0):
                allergens[-1] += ",V"
        else:
            allergens.append("")

        meal_categories.append(meal_category)
        main_prices.append(main_price)
        meal_names.append(meal_name)

    return meal_categories, meal_names, main_prices, allergens

def get_fiitfood_menu():
    soup = fetch_fiitfood_page()
    offer_block = get_today_offer_block(soup)
    return parse_offer_block(offer_block)