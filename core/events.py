import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from core.commands import daily_menu

def use_events(bot):
    @bot.event
    async def on_ready():
        print(f'Login {bot.user.name}')

        # Spustenie plánovača pri štarte bota
        scheduler = AsyncIOScheduler()
        scheduler.add_job(daily_menu, CronTrigger(hour=0, minute=0))  # každý deň o polnoci
        scheduler.add_job(daily_menu, CronTrigger(minute="*/7"))
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