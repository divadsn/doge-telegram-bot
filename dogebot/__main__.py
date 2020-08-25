import asyncio

from dogebot import APP_ID, APP_HASH, PHONE_NUMBER
from dogebot.bot import DogeBot


bot = DogeBot(APP_ID, APP_HASH, PHONE_NUMBER)

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(bot.start())
    except KeyboardInterrupt:
        bot.client.disconnect()
