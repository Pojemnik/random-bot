import lightbulb
from lightbulb import slash_commands
from __init__ import ENABLED_GUILDS, cfg
from util import get_guild_name
import logging

class Set_custom_emoji_chance(slash_commands.SlashCommand):
    enabled_guilds = ENABLED_GUILDS
    description: str = "Set chance of selecting a custom emoji when reacting"
    chance: int = slash_commands.Option('Chance of custom emoji (%)')
    name: str = "setcustomemojichance"

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        param = context.options.chance
        if 0 > param or param > 100:
            await context.respond("Incorrect parameter, expected an integer between 0 and 100 (inclusive)")
            return
        cfg.set_value(context.guild_id, 'custom_emoji_chance', param)
        await context.respond(f'Custom emoji chance set to {param}%')
        logging.info(
            f'Custom emoji chance set to {param} on server {get_guild_name(context.bot,context.guild_id)}')


def load(bot: lightbulb.Bot):
    bot.add_slash_command(Set_custom_emoji_chance)

def unload(bot: lightbulb.Bot):
    bot.remove_slash_command(Set_custom_emoji_chance.name)