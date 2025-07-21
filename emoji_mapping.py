emoji_table = {
    "polievka": "🥣",
    "menu": "🍽",
    "múčne": "🍞",
    "vegetariánske": "🥦",
    "šalát": "🥗"
}

def get_emoji_for_title(title: str) -> str:
    for key in emoji_table:
        if key.lower() in title.lower():
            return emoji_table[key]
    return "🍽"