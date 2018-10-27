from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ParseMode
from telegram import ReplyKeyboardRemove
from telegram import ChatAction
from . import strings
from src.points_finder import PointsFinder

finder = PointsFinder('data/base_drugstores_supermarkets.csv')

keyboard = [[KeyboardButton(strings.button_text, callback_data="location", request_location=True)]]
text_answer = {
    "startCommand": strings.hi,
    "helpCommand": strings.help,
}
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def makeUserDecor(func):
    def makeUserDecor_(bot, update) :
        bot.send_message(chat_id = update.message.chat_id,
                         text = text_answer[func.__name__],
                         reply_markup = reply_markup)
        func(bot, update)
    return makeUserDecor_

@makeUserDecor
def startCommand(bot, update):
    pass

@makeUserDecor
def helpCommand(bot, update):
    pass

def locationMessage(bot, update):
    chat_id = update.message.chat.id
    telegram_user = update.message.from_user
    curr_location = (update.message.location.latitude, update.message.location.longitude)
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    locations = finder(curr_location[0], curr_location[1])
    bot.send_message(chat_id=chat_id, text=strings.start_finding_text, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    _counter = 1
    for location in locations:
        name, latitude, longitude = '%d) %s'%(_counter, location[0]), location[1], location[2]  # :(
        bot.send_message(chat_id=chat_id, text=name, parse_mode=ParseMode.HTML)
        bot.send_location(chat_id=chat_id, latitude=latitude, longitude=longitude)
        _counter += 1

    bot.send_message(chat_id=chat_id, text=strings.final_text, reply_markup = reply_markup)
