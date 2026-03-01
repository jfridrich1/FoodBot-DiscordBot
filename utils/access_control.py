from utils.exceptions import InvalidGuildError, InvalidChannelError

def check_access(config, ctx) -> None:
    guild_id = str(ctx.guild.id)

    guild_config = config.get(guild_id)

    if guild_config is None or "channel_id" not in guild_config:
        raise InvalidGuildError()
        
    expected_channel_id = int(guild_config["channel_id"])

    if ctx.channel.id != expected_channel_id:
        raise InvalidChannelError()