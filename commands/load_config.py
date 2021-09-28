import lightbulb
from lightbulb import slash_commands
from __init__ import ENABLED_GUILDS,cfg


class Load_config(slash_commands.SlashCommand):
    enabled_guilds = ENABLED_GUILDS
    description: str = "Loads bot config"
    checks = [lightbulb.owner_only]
    name = "load_config"

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        cfg.load()
        await context.respond('Config loaded')

def load(bot: lightbulb.Bot):
    bot.add_slash_command(Load_config)

def unload(bot: lightbulb.Bot):
    bot.remove_slash_command(Load_config.name)