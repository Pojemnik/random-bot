import lightbulb
from __init__ import ENABLED_GUILDS, cfg
import json
import semver
from os import path

plugin = lightbulb.Plugin("version")

VERSION_STRING = '2.4.0'
CHANGELOG_FILE = path.join(path.dirname(__file__),'changelog.json')

@plugin.command
@lightbulb.command(
    name="version",
    description="Prints version number",
    guilds=ENABLED_GUILDS
)
@lightbulb.implements(lightbulb.SlashCommand)
async def version(context: lightbulb.Context) -> None:
    await context.respond(f'Random bot version: {VERSION_STRING}')

@plugin.command
@lightbulb.option('filter', 'Version filter', type=str, required=False, default=VERSION_STRING)
@lightbulb.command(
    name="changelog",
    description="Prints changelog",
    guilds=ENABLED_GUILDS
)
@lightbulb.implements(lightbulb.SlashCommand)
async def changelog(context: lightbulb.Context) -> None:
    arg = context.options.filter
    try:
        min_version = semver.Version.parse(arg)
    except ValueError as e:
        await context.respond(f'Incorrect version filter')
        return
    
    with open(CHANGELOG_FILE, 'r') as f:
        log = json.load(f)
        log = filter(lambda x: min_version <= x[0], log)
        log = map(lambda x: f"{x[0]}: {x[1]}", log)
        log = "\n".join(log)
        await context.respond(f"\n{log}")
            
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
