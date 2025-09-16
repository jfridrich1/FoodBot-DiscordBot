# Mapa kategórií a emoji
emoji_map = {
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
def title_emoji_mapper(title: str) -> str:
    for key in emoji_map:
        if key in title.upper():
            return emoji_map[key]
    return "🍽"