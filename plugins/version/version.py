import lightbulb
from __init__ import ENABLED_GUILDS, cfg

plugin = lightbulb.Plugin("version")

VERSION_STRING = 'v2.3.0'

@plugin.command
@lightbulb.command(
    name="version",
    description="Prints version number",
    guilds=ENABLED_GUILDS
)
@lightbulb.implements(lightbulb.SlashCommand)
async def version(context: lightbulb.Context) -> None:
    await context.respond(f'Random bot version: {VERSION_STRING}')
            
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
