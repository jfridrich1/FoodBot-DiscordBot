from discord.ext.commands import Bot

from core.commands.embeds import send_enm_menu_embed, send_druzba_menu_embed, send_fiitfood_menu_embed

async def send_daily_menus(config, bot: Bot):
    for guild in bot.guilds:
        guild_id = str(guild.id)
        guild_config = config.get(guild_id)
        if not guild_config:
            continue

        channel_id = guild_config.get("channel_id")
        role_id = guild_config.get("role_id")

        if not channel_id:
            continue

        channel = bot.get_channel(channel_id)

        await channel.purge(limit=4)

        if role_id:
            role = channel.guild.get_role(int(role_id))
            if role:
                await channel.send(f"{role.mention}")

        if channel:
            await send_enm_menu_embed(config, channel, guild.id)
            await send_druzba_menu_embed(config, channel, guild.id)
            await send_fiitfood_menu_embed(config, channel, guild.id)

async def send_daily_menus_to_channel(config, channel, guild_id):
    guild_config = config.get(str(guild_id))
    if not guild_config:
        return

    role_id = guild_config.get("role_id")

    await channel.purge(limit=4)

    if role_id:
        role = channel.guild.get_role(int(role_id))
        if role:
            await channel.send(role.mention)

    await send_enm_menu_embed(config, channel, guild_id)
    await send_druzba_menu_embed(config, channel, guild_id)
    await send_fiitfood_menu_embed(config, channel, guild_id)