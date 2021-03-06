import logging
import sys

from src.points_finder import PointsFinder
from telegram import ChatAction
from telegram import KeyboardButton
from telegram import ParseMode
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

sys.path.append("..")
import config

from .strings import AvailableStrings

logger = logging.getLogger(__name__)

finder = PointsFinder(config.DATABASE)

keyboard = [[KeyboardButton(AvailableStrings.button_text, callback_data="location", request_location=True)]]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def startCommand(bot, update):
    try:
        bot.send_message(chat_id=update.message.chat_id,
                         text=AvailableStrings.hi,
                         reply_markup=reply_markup)
    except Exception as exc:
        logger.warning("EXCEPTION %s: %s", exc, exc.message)


def helpCommand(bot, update):
    try:
        bot.send_message(chat_id=update.message.chat_id,
                         text=AvailableStrings.help,
                         reply_markup=reply_markup)
    except Exception as exc:
        logger.warning("EXCEPTION %s: %s", exc, exc.message)


def locationMessage(bot, update):
    chat_id = update.message.chat.id
    telegram_user = update.message.from_user
    curr_location = (update.message.location.latitude, update.message.location.longitude)
    bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        locations = finder(curr_location[0], curr_location[1])
    except:
        logger.error("Unexpected error:", sys.exc_info())

    bot.send_message(chat_id=chat_id, text=AvailableStrings.finding_text_start,
                     parse_mode=ParseMode.HTML,
                     reply_markup=ReplyKeyboardRemove())
    _counter = 1
    for location in locations:
        name, latitude, longitude = "%d) %s" % (_counter, location[0]), location[1], location[2]  # :(
        address, distance = location[3], location[4]
        text_message = "%s, %d m\n\n%s" % (name, distance, address)
        bot.send_message(chat_id=chat_id,
                         text=text_message,
                         parse_mode=ParseMode.HTML)
        bot.send_location(chat_id=chat_id,
                          latitude=latitude,
                          longitude=longitude)
        _counter += 1

    bot.send_message(chat_id=chat_id, text=AvailableStrings.finding_text_final, reply_markup=reply_markup)
