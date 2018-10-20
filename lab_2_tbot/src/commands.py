from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from . import strings


def makeUserDecor(funk):
    keyboard = [[KeyboardButton("/help", callback_data="help"),
                 KeyboardButton("/task", callback_data="task"),
                 KeyboardButton("/MyBot", callback_data="MyBot")]]
    answer = {
        "startComand": strings.hi,
        "helpComand": strings.help,
        "taskComand": strings.task,
        "solutionComand": strings.findingSolution,
        "documentMessageComand": strings.sendSolution,
    }
    reply_markup = ReplyKeyboardMarkup(keyboard)

    def makeUserDecor_(bot, update) :
        bot.send_message(chat_id = update.message.chat_id,
                         text = answer[funk.__name__],
                         reply_markup = reply_markup)
        funk(bot, update)

    return makeUserDecor_

@makeUserDecor
def startComand(bot, update):
    pass

@makeUserDecor
def helpComand(bot, update):
    pass

@makeUserDecor
def taskComand(bot, update):
    pass

@makeUserDecor
def solutionComand(bot, update):
    pass

@makeUserDecor
def documentMessageComand(bot, update):
    pass

