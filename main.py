from logging import exception
import lightbulb
import json
import random
from emoji import emojis
import hikari
import hikari.events.lifetime_events
import hikari.events.message_events
import hikari.messages
import inspect

'''
TODO:
Load command blacklist form a file
Move commands code somewhere
Make a class for config
Better logging
Slash commands
'''
config = {}

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


def get_server_command_prefix(bot: lightbulb.command_handler.Bot, message: hikari.messages.Message) -> str:
    id = str(message.guild_id)
    if id not in config:
        try:
            with open('default_config.json') as dc:
                default_config = json.load(dc)
                config[id] = default_config
        except IOError as e:
            print(f'Critical error: {e}')
            raise e
    return config[id]['command_prefix']


token = ''
with open('token.secret') as token_file:
    token = token_file.read()
if token == '':
    raise Exception('Token not found')
bot = lightbulb.Bot(token=token, prefix=get_server_command_prefix)


def save_config():
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f)
    except IOError as e:
        print(e)
    else:
        print('Config saved')


def load_config():
    global config
    try:
        with open("config.json") as f:
            config = json.load(f)
    except IOError as e:
        print(e)
    else:
        print('Config loaded')


@bot.command(allow_extra_arguments=False)
async def save(ctx: lightbulb.Context):
    save_config()
    await ctx.get_channel().send('Config saved')


@bot.command(allow_extra_arguments=False)
async def łó(ctx: lightbulb.Context):
    if ctx.message.author.id in []:
        await ctx.get_channel().send('Nie.')
    else:
        await ctx.get_channel().send('ŁóóÓÓÓÓóÓóÓÓÓóÓóÓÓÓÓóóóóóóÓóóóóóÓÓóÓÓÓÓÓÓóóÓóóÓ')


@bot.command(allow_extra_arguments=False)
async def setrand(ctx: lightbulb.Context, reaction_chance: str):
    param, ok = int_try_parse(reaction_chance)
    if not ok or 0 > param or param > 100:
        await ctx.get_channel().send("Incorrect parameter, expected an integer between 0 and 100 (inclusive)")
        return
    config[str(ctx.message.guild_id)]['reaction_parameter'] = param
    await ctx.get_channel().send(f'Reaction chance set to {param}%')
    print(
        f'Reaction chance set to {param} on server {get_guild_name(ctx.guild_id)}')
    save_config()


@bot.command(allow_extra_arguments=False)
async def setcustommul(ctx: lightbulb.Context, custom_emoji_chance: str):
    param, ok = int_try_parse(custom_emoji_chance)
    if not ok or 0 > param or param > 100:
        await ctx.get_channel().send("Incorrect parameter, expected an integer between 0 and 100 (inclusive)")
        return
    config[str(ctx.message.guild_id)]['custom_emoji_chance'] = param
    await ctx.get_channel().send(f'Custom emoji chance set to {param}%')
    print(
        f'Custom emoji chance set to {param} on server {get_guild_name(ctx.guild_id)}')
    save_config()


@bot.command(allow_extra_arguments=False)
async def setprefix(ctx: lightbulb.Context, prefix: str):
    if prefix[0] in '#@':
        await ctx.get_channel().send("Incorrect parameter, expected a string not starting with '#' or '@'")
        return
    config[str(ctx.message.guild_id)]['command_prefix'] = prefix
    await ctx.get_channel().send(f'Command prefix set to {prefix}')
    print(
        f'Command prefix set to {prefix} on server {get_guild_name(ctx.guild_id)}')
    save_config()


@bot.listen(lightbulb.events.CommandErrorEvent)
async def on_command_error(event: lightbulb.events.CommandErrorEvent):
    if isinstance(event.exception, lightbulb.errors.CommandNotFound):
        await event.message.respond("Unknown command")
    if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
        await event.message.respond(f'Not enough arguments. This command shoud take {len(inspect.signature(event.command.callback).parameters) - 1} arguments')
    if isinstance(event.exception, lightbulb.errors.TooManyArguments):
        await event.message.respond(f'Too many arguments. This command shoud take {len(inspect.signature(event.command.callback).parameters) - 1} arguments')


@bot.listen(hikari.ShardReadyEvent)
async def ready_listener(event: hikari.ShardReadyEvent):
    print(f'We have logged in as {event.my_user.id}')
    load_config()


@bot.listen(hikari.events.message_events.GuildMessageCreateEvent)
async def on_message(event: hikari.events.message_events.GuildMessageCreateEvent):

    if (bot.get_me() is not None and event.author_id == bot.get_me().id) or (bot.get_me() is None and event.is_bot):
        return

    custom_emojis = list(bot.cache.get_emojis_view().values())
    if random.randint(1, 100) <= config[str(event.guild_id)]['reaction_parameter']:
        if random.randint(1, 100) <= config[str(event.guild_id)]['custom_emoji_chance']:
            await event.message.add_reaction(random.choice(custom_emojis))
        else:
            await event.message.add_reaction(random.choice(emojis))


bot.run()
