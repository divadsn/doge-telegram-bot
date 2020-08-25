import os
import sys
import logging

# enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# if version < 3.7, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    logger.error("You MUST have a python version of at least 3.7! Multiple features depend on this. Bot quitting.")
    quit(1)

# you must get your own app_id and app_hash
# from https://my.telegram.org, under API Development.
APP_ID = os.getenv("APP_ID", None)
APP_HASH = os.getenv("APP_HASH", None)

if not APP_ID or not APP_HASH:
    logger.warning("No app credentials provided for MTProto, files over 50 MB will not be uploaded!")
    quit(1)

BOT_TOKEN = os.getenv("BOT_TOKEN", None)
