import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from core.commands.daily import send_daily_menus

#from core.reminders import send_reminder

def use_events(config, bot):
    @bot.event
    async def on_ready():
        await bot.change_presence(status=discord.Status.idle)

        # Spustenie plánovača pri štarte bota
        scheduler = AsyncIOScheduler()
        scheduler.add_job(send_daily_menus, CronTrigger(hour=6, minute=00), args=[config, bot])  # každodenný job, 7:00
        scheduler.start()

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        content = message.content.lower().strip()

        # dm + guild
        if "gej" in content:
            await message.channel.send('burin')

        if "burin" in content:
            await message.channel.send('🇭🇺')

        # iba guild
        
        # iba dm
        if not message.guild:
            if content == "info":
                info_embed = discord.Embed(
                    title="ℹ️ Info",
                    description=(
                        "[Stránka Eat&Meet](https://eatandmeet.sk/)\n"
                        "[Stránka Družby](https://www.druzbacatering.sk)\n"
                        "[Stránka FiitFood](http://www.freefood.sk/menu/#fiit-food)"
                    ),
                    color=0xFF2688
                )
                info_embed.set_footer(text=f"Provided by @breehze")
                await message.channel.send(embed=info_embed)
            
            if "test" in content:
                url = "https://htmlcolorcodes.com/assets/images/colors/baby-blue-color-solid-background-1920x1080.png"
                image_embed = discord.Embed(title="Test obrázok")
                image_embed.set_image(url=url)
                await message.channel.send(embed=image_embed)

        await bot.process_commands(message)
        # color=0x57F287