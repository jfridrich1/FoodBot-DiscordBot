import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from core.commands import daily_update

from core.spy import notify
from utils.config import save_config

def use_events(config, bot):
    @bot.event
    async def on_ready():
        #print(f'Login {bot.user.name}')
        await bot.change_presence(status=discord.Status.idle)

        # Spustenie plánovača pri štarte bota
        scheduler = AsyncIOScheduler()
        scheduler.add_job(daily_update, CronTrigger(hour=6, minute=00), args=[config, bot])  # každodenný job
        #scheduler.add_job(daily_update, CronTrigger(hour=15, minute=00), args=[bot])  # test job
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
        if message.guild:
            guild_cfg = config.get(str(message.guild.id))

            if guild_cfg:
                notify_cfg = guild_cfg.get("notify")

                if notify_cfg and notify_cfg.get("enabled"):
                    allowed_users = notify_cfg.get("trigger_users", [])

                    if str(message.author.id) in allowed_users:
                        await notify(message, notify_cfg, bot, config)
        
        # iba dm
        if not message.guild:
            if content == "dm":
                user_id = str(message.author.id)

                dm_cfg = config.setdefault("dm_settings", {})
                admins = dm_cfg.get("admins", [])

                if user_id not in admins:
                    return

                users = dm_cfg.setdefault("users", {})

                current = users.get(user_id, False)
                users[user_id] = not current

                await message.channel.send(
                    f"dm {'ON' if users[user_id] else 'OFF'}"
                )

                save_config(config)

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