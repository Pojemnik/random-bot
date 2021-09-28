from logging import exception
import lightbulb
import random
from emoji import emojis
import hikari
import hikari.events.lifetime_events
import hikari.events.message_events
import hikari.messages
import inspect
from lightbulb import slash_commands
from config import Config

'''
TODO:
Move commands code somewhere
Better logging
'''

ENABLED_GUILDS = [367006768078913536]


def int_try_parse(value: str) -> int:
    try:
        return int(value), True
    except ValueError:
        return value, False


def get_guild_name(snowflake: hikari.Snowflake) -> str:
    guild = bot.cache.get_guild(snowflake)
    if guild is None:
        return str(snowflake)
    return guild.name


token = ''
with open('token.secret') as token_file:
    token = token_file.read().strip()
if token == '':
    raise Exception('Token not found')
bot = lightbulb.Bot(token=token, slash_commands_only=True)
cfg = Config()
cfg.load()


class Load_config(slash_commands.SlashCommand):
    enabled_guilds = ENABLED_GUILDS
    description: str = "Saves bot config"
    checks = [lightbulb.owner_only]

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        cfg.load()
        await context.respond('Config loaded')


bot.add_slash_command(Load_config)


class Lo(slash_commands.SlashCommand):
    enabled_guilds = ENABLED_GUILDS
    description: str = "Sends łóó string"
    name = 'łó'

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        if context.author.id in cfg.get_value(context.guild_id, "lo_command_blacklist"):
            await context.respond('Nie.')
        else:
            await context.respond('ŁóóÓÓÓÓóÓóÓÓÓóÓóÓÓÓÓóóóóóóÓóóóóóÓÓóÓÓÓÓÓÓóóÓóóÓ')


bot.add_slash_command(Lo)


class Setrand(slash_commands.SlashCommand):
    enabled_guilds = ENABLED_GUILDS
    description: str = "Set chance for random emoji reaction to a message"
    chance: int = slash_commands.Option("New reaction chance (%)")

    async def callback(self, context: slash_commands.SlashCommandContext):
        chance = context.options["chance"].value
        if 0 > chance or chance > 100:
            await context.respond("Incorrect parameter, expected an integer between 0 and 100 (inclusive)")
            return
        cfg.set_value(context.guild_id, 'reaction_parameter', chance)
        await context.respond(f'Reaction chance set to {chance}%')
        print(
            f'Reaction chance set to {chance} on server {get_guild_name(context.guild_id)}')


bot.add_slash_command(Setrand)


class Setcustommul(slash_commands.SlashCommand):
    enabled_guilds = ENABLED_GUILDS
    description: str = "Set chance of selecting a custom emoji when reacting"
    chance: int = slash_commands.Option('Chance of custom emoji (%)')

    async def callback(self, context: slash_commands.SlashCommandContext) -> None:
        param = context.options["chance"].value
        if 0 > param or param > 100:
            await context.respond("Incorrect parameter, expected an integer between 0 and 100 (inclusive)")
            return
        cfg.set_value(context.guild_id, 'custom_emoji_chance', param)
        await context.respond(f'Custom emoji chance set to {param}%')
        print(
            f'Custom emoji chance set to {param} on server {get_guild_name(context.guild_id)}')


bot.add_slash_command(Setcustommul)


@ bot.listen(lightbulb.SlashCommandErrorEvent)
async def on_error(event: lightbulb.SlashCommandErrorEvent):
    if(isinstance(event.exception, lightbulb.errors.NotOwner)):
        await event.context.respond("Only bot owner can load config")
    else:
        raise event.exception


@ bot.listen(hikari.ShardReadyEvent)
async def ready_listener(event: hikari.ShardReadyEvent):
    print(f'We have logged in as {event.my_user.id}')


@ bot.listen(hikari.events.message_events.GuildMessageCreateEvent)
async def on_message(event: hikari.events.message_events.GuildMessageCreateEvent):

    if (bot.get_me() is not None and event.author_id == bot.get_me().id) or (bot.get_me() is None and event.is_bot):
        return

    custom_emojis = list(bot.cache.get_emojis_view().values())
    if random.randint(1, 100) <= cfg.get_value(event.guild_id, 'reaction_parameter'):
        if random.randint(1, 100) <= cfg.get_value(event.guild_id, 'custom_emoji_chance'):
            await event.message.add_reaction(random.choice(custom_emojis))
        else:
            await event.message.add_reaction(random.choice(emojis))

bot.run()
