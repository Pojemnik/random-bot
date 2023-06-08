import lightbulb
from __init__ import ENABLED_GUILDS, cfg
from util import get_guild_name
import logging
import hikari
import random
from ._emoji import emojis
from hikari.snowflakes import Snowflake
from hikari.emojis import Emoji
from collections import defaultdict

MAX_EMOJI_QUEUE_LEN = 10

plugin = lightbulb.Plugin("emoji")

last_reactions: defaultdict[(Snowflake, Snowflake), list[(Snowflake, Emoji)]] = defaultdict(list)

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
    

@plugin.command
@lightbulb.command(
    name="removereaction",
    description="Remove last reaction",
    guilds=ENABLED_GUILDS
)
@lightbulb.implements(lightbulb.SlashCommand)
async def remove_reaction(context: lightbulb.Context) -> None:
    key = (context.guild_id, context.channel_id)
    if key not in last_reactions:
        await context.respond("No my reactions on this channel")
        return
    last_reactions_list = last_reactions[key]
    if len(last_reactions_list) == 0:
        await context.respond("No my reactions on this channel")
        return
    last_reaction = last_reactions_list.pop()
    message = await context.get_channel().fetch_message(last_reaction[0])
    await message.remove_reaction(last_reaction[1])
    await context.respond("Ok")


@plugin.listener(hikari.events.message_events.GuildMessageCreateEvent, bind=True)
async def on_message(plugin: lightbulb.Plugin, event: hikari.events.message_events.GuildMessageCreateEvent) -> None:
    if (plugin.bot.get_me() is not None and event.author_id == plugin.bot.get_me().id) or (plugin.bot.get_me() is None and event.is_bot):
        return

    custom_emojis = list(plugin.bot.cache.get_emojis_view().values())
    emoji = get_random_emoji(custom_emojis, cfg.get_value(event.guild_id, 'reaction_parameter'), cfg.get_value(event.guild_id, 'custom_emoji_chance'))
    await event.message.add_reaction(emoji)
    
    last_reactions_list = last_reactions[(event.guild_id, event.channel_id)]
    last_reactions_list.append((event.message_id, emoji))
    
    if len(last_reactions_list) > MAX_EMOJI_QUEUE_LEN:
        last_reactions_list.pop(0)
        
    await reactXD(event)

async def reactXD(event):
    if random.randint(1, 100) <= cfg.get_value(event.guild_id, 'reaction_parameter'):
        xd = ['XD', 'xd', 'Xd', 'xD']
        if any(s in event.content for s in xd):
            await event.message.respond('XD')


def get_random_emoji(custom_emojis: list[Emoji], reaction_chance: int, custom_emoji_chance: int) -> Emoji:
    if random.randint(1, 100) <= reaction_chance:
        if random.randint(1, 100) <= custom_emoji_chance:
            return random.choice(custom_emojis)
        else:
            return Emoji.parse(random.choice(emojis))

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
