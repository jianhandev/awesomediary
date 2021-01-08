from utils import get_user_from_request
from constants import RANDOM_QUESTION, DEFAULT_GREETING, DEFAULT_ERROR_MESSAGE, RANDOM_QUESTION_ABOUT_THE_DAY
from api.telegram_api import send_message, send_message_with_options
from beans.user import User
import random

# temporary variable that stores questions asked
asked_qns = []

# Returns an error message stating that command is invalid
def handle_invalid_command(command):
    return DEFAULT_ERROR_MESSAGE


# Returns a greeting message with instructions on how to get started
def __show_default_greeting():
    return DEFAULT_GREETING

# Starts the current journaling session
def __hi(command):
    
    key = random.choice(list(RANDOM_QUESTION_ABOUT_THE_DAY))
    question = RANDOM_QUESTION_ABOUT_THE_DAY[key]
    # question = get_question()
    asked_qns.append(question)
    response = "Here's your first question! \n"
    return response + question

# Generates the next question to be asked and checks that the next question is not repeated 
def __next():
    if not asked_qns: # Checks if the user has started the hi command first
        return "You haven't started an entry for today!"

    key = random.choice(list(RANDOM_QUESTION))
    question = RANDOM_QUESTION[key]
    # question = get_question()
    while question in asked_qns: 
        key = random.choice(list(RANDOM_QUESTION))
        question = RANDOM_QUESTION[key]
        # question = get_question()
    
    asked_qns.append(question)
    response = "Here's your next question :) \n"
    return response + question

# Ends the current journaling session
def __end():
    asked_qns.clear()
    return "Come back tomorrow! ;)"

# Set the time for the bot to ask question
def __set_reminder():
    return "/ask hh:MM" 

# Returns a simple tutorial of the bot
def __show_starter_menu():
    return "Welcome to the AwesomeDiary! This bot helps you keep track of your internal thoughts and interesting events of your day. \n" \
        "To start a new entry, say '/hi' to this bot. "\
        "After answering each question, indicate '/next' for the next question to appear. "\
        "Once your done, tell this bot to '/end' this session."


# Returns a response string with commands offered as a bulleted list
# "\u2022" is the character for bullet points
def __show_command_list():
    return "Here are all the commands: \n"\
        "\u2022" + " " + "/hi" + ": To start a new diary entry" + "\n"\
        "\u2022" + " " + "/next" + ": Get a new question from the mod" + "\n"\
        "\u2022" + " " + "/end" + ": Wrap up your thoughts for today!"

# Dictionary of command actions mapped to a corresponding function that will be executed when user submits said command
COMMAND_HANDLERS = {
    'default_greeting': lambda ignored: __show_default_greeting(),
    'start': lambda ignored: __show_starter_menu(),
    'commands': lambda ignored: __show_command_list(),
    'hi': lambda ignored: __hi(), 
    'next': lambda ignored: __next(), 
    'end': lambda ignored: __end(),
    'ask': lambda ignored: __set_reminder()
}
