import discord
import os
import threading
from discord.ext import commands
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer

from core.commands import use_commands
from core.events import use_events

#EMBED_COLOR = 0xffe28a-
load_dotenv()

# Priradenie práv botovi
bot_intents = discord.Intents.default()
bot_intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=bot_intents)

use_commands(bot)
use_events(bot)

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

# Spustenie bota a HTTP servera
if __name__ == '__main__':
    threading.Thread(target=start_bot, daemon=True).start()
    start_http_server()