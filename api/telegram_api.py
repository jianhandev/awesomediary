# from os import SCHED_BATCH
from cache import add_to_journal
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from beans.user import User
from constants import MOOD, TELEGRAM_API_TOKEN

import schedule
from threading import Thread
from time import sleep

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

# Send a message to Telegram chat without options
def send_message(user: User, state, session_id, response):
    # Note: state and session_id are only used for logging
    print("Sending response '{}' for user {} session {} state '{}'"
          .format(response, user.id, session_id, state))

    return bot.send_message(user.id, response, reply_markup="markdown")


# Send a message to Telegram chat with options, with two options in a row by default
def send_message_with_options(user: User, state, session_id, response, *options, row_width=5):
    print("Sending response '{}' with options '{}' for user {} session {} state '{}'"
          .format(response, options, user.id, session_id, state))

    keyboard = [
        [InlineKeyboardButton(MOOD["happy"], callback_data='happy')],
        [InlineKeyboardButton(MOOD["sad"], callback_data='sad')],
        [InlineKeyboardButton(MOOD["angry"], callback_data='angry')],
        [InlineKeyboardButton(MOOD["meh"], callback_data='meh')],
        [InlineKeyboardButton(MOOD["annoyed"], callback_data='annoyed')]
    ]

    markup = InlineKeyboardMarkup(keyboard)
    
    return bot.send_message(user.id, response, reply_markup=markup)

# can share the link ure referencing?
# https://python-telegram-bot.readthedocs.io/en/stable/telegram.callbackquery.html
# https://core.telegram.org/bots/api#callbackquery
# https://www.mindk.com/blog/how-to-develop-a-chat-bot/

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
   data = query.data 
   handle_callback(query)


def handle_callback(query):
    response = "Noted/Dont be sad/stay happy... <3"
    # required to remove the loading state
    bot.answer_callback_query(query.id, text=response)
    # Write mood into journal 
    # add_to_journal(user, query) 
    # send_result(query.message, response])

# def send_result(message, ex_code):
#    bot.send_message(
#        message.chat.id, response,
#     #    reply_markup=get_update_keyboard(ex),
#     #    parse_mode='HTML'
#    ) 

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

def function_to_run(user: User, response):
    return bot.send_message(user.id, response)

def send_timed_message(user: User, time, response):    # Create the job in schedule.
    print("Sending response {} for user {} "
          .format(response, user.id))
    schedule.every().day.at(time).do(function_to_run, user, response)

    # Spin up a thread to run the schedule check so it doesn't block your bot.
    # This will take the function schedule_checker which will check every second
    # to see if the scheduled job needs to be ran.
    Thread(target=schedule_checker).start()
