import os
import sys
import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from src import commands

try:
    updater = Updater(token=os.environ['COND_BOT_TOKEN'])
except KeyError:
    print("Please, run 'source SECURITY.sh' beforehand!", file=sys.stderr)
dispatcher = updater.dispatcher

startCommandHandler = CommandHandler('start', commands.startCommand)
helpCommandHandler = CommandHandler('help', commands.helpCommand)
findCommandHandler = CommandHandler('location', commands.helpCommand)
findStoresHandler = MessageHandler(Filters.location, commands.locationMessage)

dispatcher.add_handler(startCommandHandler)
dispatcher.add_handler(helpCommandHandler)
dispatcher.add_handler(findCommandHandler)
dispatcher.add_handler(findStoresHandler)

updater.start_polling(clean=True)
updater.idle()
