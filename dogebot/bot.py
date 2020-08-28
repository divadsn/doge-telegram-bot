import logging
import random

from io import BytesIO
from PIL import Image, ImageFont

from telethon import TelegramClient, events

from dogebot.doge import DogeImage
from dogebot.utils import get_sender_name

logger = logging.getLogger(__name__)


class DogeBot(object):

    def __init__(self, app_id, app_hash, bot_token):
        self.client = TelegramClient("dogebot", app_id, app_hash)
        self.client.add_event_handler(self.command_handler)
        self.client.add_event_handler(self.word_handler)

        self.bot_token = bot_token
        self.chats = {}

        self.image = Image.open("doge.jpg")
        self.font = ImageFont.truetype("comicsans.ttf", 52)
        self.modifiers = ["so", "such", "many", "much", "very"]

    @events.register(events.NewMessage(incoming=True, forwards=False, pattern="/doge"))
    async def command_handler(self, event):
        logger.info(f"User {get_sender_name(await event.get_sender())} issued command: {event.message.raw_text}")

        # Check if we have a word list for this chat
        if event.chat_id not in self.chats:
            await event.message.reply(message="I don't have any words written down for this chat yet!")
            return

        words = list(self.chats[event.chat_id])

        # Check if we have at least 4 unique words
        if len(words) < 4:
            await event.message.reply(message="I need at least 4 words to create an image!")
            return

        # Order the list using random
        random.shuffle(words)

        # Shuffle those modifiers too
        random.shuffle(self.modifiers)

        # Create image canvas using doge template
        image = DogeImage(self.image.copy(), self.font)
        image.add_phrase("wow")
        
        # Select 4 phrases + wow
        for i in range(4):
            image.add_phrase(self.modifiers[i], words[i])

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
            # Exclude any non-alphabetical words, @mentions, letters and non-words
            if not word.isalpha() or word.startswith("@") or len(word) < 4 or len(word) > 27:
                continue

            # Delete first word if the list is larger or equal 30
            if len(words) >= 30:
                words.pop(0)

            words.append(word)

        # Store updated word list for this chat
        self.chats[event.chat_id] = words

    async def start(self):
        await self.client.start(bot_token=self.bot_token)
        logger.info("Bot started!")

        # wait for incoming messages/actions
        await self.client.run_until_disconnected()
