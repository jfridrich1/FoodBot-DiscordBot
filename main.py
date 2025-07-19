import discord
import os
import threading
from discord.ext import commands
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer

ints = discord.Intents.default()
ints.message_content = True
bot = commands.Bot(command_prefix='!', intents=ints)

def run_fake_http_server():
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running.")

    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"Fake HTTP server bezi na porte {port}")
    server.serve_forever()

threading.Thread(target=run_fake_http_server, daemon=True).start()

@bot.event
async def on_ready():
    print(f'Login {bot.user.name}')

@bot.command()
async def ping(ctx):
    await ctx.send('bu')

@bot.command()
async def gej(ctx):
    await ctx.send('burin')

load_dotenv()
bot.run(os.getenv('TOKEN'))