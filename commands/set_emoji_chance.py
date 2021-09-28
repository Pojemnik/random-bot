import lightbulb
from lightbulb import slash_commands
from __init__ import ENABLED_GUILDS, cfg
from util import get_guild_name
import logging

class Set_emoji_chance(slash_commands.SlashCommand):
    enabled_guilds = ENABLED_GUILDS
    description: str = "Set chance for random emoji reaction to a message"
    chance: int = slash_commands.Option("New reaction chance (%)")
    name: str = "setreactionchance"

    async def callback(self, context: slash_commands.SlashCommandContext):
        chance = context.options["chance"].value
        if 0 > chance or chance > 100:
            await context.respond("Incorrect parameter, expected an integer between 0 and 100 (inclusive)")
            return
        cfg.set_value(context.guild_id, 'reaction_parameter', chance)
        await context.respond(f'Reaction chance set to {chance}%')
        logging.info(
            f'Reaction chance set to {chance} on server {get_guild_name(context.bot, context.guild_id)}')


def load(bot: lightbulb.Bot):
    bot.add_slash_command(Set_emoji_chance)

def unload(bot: lightbulb.Bot):
    bot.remove_slash_command(Set_emoji_chance.name)