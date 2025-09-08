from utils.exceptions import InvalidGuildError, InvalidChannelError

def accessCheck(config, ctx):
    guild_id = str(ctx.guild.id)

    if guild_id not in config or "channel_id" not in config[guild_id]:
        raise InvalidGuildError
        #return
        
    expected_channel_id = config[guild_id]["channel_id"]

    if ctx.channel.id != expected_channel_id:
        raise InvalidChannelError
        #return