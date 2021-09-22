import discord
from discord.ext import commands
import json
import random
from emoji import emojis

'''
TODO:
Remove user id from the code
Move commands code somewhere
Make a class for config
Better logging
'''

config = {}

def int_try_parse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


def get_server_command_prefix(bot: commands.Bot , message: discord.Message):
    id = message.guild.id
    if id not in config:
        try:
            with open('default_config.json') as dc:
                default_config = json.load(dc)
                config[id] = default_config
        except IOError as e:
            print(f'Critical error: {e}')
            raise e
    return config[id]['command_prefix']

bot = commands.Bot(command_prefix=get_server_command_prefix)

def save_config():
    try:
        with open('config.json','w') as f:
            json.dump(config, f)
    except IOError as e:
        print(e)
    else:
        print('Config saved')

def load_config():
    try:
        with open("config.json") as f:
            config = json.load(f)
    except IOError as e:
        print(e)
    else:
        print('Config loaded')

@bot.command()
async def save(ctx):
    save_config()
    await ctx.send('Config saved')

@bot.command()
async def łó(ctx):
    if ctx.message.author.id in []:
        await ctx.send('Nie.')
    else:
        await ctx.send('ŁóóÓÓÓÓóÓóÓÓÓóÓóÓÓÓÓóóóóóóÓóóóóóÓÓóÓÓÓÓÓÓóóÓóóÓ')

@bot.command()
async def setrand(ctx, reaction_chance):
    param, ok = int_try_parse(reaction_chance)
    if not ok or 0 > param or param > 100:
        await ctx.send("Incorrect parameter, expected an integer between 0 and 100 (inclusive)")
        return
    config[ctx.message.guild.id]['reaction_parameter'] = param
    await ctx.send(f'Reaction chance set to {param}%')
    print(f'Reaction chance set to {param} on server {ctx.guild.name}')
    save_config()

@bot.command()
async def setcustommul(ctx, custom_emoji_chance):
    param, ok = int_try_parse(custom_emoji_chance)
    if not ok or 0 > param or param > 100:
        await ctx.send("Incorrect parameter, expected an integer between 0 and 100 (inclusive)")
        return
    config[ctx.message.guild.id]['custom_emoji_chance'] = param
    await ctx.send(f'Custom emoji chance set to {param}%')
    print(f'Custom emoji chance set to {param} on server {ctx.guild.name}')
    save_config()

@bot.command()
async def setprefix(ctx, prefix):
    if prefix[0] in '#@':
        await ctx.send("Incorrect parameter, expected a string not starting with '#' or '@'")
        return
    config[ctx.message.guild.id]['command_prefix'] = prefix
    await ctx.send(f'Command prefix set to {prefix}')
    print(f'Command prefix set to {prefix} on server {ctx.guild.name}')
    save_config()
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send('Incorrect command')
    elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send(f'No argument {error.param.name} found.')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    load_config()

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

    if random.randint(1, 100) <= config[message.guild.id]['reaction_parameter']:
        if random.randint(1, 100) <= config[message.guild.id]['custom_emoji_chance']:
            await message.add_reaction(bot.emojis[random.randint(0, len(bot.emojis))])
        else:
            await message.add_reaction(emojis[random.randint(0, len(emojis))])
    
with open('token.secret') as token_file:
    token = token_file.read()
    bot.run(token)