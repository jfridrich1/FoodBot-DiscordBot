# Mapa kategórií a emoji
CATEGORY_EMOJI_MAP = {
    "POLIEVKA": "🥣",
    "MENU": "🍽",
    "MÚČNE": "🥞",
    "VEGETARIÁNSKE": "🥦",
    "ŠALÁT": "🥗",
    "I.": "🍽",
    "II.": "🍽",
    "III.": "🍽",
    "P.": "🥣",
    "1.": "🍽",
    "2.": "🍽",
    "3.": "🍽"
}

# Funkcia na mapovanie kategórie k príslušnému emoji
def get_emoji_for_title(title: str) -> str:
    for key in CATEGORY_EMOJI_MAP:
        if key in title.upper():
            return CATEGORY_EMOJI_MAP[key]
    return "🍽"