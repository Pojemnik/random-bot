from logging import FileHandler, exception
import lightbulb
import random
from emoji import emojis
import hikari
import hikari.events.lifetime_events
import hikari.events.message_events
import hikari.messages
from __init__ import cfg
from pathlib import Path
import logging


def create_bot() -> lightbulb.Bot:
    token = ''
    with open('token.secret') as token_file:
        token = token_file.read().strip()
    if token == '':
        raise Exception('Token not found')

    init_logger()
    bot = lightbulb.Bot(token=token, slash_commands_only=True)
    commands = Path("./commands").glob("*.py")
    for c in commands:
        bot.load_extension(f"commands.{c.stem}")
    return bot


def init_logger():
    format = logging.Formatter("%(asctime)-15s: %(levelname)s: %(message)s")

    logger = logging.root
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("randombot2.log")
    file_handler.setFormatter(format)
    logger.addHandler(file_handler)


def main():
    bot = create_bot()

    @ bot.listen(lightbulb.SlashCommandErrorEvent)
    async def on_error(event: lightbulb.SlashCommandErrorEvent):
        if(isinstance(event.exception, lightbulb.errors.NotOwner)):
            await event.context.respond("Only bot owner can load config")
            logging.warn(
                f"User {event.context.author.id} tried to use owner-only command {event.context.command.name}")
        else:
            raise event.exception

    @ bot.listen(hikari.ShardReadyEvent)
    async def ready_listener(event: hikari.ShardReadyEvent):
        logging.info(f'We have logged in as {event.my_user.id}')

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


if __name__ == "__main__":
    main()
