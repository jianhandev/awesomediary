from random import randrange
import requests
import json


DEFAULT_DIALOGFLOW_LANGUAGE_CODE = "en"

DEFAULT_GREETING = 'Hi Glad we could talk today, just say \'hi\'or let me know what you need!'
DEFAULT_ERROR_MESSAGE = 'Sorry, something went wrong. Please try again later!'

MOOD = {
    "happy": "~(≧▽≦)/~",
    "sad": "(>_<)",
    "angry": "(♯｀∧´)",
    "meh": "(´･_･`)",
    "annoyed": "(-_-ll)" 
}

RANDOM_QUESTION_ABOUT_THE_DAY = {
    1:"What kind of day are you having?",
    2:"Did you dream about anything last night?",
    3:"What is the happiest moment for you today?",
    4:"Any person you are grateful for today?", 
    5:"Something interesting that happened today?"
}

RANDOM_QUESTION = {
    1: "What's something you were afraid of as a child?",
    2: "What's something difficult you had to do?",
    3: "What's an embarrassing moment that happened to you?",
    4: "Who is someone you've lost? What are some of your memories about that person?",
    5: "What's something that helped to shape your outlook to life?",
    6: "Describe your teachers at school.",
    7: "Describe your best childhood friend and your relationship with this person.",
    8: "When you were a child, how did you imagine your adult self?",
    9: "What's your earliest memory?",
    10: "What are some of the memories you associate with springtime? With summer, fall, and winter?"
}

NO_ENTRY = "You haven't started an entry for today!"
FIRST_QUESTION = "Here's your first question!\n"
NEXT_QUESTION = "Here's your next question :)\n"
BYE_MSG = "Come back tomorrow! ;)"

# Change the following to suit your project
DIALOGFLOW_PROJECT_ID = "ninja-van-dialogflow-devmy"
GOOGLE_SERVICE_ACCOUNT_FILE_PATH = "ninja-van-dialogflow-devmy.json"
TELEGRAM_API_TOKEN = "1538593503:AAENwT_YNS24IuenvSHT_gf5ri1DkmZiT70"

# def get_question():
#     rand = randrange(1, 15)
#     questions = json.loads('questions.json')

#     current_question = questions[str(rand)]
#     return current_question
