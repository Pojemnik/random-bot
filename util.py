import hikari
import lightbulb

def get_guild_name(bot: lightbulb.Bot, snowflake: hikari.Snowflake) -> str:
    guild = bot.cache.get_guild(snowflake)
    if guild is None:
        return str(snowflake)
    return guild.name