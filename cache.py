from beans.item import Item
from beans.session import Session
from beans.user import User
from main import cache
from utils import default_if_blank, is_not_blank
from os import path, mkdir
from datetime import date 
from constants import *
import uuid

# Returns a session id for the current user, or generates a new one (UUID)
def get_current_session(user: User):
    session_key = __session_key(user)
    session_id = cache.get(session_key)

    if is_not_blank(session_id):
        return Session(session_id, False)
    else:
        new_session_id = uuid.uuid4().hex
        cache.set(session_key, new_session_id)
        return Session(new_session_id, True)

# Reads the Markdown file and returns a log of the entry
def get_journal_entry(user: User):
    filePath = "data/{}/{}.md".format(default_if_blank(user.handle,''), str(date.today()))
    if not path.exists(filePath):
        response = "You haven't written anything today. Start writing now!"
    else:
        f = open(filePath, "r") # Modify to get correct file based on user and date 
        response = "*Today's Date:* " + str(date.today()) + '\n'
        for line in f:
            if line in FIRST_QUESTION or line in NEXT_QUESTION:
                response += "*" + f.readline().rstrip('\n') + "*" + '\n'
            elif line == BYE_MSG:
                pass
            else:
                response += line
    return response

# Convert the message journal entry into a Markdown file by user and session_id
def add_to_journal(user: User, user_input):

    if not path.exists("data"):
        mkdir("data")

    user_folder = "data/{}".format(default_if_blank(user.handle, ''))

    if not path.exists(user_folder):
        mkdir(user_folder)
    
    new_file_name = user_folder + '/' + str(date.today()) + ".md"

    try:
        f = open(new_file_name, 'x')
        f.write(user_input)
    except: 
        f = open(new_file_name, 'a')
        f.write("\n" + user_input)

    f.close()

def __session_key(user: User):
    return "session_{}".format(default_if_blank(user.id, ''))