import os
import telegram
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from .src import commands

updater = Updater(token=os.environ['COND_BOT_TOKEN'])
dispatcher = updater.dispatcher

startCommandHandler = CommandHandler('start', commands.startComand)
helpCommandHandler = CommandHandler('help', commands.helpComand)
solutionCommandHandler = CommandHandler('MyBot', commands.solutionComand)
taskCommandHandler = CommandHandler('task', commands.taskComand)

documentMessageHandler = MessageHandler(Filters.document, commands.documentMessageComand)
stickerMessageHandler = MessageHandler(Filters.sticker, commands.stickerMessageComand)

dispatcher.add_handler(startCommandHandler)
dispatcher.add_handler(helpCommandHandler)
dispatcher.add_handler(solutionCommandHandler)
dispatcher.add_handler(taskCommandHandler)
dispatcher.add_handler(documentMessageHandler)

updater.start_polling(clean=True)
updater.idle()
