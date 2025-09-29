import re
import requests
from bs4 import BeautifulSoup
from utils.exceptions import WeekendError, MenuNotFoundError, MenuBodyNotFoundError
from datetime import date

fiitfood_page_url = "http://www.freefood.sk/menu/#fiit-food"

def fiitfoodScrap():
    meal_names, main_prices, allergens, meal_categories = [], [], [], []
    html_response = requests.get(fiitfood_page_url)
    soup = BeautifulSoup(html_response.text, 'html.parser')

    # Kontrola správnosti dnešného dátumu
    date_today = date.today()
    formatted_date = f"{date_today.day}.{date_today.month}.{date_today.year}"
    weekday_number = date_today.isoweekday()

    ff_block = soup.find("div", id="fiit-food")

    daily_offer = ff_block.find("ul", class_="daily-offer")

    # nájdi dnešný deň podľa span.day-title
    today_block = daily_offer.find("span", class_="day-title", string=lambda t: t and formatted_date in t)
    if not today_block:
        if weekday_number in (6,7):
            raise WeekendError("Víkendové menu sa nenašlo. (FF)")
        else:
            raise MenuNotFoundError(formatted_date, date_today)

    # nájdi ul.day-offer patriaci k tomuto dňu
    offer_block = today_block.find_next("ul", class_="day-offer")
    if not offer_block:
        raise MenuBodyNotFoundError("Nenašli sa položky z menu. (FF)")
    
    for li in offer_block.find_all("li"):
        meal_category = li.find("span", class_="brand").get_text()

        price_tag = li.find("span", class_="brand price")
        main_price = price_tag.get_text(strip=True)

        parts = [t for t in li.contents if t.name is None]
        meal_name = " ".join(p.strip() for p in parts if p.strip())

        match = re.search(r"A:([0-9,]+)(?:\s*\(V\))?", meal_name)
        if match:
            allergens.append(match.group(1))
            meal_name = meal_name.replace(match.group(0), "").strip()
            if "(V)" in match.group(0):
                allergens[-1] += ",V"
        else:
            allergens.append("")

        meal_categories.append(meal_category)
        main_prices.append(main_price)
        meal_names.append(meal_name)

    return meal_categories, meal_names, main_prices, allergens