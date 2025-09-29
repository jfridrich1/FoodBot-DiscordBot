import re
import requests
from bs4 import BeautifulSoup
from utils.exceptions import WeekendError, MenuNotFoundError, MenuBodyNotFoundError
from datetime import date

druzba_page_url = "https://www.druzbacatering.sk/obedove-menu/"
druzba_page_url2 = "https://www.druzbacatering.sk/jedalny-listok/"

# scrap z dennej ponuky
def druzbaScrapDaily():
    meal_names, main_prices, secondary_prices, allergens, meal_categories = [], [], [], [], []
    html_response = requests.get(druzba_page_url)
    soup = BeautifulSoup(html_response.text, 'html.parser')

    # Kontrola správnosti dnešného dátumu
    date_today = date.today()
    formatted_date = date_today.strftime("%d.%m.%Y")
    weekday_number = date_today.isoweekday()

    current_date = soup.select_one(".heading-title h2").get_text(strip=True)
    current_date = current_date.split(" ")[1]

    if formatted_date != current_date:
        if weekday_number in (6,7):
            raise WeekendError("Víkendové menu sa nenašlo. (D)")
        else:
            raise MenuNotFoundError("Dnešné menu sa nenašlo. (D)")
        
    # Rozparsovanie tabuľky (všetky riadky)
    rows = soup.find_all("tr")

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
        meal_clean = re.sub(r"^(Polievka:.*?|I\.|II\.|III\.)", "", meal_text).strip()
        meal_clean = re.sub(r"\([\d,]+\)", "", meal_clean).strip()

        # ceny
        price_main, price_secondary = None, None
        prices = re.findall(r"\d+,\d+€", price_text)
        if prices:
            if len(prices)>=1:
                price_main=prices[0]
            if len(prices)>=2:
                price_secondary=prices[1]

        # "v cene menu"
        elif price_text:
            price_main = price_text.strip()
            price_secondary = price_text.strip()

        # filter na prazdny element
        if category != "":
            meal_categories.append(category)
            meal_names.append(meal_clean)
            allergens.append(allergen_list)
            main_prices.append(price_main)
            secondary_prices.append(price_secondary)

    return meal_categories, meal_names, allergens, main_prices, secondary_prices

# scrap z týždenného menu
def druzbaScrapWeekly():
    meal_names, main_prices, secondary_prices, allergens, meal_categories = [], [], [], [], []
    html_response = requests.get(druzba_page_url2)
    soup = BeautifulSoup(html_response.text, 'html.parser')

    # dnešný dátum
    date_today = date.today()
    formatted_date = date_today.strftime("%d.%m.%Y")
    weekday_number = date_today.isoweekday()

    current_date = soup.select_one(".heading-title h2").get_text(strip=True)
    current_date = current_date.split(" ")[1]

    if formatted_date != current_date:
        if weekday_number in (6,7):
            raise WeekendError("Víkendové menu sa nenašlo. (D)")
        else:
            raise MenuNotFoundError(formatted_date, current_date)

    for div in soup.select("div.heading-title"):
        h2 = div.find("h2")
        if h2 and formatted_date in h2.get_text(strip=True):
            table = div.find_next_sibling("table")
            if not table:
                raise MenuBodyNotFoundError("Ponuka z dneska sa nepodarila. (D)")

            rows = table.find_all("tr")

            for row in rows[1:]:
                cols = row.find_all("td")
                if not cols:
                    continue

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
                #meal_clean = re.sub(r"^(Polievka: 0,33l: .*?|I\.|II\.|III\.)", "", meal_text).strip()
                meal_clean = re.sub(r"^(Polievka:\s*\d+,\d+l|I\.|II\.|III\.)", "", meal_text).strip()

                meal_clean = re.sub(r"\([\d,]+\)", "", meal_clean).strip()

                # ceny
                price_main, price_secondary = None, None
                prices = re.findall(r"\d+,\d+€", price_text)
                if prices:
                    if len(prices)>=1:
                        price_main=prices[0]
                    if len(prices)>=2:
                        price_secondary=prices[1]

                # "v cene menu"
                elif price_text:
                    price_main = ""
                    price_secondary = ""

                # filter na prazdny element
                if category != "":
                    meal_categories.append(category)
                    meal_names.append(meal_clean)
                    allergens.append(allergen_list)
                    main_prices.append(price_secondary)
                    secondary_prices.append(price_main)

            return meal_categories, meal_names, allergens, main_prices, secondary_prices