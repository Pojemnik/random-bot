#!/home/pi/Python3.9/Python-3.9.7/python

import lightbulb
import hikari
import logging
import os


def create_bot() -> lightbulb.BotApp:
    token = ''
    with open('token.secret') as token_file:
        token = token_file.read().strip()
    if token == '':
        raise Exception('Token not found')

    init_logger()
    bot = lightbulb.BotApp(token=token, intents=hikari.Intents.GUILD_MESSAGES | hikari.Intents.MESSAGE_CONTENT | hikari.Intents.GUILDS)
    bot.load_extensions_from("./plugins", recursive=True)
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

    @bot.listen(lightbulb.events.SlashCommandErrorEvent)
    async def on_error(event: lightbulb.events.SlashCommandErrorEvent):
        if (isinstance(event.exception, lightbulb.errors.NotOwner)):
            await event.context.respond("Only bot owner can load config")
            logging.warn(
                f"User {event.context.author.id} tried to use owner-only command {event.context.command.name}")
        else:
            raise event.exception

    @bot.listen(hikari.ShardReadyEvent)
    async def ready_listener(event: hikari.ShardReadyEvent):
        logging.info(f'We have logged in as {event.my_user.id}')

    bot.run()


if __name__ == "__main__":
    if os.name != "nt":
        # uvloop is only available on UNIX systems, but instead of coding
        # for the OS, we include this if statement to make life easier.
        import uvloop
        uvloop.install()
    main()
