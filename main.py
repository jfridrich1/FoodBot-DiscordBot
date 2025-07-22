import discord
import os
import threading
import json
from datetime import datetime
from program import scrapping
from discord.ext import commands
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer
from exceptions import MenuNotFoundError, MenuBodyNotFoundError
from emoji_mapping import title_emoji_mapper

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

#EMBED_COLOR = 0xffe28a
CONFIG_FILE = "config.json"
load_dotenv()

# Priradenie práv botovi
bot_intents = discord.Intents.default()
bot_intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=bot_intents)

# Falošný HTTP kvôli web hostovaniu
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'...Bot is running...')

def start_bot():
    bot.run(os.getenv('TOKEN'))

def start_http_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Fake HTTP server running on port {port}.")
    server.serve_forever()

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump({}, f)

def load_config():
    with open(CONFIG_FILE,"r") as f:
        return json.load(f)

@bot.event
async def on_ready():
    print(f'Login {bot.user.name}')

    # Spustenie plánovača pri štarte bota
    scheduler = AsyncIOScheduler()
    #scheduler.add_job(daily_menu, CronTrigger(hour=0, minute=0))  # každý deň o polnoci
    scheduler.add_job(daily_menu, CronTrigger(second="*/30"))
    scheduler.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "gej" in message.content.lower().strip():
        await message.channel.send('burin')
    if "burin" in message.content.lower().strip():
        await message.channel.send('🇭🇺')
    await bot.process_commands(message)

# Ping príkaz
@bot.command()
async def ping(ctx):
    await ctx.send('bu')

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

async def daily_menu():
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
            title=f"**Dnešné menu**",
            description=f"{current_date}",
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

if __name__ == '__main__':
    threading.Thread(target=start_bot, daemon=True).start()
    start_http_server()