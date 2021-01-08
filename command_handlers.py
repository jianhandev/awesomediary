from utils import \
    get_user_from_request,\
    is_not_blank
from constants import *
from api.telegram_api import send_message, send_message_with_options, send_timed_message
from beans.user import User
from cache import get_journal_entry, add_to_journal
import random
import time

# temporary variable that stores questions asked
asked_qns = []

# Returns an error message stating that command is invalid
def handle_invalid_command(**kwargs):
    return DEFAULT_ERROR_MESSAGE, False


# Returns a greeting message with instructions on how to get started
def __show_default_greeting(**kwargs):
    return DEFAULT_GREETING, False

# Starts the current journaling session
def __hi(user_input, user):
    key = random.choice(list(RANDOM_QUESTION_ABOUT_THE_DAY))
    question = RANDOM_QUESTION_ABOUT_THE_DAY[key]
    asked_qns.append(question)
    add_to_journal(user, NEXT_QUESTION + question)
    return (FIRST_QUESTION + question), True

# Generates the next question to be asked and checks that the next question is not repeated 
def __next(user_input, user):
    if not asked_qns: # Checks if the user has started the hi command first
        return NO_ENTRY, False

    key = random.choice(list(RANDOM_QUESTION))
    question = RANDOM_QUESTION[key]
    while question in asked_qns: 
        key = random.choice(list(RANDOM_QUESTION))
        question = RANDOM_QUESTION[key]
    
    asked_qns.append(question)
    add_to_journal(user, NEXT_QUESTION + question)

    return (NEXT_QUESTION + question), False

# Ends the current journaling session
def __end(user_input, user):
    asked_qns.clear()
    return BYE_MSG, False

def __today(user_input, user):
    return get_journal_entry(user), False

def is_hh_mm_time(time_string):
    try:
        time.strptime(time_string, '%H:%M')
    except ValueError:
        return False
    return len(time_string) == 5

# Set the time for the bot to ask question
def __set_reminder(user_input, user):
    splitted = user_input.split(" ")
    response = ''
    time = ''
    if len(splitted) >= 2:
        time = splitted[1]
        if is_hh_mm_time(time):
            key = random.choice(list(RANDOM_QUESTION_ABOUT_THE_DAY))
            question = RANDOM_QUESTION_ABOUT_THE_DAY[key]
            asked_qns.append(question)
            add_to_journal(user, question)
            send_timed_message(user, time, question)
            response = "Time set successfully at " + time
        else:
            response = "Please enter in the format of '/ask hh:mm'" 
    else:
        response = "Please enter in the format of '/ask hh:mm'" 
    return response


# Returns a simple tutorial of the bot
def __show_starter_menu(**kwargs):
    return "Welcome to the AwesomeDiary! This bot helps you keep track of your internal thoughts and interesting events of your day. \n\n" \
        "To start a new entry for today, say '/hi' to this bot. "\
        "After answering each question, indicate '/next' in a new message for the next question to appear. "\
        "Once your done, tell this bot to '/end' this session."


# Returns a response string with commands offered as a bulleted list
# "\u2022" is the character for bullet points
def __show_command_list(**kwargs):
    return "Here are all the commands: \n"\
        "\u2022" + " " + "/start" + ": Gives you a quick tutorial to this simple telegram bot" + "\n"\
        "\u2022" + " " + "/hi" + ": Start your new diary entry for the day" + "\n"\
        "\u2022" + " " + "/next" + ": Get a new question from the bot" + "\n"\
        "\u2022" + " " + "/end" + ": Wrap up your thoughts for today!"+ "\n"\
        "\u2022" + " " + "/today" + ": Receive an overview of your reflections today" + "\n"\
        "\u2022" + " " + "/ask" + ": Include the time in HH:mm format to receive a timely notification" + "\n"\
        "\u2022" + " " + "/commands" + ": Displays all commands (Isn't this what you typed?)" + "\n"\

# Dictionary of command actions mapped to a corresponding function that will be executed when user submits said command
COMMAND_HANDLERS = {
    'default_greeting': lambda user_input, user: __show_default_greeting(),
    'start': lambda user_input, user: __show_starter_menu(),
    'commands': lambda user_input, user: __show_command_list(),
    'hi': lambda user_input, user: __hi(user_input, user), 
    'next': lambda user_input, user: __next(user_input, user), 
    'end': lambda user_input, user: __end(user_input, user),
    'ask': lambda user_input, user: __set_reminder(user_input, user),
    'today': lambda user_input, user: __today(user_input, user)
}
