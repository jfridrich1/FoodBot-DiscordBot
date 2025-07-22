from discord.ext import commands
from datetime import datetime
from scraper.scraper import scrapping
from utils.config import load_config
from discord.ext.commands import Bot
from utils.emoji_map import title_emoji_mapper
from scraper.exceptions import MenuNotFoundError, MenuBodyNotFoundError
import discord

async def daily_menu(bot: Bot):
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
        if channel:
            await send_daily_menu(channel, guild.id)

async def send_daily_menu(channel, guild_id):
    try:
        # Premazanie správ pred poslaním novej spŕavy
        await channel.purge(limit=10)
        meal_names, main_prices, secondary_prices, allergens, meal_categories = scrapping()
        config = load_config()
        embed_color = config.get(str(guild_id), {}).get("embed_color", 0xffe28a)

        # Získanie dnešného dátumu
        current_date = datetime.today().strftime("%-d. %-m. %Y")
        embed_list = []

        # Úvodná správa
        start_embed = discord.Embed(
            title=f"**{current_date} : Dnešné menu**",
            #description=f"{current_date}",
            color=embed_color
        )
        embed_list.append(start_embed)

        # Správy o jednotlivých jedlách
        for i in range(len(meal_names)):
            emoji = title_emoji_mapper(meal_categories[i])
            embed = discord.Embed(
                title=f"{emoji} {meal_categories[i]} \n{meal_names[i]}",
                description=f"Cena: *{main_prices[i]}*  **{secondary_prices[i]}**",
                color=embed_color
            )
            embed.set_footer(text=f"{allergens[i]}")
            embed_list.append(embed)

        # Discord má limit 10 embedov v embede, ak ich je viac, treba poslať po dávkach po 10
        # Poslanie všetkých správ
        await channel.send(embeds=embed_list)
        
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
        await ctx.send('bu')

    @bot.command()
    async def info(ctx):
        embed = discord.Embed(
        title="ℹ️ Info o botovi",
        description=(
            "[🌐 Stránka Eat&Meet](https://eatandmeet.sk/)\n"
            "[💻 GitHub Repository](https://github.com/jfridrich1/EatNMeet-DiscordBot)"
        ),
        color=0x57F287
        )
        #embed.set_footer(text="Eat&Meet bot")
        await ctx.send(embed=embed)

    # Príkaz na testovanie posielania obrázku
    @bot.command()
    async def testimage(ctx):
        url2 = "https://htmlcolorcodes.com/assets/images/colors/baby-blue-color-solid-background-1920x1080.png"
        embed = discord.Embed(title="Test obrázok")
        embed.set_image(url=url2)
        await ctx.send(embed=embed)

    # Príkaz na manuálne posielanie denného menu
    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def eat(ctx):
        await send_daily_menu(ctx.channel, ctx.guild.id)