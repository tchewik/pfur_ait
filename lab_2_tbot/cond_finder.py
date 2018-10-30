import logging
import logging.handlers
import sys

import config
from src import commands
from src.strings import AvailableStrings
from telegram import Bot
from telegram.error import InvalidToken
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater


def setUpLoggers():
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("btcLogger")
    logger.setLevel(logging.DEBUG)
    fh = logging.handlers.TimedRotatingFileHandler(filename=config.LOGPATH, when="d", interval=7, backupCount=3)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


setUpLoggers()

logger = logging.getLogger(__name__)

try:
    Bot._validate_token(token=config.COND_BOT_TOKEN)
    updater = Updater(token=config.COND_BOT_TOKEN)
except KeyError:
    logger.warning(AvailableStrings.error_token_not_found)
    sys.exit(0)
except InvalidToken:
    logger.error(AvailableStrings.error_token_invalid)
    sys.exit(0)

dispatcher = updater.dispatcher

startCommandHandler = CommandHandler("start", commands.startCommand)
helpCommandHandler = CommandHandler("help", commands.helpCommand)
findCommandHandler = CommandHandler("location", commands.locationMessage)
findStoresHandler = MessageHandler(Filters.location, commands.locationMessage)

dispatcher.add_handler(startCommandHandler)
dispatcher.add_handler(helpCommandHandler)
dispatcher.add_handler(findCommandHandler)
dispatcher.add_handler(findStoresHandler)

try:
    updater.start_polling(clean=True)
    updater.idle()
except Exception as exc:
    logger.warning("EXCEPTION %s: %s", exc, exc.message)
