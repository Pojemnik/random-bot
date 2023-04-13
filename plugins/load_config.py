import lightbulb
from __init__ import ENABLED_GUILDS, cfg

plugin = lightbulb.Plugin("load_config")


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command(
    name="load_config",
    description="Loads bot config",
    guilds=ENABLED_GUILDS
)
@lightbulb.implements(lightbulb.SlashCommand)
async def load_config(context: lightbulb.Context) -> None:
    cfg.load()
    await context.respond('Config loaded')


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
