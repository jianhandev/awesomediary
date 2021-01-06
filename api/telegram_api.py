import telebot
from telebot import types

from beans.user import User
from constants import TELEGRAM_API_TOKEN

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)


# Send a message to Telegram chat without options
def send_message(user: User, state, session_id, response):
    # FILL IN CODE
    # Note: state and session_id are only used for logging
    return


# Send a message to Telegram chat with options, with two options in a row by default
def send_message_with_options(user: User, state, session_id, response, *options, row_width=2):
    # FILL IN CODE
    # Note: state and session_id are only used for logging
    return
