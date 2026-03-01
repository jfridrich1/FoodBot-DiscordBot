from discord.ext import commands
from discord.ext.commands import Bot

from core.commands.daily import send_daily_menus_to_channel
from core.commands.embeds import send_enm_menu_embed, send_druzba_menu_embed, send_fiitfood_menu_embed

from utils.access_control import check_access
from utils.exceptions import InvalidGuildError, InvalidChannelError


def use_commands(config, bot):
    @bot.command()
    async def ping(ctx):
        guild_id = str(ctx.guild.id)

        # Skontroluj, či pre daný server existujú údaje
        if guild_id not in config or "role_id" not in config[guild_id]:
            return
        
        expected_channel_id = config[guild_id]["channel_id"]

        if ctx.channel.id != expected_channel_id:
            return

        role_id = config[guild_id]["role_id"]
        role = ctx.guild.get_role(int(role_id))

        if role:
            await ctx.send(f'{role.mention} bu!')
        else:
            await ctx.send("Rola s týmto ID neexistuje na serveri.")

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def eat1(ctx):
        try: 
            check_access(config, ctx)
            await send_enm_menu_embed(config, ctx.channel, ctx.guild.id)
        except InvalidGuildError:
            return
        except InvalidChannelError:
            return

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def druzba1(ctx):
        try: 
            check_access(config, ctx)
            await send_druzba_menu_embed(config, ctx.channel, ctx.guild.id)
        except InvalidGuildError:
            return
        except InvalidChannelError:
            return

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def ff1(ctx):
        try: 
            check_access(config, ctx)
            await send_fiitfood_menu_embed(config, ctx.channel, ctx.guild.id)
        except InvalidGuildError:
            return
        except InvalidChannelError:
            return
    
    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def daily(ctx):
        try:
            check_access(config, ctx)
            await send_daily_menus_to_channel(config, ctx.channel, ctx.guild.id)
        except InvalidGuildError:
            return
        except InvalidChannelError:
            return