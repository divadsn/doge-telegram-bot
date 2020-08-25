import logging
import random

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from dogebot.drawmeme import DogeImage
from telethon import TelegramClient, events


logger = logging.getLogger(__name__)

class DogeBot(object):

    def __init__(self, app_id, app_hash, phone_number):
        self.client = TelegramClient("dogebot", app_id, app_hash)
        self.client.add_event_handler(self.command_handler)
        self.phone_number = phone_number
        self.image = Image.open("doge.jpg")
        self.font = ImageFont.truetype("comicsans.ttf", 48)

    @events.register(events.NewMessage(incoming=True, forwards=False, pattern="/doge"))
    async def command_handler(self, event):
        words = set()

        # Get past messages in the group and select ~50 unique words
        async for message in self.client.iter_messages(event.chat_id):
            if message.raw_text.startswith("/"):
                continue

            for word in message.raw_text.lower().split():
                # Exclude any non-alphabetical words and @mentions
                if not word.isalpha() or word.startswith("@"):
                    continue

                words.add(word)

            if len(words) >= 50:
                break

        words = list(words)

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

    async def start(self):
        await self.client.start(phone=self.phone_number)
        logger.info("Bot started!")

        # wait for incoming messages/actions
        await self.client.run_until_disconnected()
