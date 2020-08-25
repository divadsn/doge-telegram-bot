import logging
import random

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from dogebot.collection import MaxSizeList
#from dogebot.drawmeme import DogeImage

from telethon import TelegramClient, events


logger = logging.getLogger(__name__)

modifiers = ["so", "such", "many", "much", "very"]

class DogeBot(object):

    def __init__(self, app_id, app_hash, bot_token):
        self.client = TelegramClient("dogebot", app_id, app_hash)
        self.client.add_event_handler(self.command_handler)
        self.client.add_event_handler(self.word_handler)

        self.bot_token = bot_token
        self.chats = {}

        self.image = Image.open("doge.jpg")
        self.font = ImageFont.truetype("comicsans.ttf", 48)

    @events.register(events.NewMessage(incoming=True, forwards=False, pattern="/doge"))
    async def command_handler(self, event):
        words = list(self.chats[event.chat_id])

        # Order the list using random
        random.shuffle(words)

        # Shuffle those modifiers too
        random.shuffle(modifiers)

        # Create image canvas using doge template
        image = DogeImage(self.image.copy(), self.font)
        image.add_phrase("wow")
        
        # Select 4 phrases + wow
        for i in range(4):
            image.add_phrase(modifiers[i], words[i])

        # Save image to BytesIO
        result = BytesIO()
        image.save(result, format="jpeg")
        result.seek(0)

        # Send result as reply to the chat
        await event.message.reply(file=result)

        # Close any open I/O from memory
        result.close()

    @events.register(events.NewMessage(incoming=True))
    async def word_handler(self, event):
        message = event.message

        # Ignore any command related messages starting with /
        if message.raw_text.startswith("/"):
            return

        # Check if we have a list already for this chat in memory
        if event.chat_id in self.chats:
            words = self.chats[event.chat_id]
        else:
            words = []

        for word in message.raw_text.lower().split():
            # Exclude any non-alphabetical words, @mentions and duplicates
            if not word.isalpha() or word.startswith("@") or word in words:
                continue

            # Delete first word if the list is larger or equal 50
            if len(words) >= 50:
                words.pop(0)

            words.append(word)

        # Store updated word list for this chat
        self.chats[event.chat_id] = words

    async def start(self):
        await self.client.start(bot_token=self.bot_token)
        logger.info("Bot started!")

        # wait for incoming messages/actions
        await self.client.run_until_disconnected()
