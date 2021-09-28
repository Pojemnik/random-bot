import lightbulb
from lightbulb import slash_commands
from __init__ import ENABLED_GUILDS, cfg

class Lo(slash_commands.SlashCommand):
    enabled_guilds = ENABLED_GUILDS
    description: str = "Sends łóó string"
    name = 'łó'

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        if context.author.id in cfg.get_value(context.guild_id, "lo_command_blacklist"):
            await context.respond('Nie.')
        else:
            await context.respond('ŁóóÓÓÓÓóÓóÓÓÓóÓóÓÓÓÓóóóóóóÓóóóóóÓÓóÓÓÓÓÓÓóóÓóóÓ')

            
def load(bot: lightbulb.Bot):
    bot.add_slash_command(Lo)

def unload(bot: lightbulb.Bot):
    bot.remove_slash_command(Lo.name)