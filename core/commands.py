import discord
from discord.ext import commands
from discord.ext.commands import Bot

from scraper.ENMscraper import enmScrap
from scraper.DRUZBAscraper import druzbaScrapDaily
from scraper.DRUZBAscraper import druzbaScrapWeekly

from scraper.FIITFOODscraper import fiitfoodScrap

from utils.config import load_config
from utils.emojiMap import title_emoji_mapper
from utils.accessControl import accessCheck
from utils.exceptions import WeekendError, MenuNotFoundError, MenuBodyNotFoundError, InvalidGuildError, InvalidChannelError

async def daily_update(bot: Bot):
    config = load_config()
    for guild in bot.guilds:
        guild_id = str(guild.id)
        guild_config = config.get(guild_id)
        if not guild_config:
            continue

        channel_id = guild_config.get("channel_id")
        if not channel_id:
            continue

        channel = bot.get_channel(channel_id)
        await channel.purge(limit=4)
        if channel:
            await send_enm_menu(config, channel, guild.id)
            await send_druzba_menu(config, channel, guild.id)
            await send_fiitfood_menu(config, channel, guild.id)

async def send_enm_menu(config, channel, guild_id):
    try:
        # Premazanie správ pred poslaním novej spŕavy
        #await channel.purge(limit=10)
        embed_color = config.get(str(guild_id), {}).get("embed_color", 0xffe28a)

        meal_names, main_prices, secondary_prices, allergens, meal_categories = enmScrap()

        string_embed = ""

        # Správy o jednotlivých jedlách
        for i in range(len(meal_names)):
            emoji = title_emoji_mapper(meal_categories[i])
            category = f"{meal_categories[i]:<130}"
            name = f"{meal_names[i]}"

            string_embed += f"{emoji} **{category}**\n{name}\nCena: *{main_prices[i]}*  **{secondary_prices[i]}**\n"
            if allergens[i] != "":
                string_embed += f"{allergens[i]}\n\n"
            else:
                string_embed += "\n"

        enm_embed = discord.Embed(
            title="Eat&Meet",
            description=string_embed,
            color=embed_color,
            url="https://eatandmeet.sk/tyzdenne-menu"
        )

        # Ping JSON role predtým ako sa pošle menu
        role_id = config[str(guild_id)].get("role_id")
        if role_id:
            role = channel.guild.get_role(int(role_id))
            if role:
                await channel.send(f"{role.mention}")
            #else:
                #await channel.send("Rola neexistuje na serveri.")
        else:
            await channel.send("Role ID nie je nastavené.")

        # Discord má limit 10 embedov v embede, ak ich je viac, treba poslať po dávkach po 10
        # Poslanie všetkých správ
        await channel.send(embed=enm_embed)
        
    except MenuNotFoundError as e:
        await channel.send("Nepodarilo sa nájsť dnešné menu.")
    except MenuBodyNotFoundError as e:
        await channel.send("Našlo sa menu, nepodarilo sa nájst položky z menu.")
    except Exception as e:
        await channel.send(f"Neočakávaná chyba: {type(e).__name__}: {e}")

async def send_druzba_menu(config, channel, guild_id):
    try:
        #await channel.purge(limit=6)
        embed_color = config.get(str(guild_id), {}).get("embed_color", 0xffe28a)

        meal_categories, meal_names, allergens, main_prices, secondary_prices = druzbaScrapWeekly()

        string_embed = ""

        # Správy o jednotlivých jedlách
        for i in range(len(meal_names)):
            emoji = title_emoji_mapper(meal_categories[i])
            name = f"{meal_names[i]}"
            f_secondary_price = f"/ *{secondary_prices[i]}*"

            string_embed += f"{emoji} **{meal_categories[i]}**\n{name}\nCena: "
            if main_prices[i] != "" and secondary_prices != "":
                string_embed += f"*{main_prices[i]}* **{f_secondary_price}\n**"
            else:
                string_embed += f"**V cene menu\n**"

            if allergens[i] != "":
                string_embed += f"{allergens[i]}\n\n"
            else:
                string_embed += "\n"
            
        druzba_embed = discord.Embed(
            title="Družba",
            description=string_embed,
            color=embed_color,
            url="https://www.druzbacatering.sk/jedalny-listok"
        )

        # Ping JSON role predtým ako sa pošle menu
        role_id = config[str(guild_id)].get("role_id")
        if role_id:
            role = channel.guild.get_role(int(role_id))
            #if role:
                #await channel.send(f"{role.mention}")
            #else:
                #await channel.send("Rola neexistuje na serveri.")
        else:
            await channel.send("Role ID nie je nastavené.")

        # # Discord má limit 10 embedov v embede, ak ich je viac, treba poslať po dávkach po 10
        # Poslanie všetkých správ
        await channel.send(embed=druzba_embed)
        
    except WeekendError as e:
        druzba_error_embed = discord.Embed(
            title="Družba",
            description="Cez víkend len stále menu.",
            color=embed_color,
            url="https://www.druzbacatering.sk/nasa-ponuka/vianocne-pecivo/"
        )
        await channel.send(embed=druzba_error_embed)
    except MenuNotFoundError as e:
        #await channel.send("Nepodarilo sa nájsť dnešné menu.")
        await channel.send(f"Nepodarilo sa nájsť dnešné menu. - {e.date_expected} {e.date_found}")
    except MenuBodyNotFoundError as e:
        await channel.send("Našlo sa menu, nepodarilo sa nájst položky z menu.")
    except Exception as e:
        await channel.send(f"Neočakávaná chyba: {type(e).__name__}: {e}")

