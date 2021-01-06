from constants import MENU_CODES_TO_OPTIONS, DEFAULT_GREETING


# Returns an error message stating that command is invalid
def handle_invalid_command(command):
    return "Sorry, your command '{}' is invalid".format(command)


# Returns a greeting message with instructions on how to get started
def __show_default_greeting():
    return DEFAULT_GREETING


# Returns a bulleted list of features the bot offers
def __show_help_menu():
    response = "Hello there! I'm the bot for Ninja Cafe. Feel free to:\n\n"
    response += "- Order something from our menu\n"
    response += "- Ask about what's available on the menu (or use '/menu')\n"
    response += "- Check on your current orders with us\n"
    response += "- Enquire about where your order is\n"

    return response


# Returns a response string with menu items offered as a bulleted list
def __show_menu_response_for_command():
    response = "Here's the menu you asked for:\n"
    for x in range(1, len(list(MENU_CODES_TO_OPTIONS.values())) + 1):
        response += "{}: {}\n".format(x, list(MENU_CODES_TO_OPTIONS.values())[x - 1])
    response += "\nWhat would you like?\n"

    return response


# Dictionary of command actions mapped to a corresponding function that will be executed when user submits said command
COMMAND_HANDLERS = {
    'start': lambda ignored: __show_default_greeting(),
    'help': lambda ignored: __show_help_menu(),
    'menu': lambda ignored: __show_menu_response_for_command()
}
