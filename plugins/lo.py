import lightbulb
from __init__ import ENABLED_GUILDS, cfg

plugin = lightbulb.Plugin("set_reaction_chance")


@plugin.command
@lightbulb.command(
    name="łó",
    description="Sends łóó string",
    guilds=ENABLED_GUILDS
)
@lightbulb.implements(lightbulb.SlashCommand)
async def lo(context: lightbulb.Context) -> None:
    if context.author.id in cfg.get_value(context.guild_id, "lo_command_blacklist"):
        await context.respond('Nie.')
    else:
        await context.respond('ŁóóÓÓÓÓóÓóÓÓÓóÓóÓÓÓÓóóóóóóÓóóóóóÓÓóÓÓÓÓÓÓóóÓóóÓ')

            
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
