from program import scrapping
import discord
import os
import threading
from discord.ext import commands
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer

load_dotenv()

ints = discord.Intents.default()
ints.message_content = True
bot = commands.Bot(command_prefix='!', intents=ints)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'...Bot is running...')

def start_http_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Fake HTTP server bezi na porte {port}")
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
async def eat(ctx):
    meals, main_prices, secondary_prices = scrapping()

    response = "\n".join([f"{meals[i]} {main_prices[i]} {secondary_prices[i]}" for i in range(len(meals))])
    await ctx.send(f"**Dnešné menu:**\n{response}")

def start_bot():
    bot.run(os.getenv('TOKEN'))

if __name__ == '__main__':
    threading.Thread(target=start_bot, daemon=True).start()
    start_http_server()