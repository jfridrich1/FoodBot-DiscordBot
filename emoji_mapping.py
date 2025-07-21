# Mapa kategórií a emoji
emoji_map = {
    "POLIEVKA": "🥣",
    "MENU": "🍽",
    "MÚČNE": "🥞",
    "VEGETARIÁNSKE": "🥦",
    "ŠALÁT": "🥗"
}

# Funkcia na mapovanie kategórie k príslušnému emoji
def title_emoji_mapper(title: str) -> str:
    for key in emoji_map:
        if key in title.upper():
            return emoji_map[key]
    return "🍽"