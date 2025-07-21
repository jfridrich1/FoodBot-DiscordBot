import discord
import os
import threading
from datetime import datetime
from program import scrapping
from discord.ext import commands
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer
from exceptions import MenuNotFoundError, MenuBodyNotFoundError
from emoji_mapping import title_emoji_mapper

EMBED_COLOR = 0xffe28a
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

@bot.event
async def on_ready():
    print(f'Login {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "gej" in message.content.lower().strip():
        await message.channel.send('burin')
    if "burin" in message.content.lower().strip():
        await message.channel.send('🇭🇺')
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send('bu')

@bot.command()
async def testimage(ctx):
    url2 = "https://htmlcolorcodes.com/assets/images/colors/baby-blue-color-solid-background-1920x1080.png"
    embed = discord.Embed(title="Test obrázok")
    embed.set_image(url=url2)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def eat(ctx):
    try:
        meal_names, main_prices, secondary_prices, allergens, titles = scrapping()
        embed_list = []

        # Premazanie správ pred poslaním novej spŕavy
        await ctx.channel.purge(limit=10)

        # Získanie dnešného dátumu
        current_date = datetime.today().strftime("%-d. %-m. %Y")

        # Úvodná správa
        start_embed = discord.Embed(
            title=f"**Dnešné menu**",
            description=f"{current_date}",
            color=EMBED_COLOR
        )
        embed_list.append(start_embed)

        # Správy o jednotlivých jedlách
        for i in range(len(meal_names)):
            emoji = title_emoji_mapper(titles[i])
            embed = discord.Embed(
                title=f"{emoji} {titles[i]} \n{meal_names[i]}",
                description=f"Cena: *{main_prices[i]}*  **{secondary_prices[i]}**",
                color=EMBED_COLOR
            )
            embed.set_footer(text=f"{allergens[i]}")
            embed_list.append(embed)

        # Discord ma limit 10 embedov v embede, ak ich je viac - poslat po davkach po 10
        # Poslanie všetkých správ
        await ctx.send(embeds=embed_list)
        
    except MenuNotFoundError as e:
        await ctx.send("Nepodarilo sa nájsť dnešné menu.")
    except MenuBodyNotFoundError as e:
        await ctx.send("Našlo sa menu, nepodarilo sa nájst položky z menu.")
    except Exception as e:
        await ctx.send(f"Neočakávaná chyba: {type(e).__name__}: {e}")

if __name__ == '__main__':
    threading.Thread(target=start_bot, daemon=True).start()
    start_http_server()