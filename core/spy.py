import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.errors import Forbidden

async def notify(message: discord.Message, notify_cfg: dict, bot, config: dict):

    # speci kanal poslanie
    target_guild_id = int(notify_cfg["target_guild"])
    target_channel_id = int(notify_cfg["target_channel"])

    target_guild = bot.get_guild(target_guild_id)
    if target_guild is None:
        # bot nie je na cieľovom serveri
        return

    target_channel = target_guild.get_channel(target_channel_id)
    if target_channel is None:
        # kanál neexistuje alebo nemá prístup
        return
    
    embed = discord.Embed(
        title="📢 🇭🇺 📢",
        description=f"{message.guild.name} | #{message.channel.name}",
        color=notify_cfg.get("embed_color", 0xE6921C)
    )

    embed.add_field(
        name="",
        value=f"{message.author}",
        inline=False
    )

    embed.add_field(
        name="",
        value=message.content,
        inline=False
    )

    await target_channel.send(embed=embed)


    # dm poslanie
    dm_cfg = config.get("dm_settings", {})
    dm_users = dm_cfg.get("users", {})

    for user_id in notify_cfg.get("target_users", []):
        # DM len ak má user zapnutý DM mód
        if not dm_users.get(user_id, False):
            continue

        try:
            user = await bot.fetch_user(int(user_id))
            await user.send(embed=embed)
        except Forbidden:
            continue
        except Exception:
            continue