async def send_fiitfood_menu(config, channel, guild_id):
    try:
        embed_color = config.get(str(guild_id), {}).get("embed_color", 0xffe28a)

        meal_categories, meal_names, main_prices, allergens = fiitfoodScrap()

        string_embed = ""

        # Správy o jednotlivých jedlách
        for i in range(len(meal_names)):
            emoji = title_emoji_mapper(meal_categories[i])
            name = f"{meal_names[i]}"

            string_embed += f"{emoji} **{meal_categories[i]}**\n{name}\nCena: **{main_prices[i]}**\n"
            if allergens[i] != "":
                string_embed += f"({allergens[i]})\n\n" 
            else:
                string_embed += "\n"

        fiitfood_embed = discord.Embed(
            title="FiitFood",
            description=string_embed,
            color=embed_color,
            url="http://www.freefood.sk/menu/#fiit-food"
        )

        # Ping JSON role predtým ako sa pošle menu
        role_id = config[str(guild_id)].get("role_id")
        if role_id:
            role = channel.guild.get_role(int(role_id))
            #if role:
                #await channel.send(f"{role.mention}")
            #else:
                #await channel.send("Rola neexistuje na serveri.")
        else:
            await channel.send("Role ID nie je nastavené.")

        # # Discord má limit 10 embedov v embede, ak ich je viac, treba poslať po dávkach po 10
        # Poslanie všetkých správ
        await channel.send(embed=fiitfood_embed)

    except WeekendError as e:
        fiitfood_error_embed = discord.Embed(
            title="FiitFood",
            description="FiitFood cez víkend nerobí :(",
            color=embed_color,
            url="http://www.freefood.sk/menu/#fiit-food"
        )
        await channel.send(embed=fiitfood_error_embed)
    except MenuNotFoundError as e:
        await channel.send("Nepodarilo sa nájsť dnešné menu.")
    except MenuBodyNotFoundError as e:
        await channel.send("Našlo sa menu, nepodarilo sa nájst položky z menu.")
    except Exception as e:
        await channel.send(f"Neočakávaná chyba: {type(e).__name__}: {e}")

def use_commands(bot):
    # Ping príkaz
    @bot.command()
    async def ping(ctx):
        guild_id = str(ctx.guild.id)
        config = load_config()

        # Skontroluj, či pre daný server existujú údaje
        if guild_id not in config or "role_id" not in config[guild_id]:
            return
        
        expected_channel_id = config[guild_id]["channel_id"]

        if ctx.channel.id != expected_channel_id:
            return

        role_id = config[guild_id]["role_id"]
        role = ctx.guild.get_role(int(role_id))

        if role:
            await ctx.send(f'{role.mention} bu!')
        else:
            await ctx.send("Rola s týmto ID neexistuje na serveri.")

    @bot.command()
    async def info(ctx):
        info_embed = discord.Embed(
        title="ℹ️ Info",
        description=(
            "[Stránka Eat&Meet](https://eatandmeet.sk/)\n[Stránka Družby](https://www.druzbacatering.sk)\n[Stránka FiitFood](http://www.freefood.sk/menu/#fiit-food)"
        ),
        color=0x57F287
        )
        await ctx.send(embed=info_embed)

    # Príkaz na testovanie posielania obrázku
    @bot.command()
    async def testimage(ctx):
        url = "https://htmlcolorcodes.com/assets/images/colors/baby-blue-color-solid-background-1920x1080.png"
        embed = discord.Embed(title="Test obrázok")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    #@bot.command()
    #async def rmv(ctx, number: int):
        #await ctx.channel.purge(limit=number+1)

    # Príkaz na manuálne posielanie denného menu
    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def eat(ctx):
        config = load_config()
        try: 
            accessCheck(config, ctx)
            await send_enm_menu(config, ctx.channel, ctx.guild.id)
        except InvalidGuildError as e:
            return
        except InvalidChannelError as e:
            return
            #await ctx.channel.send("zly kanal")

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def druzba(ctx):
        config = load_config()
        try: 
            accessCheck(config, ctx)
            await send_druzba_menu(config, ctx.channel, ctx.guild.id)
        except InvalidGuildError as e:
            return
        except InvalidChannelError as e:
            return
            #await ctx.channel.send("zly kanal")

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def ff(ctx):
        config = load_config()
        try: 
            accessCheck(config, ctx)
            await send_fiitfood_menu(config, ctx.channel, ctx.guild.id)
        except InvalidGuildError as e:
            return
        except InvalidChannelError as e:
            return
            #await ctx.channel.send("zly kanal")

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def mnam(ctx):
        config = load_config()
        await ctx.channel.purge(limit=5)
        try: 
            accessCheck(config, ctx)
            await send_enm_menu(config, ctx.channel, ctx.guild.id)
            await send_druzba_menu(config, ctx.channel, ctx.guild.id)
            await send_fiitfood_menu(config, ctx.channel, ctx.guild.id)
        except InvalidGuildError as e:
            return
        except InvalidChannelError as e:
            return
            #await ctx.channel.send("zly kanal")