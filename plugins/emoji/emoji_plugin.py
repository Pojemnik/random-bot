import lightbulb
from __init__ import ENABLED_GUILDS, cfg
from util import get_guild_name
import logging
import hikari
import random
from ._emoji import emojis

plugin = lightbulb.Plugin("emoji")


@plugin.command
@lightbulb.option('chance', 'New reaction chance (%)', type=int)
@lightbulb.command(
    name="setreactionchance",
    description="Set chance for random emoji reaction to a message",
    guilds=ENABLED_GUILDS
)
@lightbulb.implements(lightbulb.SlashCommand)
async def set_reaction_chance(context: lightbulb.Context) -> None:
    chance = context.options.chance
    if 0 > chance or chance > 100:
        await context.respond("Incorrect parameter, expected an integer between 0 and 100 (inclusive)")
        return
    cfg.set_value(context.guild_id, 'reaction_parameter', chance)
    await context.respond(f'Reaction chance set to {chance}%')
    logging.info(
        f'Reaction chance set to {chance} on server {get_guild_name(context.bot, context.guild_id)}')

    
@plugin.command
@lightbulb.option('chance', 'Chance of custom emoji (%)', type=int)
@lightbulb.command(
    name="setcustomemojichance",
    description="Set chance of selecting a custom emoji when reacting",
    guilds=ENABLED_GUILDS
)
@lightbulb.implements(lightbulb.SlashCommand)
async def set_custom_emoji_chance(context: lightbulb.Context) -> None:
    param = context.options.chance
    if 0 > param or param > 100:
        await context.respond("Incorrect parameter, expected an integer between 0 and 100 (inclusive)")
        return
    cfg.set_value(context.guild_id, 'custom_emoji_chance', param)
    await context.respond(f'Custom emoji chance set to {param}%')
    logging.info(
        f'Custom emoji chance set to {param} on server {get_guild_name(context.bot,context.guild_id)}')
    

@plugin.listener(hikari.events.message_events.GuildMessageCreateEvent, bind=True)
async def on_message(plugin: lightbulb.Plugin, event: hikari.events.message_events.GuildMessageCreateEvent) -> None:
    if (plugin.bot.get_me() is not None and event.author_id == plugin.bot.get_me().id) or (plugin.bot.get_me() is None and event.is_bot):
        return

    custom_emojis = list(plugin.bot.cache.get_emojis_view().values())
    if random.randint(1, 100) <= cfg.get_value(event.guild_id, 'reaction_parameter'):
        if random.randint(1, 100) <= cfg.get_value(event.guild_id, 'custom_emoji_chance'):
            await event.message.add_reaction(random.choice(custom_emojis))
        else:
            await event.message.add_reaction(random.choice(emojis))
    if random.randint(1, 100) <= cfg.get_value(event.guild_id, 'reaction_parameter'):
        xd = ['XD', 'xd', 'Xd', 'xD']
        if any(s in event.content for s in xd):
            await event.message.respond('XD')



def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
