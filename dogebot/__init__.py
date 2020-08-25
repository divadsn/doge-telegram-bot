import os
import sys
import logging


# enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

APP_ID = os.getenv("APP_ID", None)
APP_HASH = os.getenv("APP_HASH", None)
BOT_TOKEN = os.getenv("BOT_TOKEN", None)
