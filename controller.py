from pprint import pprint
from flask import request
                                                                                                              
from api.telegram_api import send_message
from beans.session import Session
from beans.user import User
from cache import add_to_journal, get_current_session
from command_handlers import COMMAND_HANDLERS, handle_invalid_command
from main import app
from utils import \
    get_user_from_request, \
    get_user_input_from_request, \
    is_not_blank, \
    get_user_command_from_request

# Validates incoming webhook request to make sure required fields are present, before processing
@app.route('/webhook', methods=['POST'])
def webhook():
    req_body = request.get_json()
    user = get_user_from_request(req_body)
    user_input = get_user_input_from_request(req_body)
    commands = get_user_command_from_request(req_body)

    if user == '':
        return ''

    elif is_not_blank(user.id, user_input):
        session = get_current_session(user)
        if 'message' in req_body:
            __process_request(user, session, user_input, commands)

    else:
        pass

    return ''

# Process incoming request as either one with commands or a response to prompted questions
def __process_request(user: User, session: Session, user_input, commands):
    if len(commands) > 0:
        __process_telegram_commands(user, session, commands, user_input)
    else:
        print(user_input)
        add_to_journal(user, user_input)

# Processes all individual commands found in user input, concatenating them into a single response for user
# Does not support options for individual commands since we are responding to potentially multiple commands in input
def __process_telegram_commands(user: User, session: Session, commands, user_input):
    chosen_command = commands.pop()
    result = __process_individual_telegram_command_with_parameter(chosen_command, user_input, user)
    send_message(user, ", " .join(commands), session.id, result)

def __process_individual_telegram_command (command) :
    if is_not_blank(command):
        return COMMAND_HANDLERS.get(command, handle_invalid_command)()
    else:
        return ''

def __process_individual_telegram_command_with_parameter (command, user_input, user) :
    if is_not_blank(command):
        return COMMAND_HANDLERS.get(command, handle_invalid_command)(user_input, user)
    else:
        return ''
