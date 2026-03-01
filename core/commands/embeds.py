import discord

from scrapers.enm import get_enm_menu
from scrapers.fiitfood import get_fiitfood_menu
from scrapers.druzba import get_druzba_menu

from utils.emoji_map import get_emoji_for_title
from utils.exceptions import WeekendError, MenuNotFoundError, MenuBodyNotFoundError

async def send_enm_menu_embed(config, channel, guild_id):
    try:
        embed_color = config.get(str(guild_id), {}).get("embed_color", 0xffe28a)

        meal_names, main_prices, secondary_prices, allergens, meal_categories = get_enm_menu()

        enm_embed = discord.Embed(
            title="Eat&Meet",
            description="Pon - Pia: 7:00 - 20:30\nSob - Ned: 9:00 - 19:00",
            color=embed_color,
            url="https://eatandmeet.sk/tyzdenne-menu"
        )

        # Správy o jednotlivých jedlách
        for i in range(len(meal_names)):
            emoji = get_emoji_for_title(meal_categories[i])
            category = f"{meal_categories[i]:<130}"
            name = f"{meal_names[i]}"

            field_text = f"{name}\nCena: *{main_prices[i]}*  **{secondary_prices[i]}**\n"
            if allergens[i] != "":
                field_text += f"{allergens[i]}\n"
            if i != len(meal_names)-1:
                field_text += "\u200B"

            enm_embed.add_field(name=f"{emoji} **{category}**", value=field_text, inline=False)

        # Discord má limit 10 embedov v embede, ak ich je viac, treba poslať po dávkach po 10
        # Poslanie všetkých správ
        await channel.send(embed=enm_embed)
        
    except MenuNotFoundError:
        await channel.send("Nepodarilo sa nájsť dnešné menu.")
    except MenuBodyNotFoundError:
        await channel.send("Našlo sa menu, nepodarilo sa nájst položky z menu.")
    except Exception as e:
        await channel.send(f"Neočakávaná chyba: {type(e).__name__}: {e}")

async def send_druzba_menu_embed(config, channel, guild_id):
    try:
        embed_color = config.get(str(guild_id), {}).get("embed_color", 0xffe28a)

        meal_categories, meal_names, allergens, main_prices, secondary_prices = get_druzba_menu()
            
        druzba_embed = discord.Embed(
            title="Družba",
            description="Pon - Štv: 7:00 - 20:00\nPia: 7:00 - 18:00\nSob - Ned: 8:00 - 18:00",
            color=embed_color,
            url="https://www.druzbacatering.sk/jedalny-listok"
        )

        for i in range(len(meal_names)):
            emoji = get_emoji_for_title(meal_categories[i])
            name = f"{meal_names[i]}"
            secondary_price_text = f"/ *{secondary_prices[i]}*"

            field_text = f"{name}\nCena: "
            if main_prices[i] != "" and secondary_prices != "":
                field_text += f"*{main_prices[i]}* **{secondary_price_text}\n**"
            else:
                field_text += f"**V cene menu\n**"

            if allergens[i] != "":
                field_text += f"{allergens[i]}\n"
            if i != len(meal_names)-1:
                field_text += "\u200B"

            druzba_embed.add_field(name=f"{emoji} **{meal_categories[i]}**", value=field_text, inline=False)

        # Poslanie všetkých správ
        await channel.send(embed=druzba_embed)
        
    except WeekendError as e:
        druzba_error_embed = discord.Embed(
            title="Družba",
            description="Pon - Štv: 7:00 - 20:00\nPia: 7:00 - 18:00\nSob - Ned: 8:00 - 18:00\n**Cez víkend len stále menu.**",
            color=embed_color,
            url="https://www.druzbacatering.sk/nasa-ponuka/vianocne-pecivo/"
        )
        await channel.send(embed=druzba_error_embed)

    except MenuNotFoundError as e:
        #await channel.send("Nepodarilo sa nájsť dnešné menu.")
        await channel.send(f"Nepodarilo sa nájsť dnešné menu. - {e.date_expected} {e.date_found}")
    except MenuBodyNotFoundError:
        await channel.send("Našlo sa menu, nepodarilo sa nájst položky z menu.")
    except Exception as e:
        await channel.send(f"Neočakávaná chyba: {type(e).__name__}: {e}")

async def send_fiitfood_menu_embed(config, channel, guild_id):
    try:
        embed_color = config.get(str(guild_id), {}).get("embed_color", 0xffe28a)

        meal_categories, meal_names, main_prices, allergens = get_fiitfood_menu()

        fiitfood_embed = discord.Embed(
            title="FiitFood",
            description="Pon - Pia: 7:30 - 15:00",
            color=embed_color,
            url="http://www.freefood.sk/menu/#fiit-food"
        )

        for i in range(len(meal_names)):
            emoji = get_emoji_for_title(meal_categories[i])
            name = f"{meal_names[i]}"

            field_text = f"{name}\nCena: **{main_prices[i]}**\n"
            if allergens[i] != "":
                field_text += f"({allergens[i]})\n" 
            if i != len(meal_names)-1:
                field_text += "\u200B"

            fiitfood_embed.add_field(name=f"{emoji} **{meal_categories[i]}**", value=field_text, inline=False)

        # Poslanie všetkých správ
        await channel.send(embed=fiitfood_embed)

    except WeekendError:
        fiitfood_error_embed = discord.Embed(
            title="FiitFood",
            description="FiitFood cez víkend nerobí :(",
            color=embed_color,
            url="http://www.freefood.sk/menu/#fiit-food"
        )
        await channel.send(embed=fiitfood_error_embed)
    except MenuNotFoundError:
        await channel.send("Nepodarilo sa nájsť dnešné menu.")
    except MenuBodyNotFoundError:
        await channel.send("Našlo sa menu, nepodarilo sa nájst položky z menu.")
    except Exception as e:
        await channel.send(f"Neočakávaná chyba: {type(e).__name__}: {e}")