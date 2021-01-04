from api import order_api
from api.dialogflow_api import detect_intent_via_event
from api.telegram_api import send_message, send_message_with_options
from beans.user import User
from cache import get_current_order, add_to_order, clear_from_order
from constants import MENU_CODES_TO_OPTIONS, DEFAULT_ERROR_MESSAGE, MAIN_SUGGESTIONS, ONGOING_ORDER_SUGGESTIONS
from utils import default_if_blank, is_not_blank, get_items_from_response


# Returns a generic fallback message
def handle_invalid_intent(user: User, intent_result, session_id):
    response = "Sorry, I did not understand you. What were you saying?"

    return send_message(user, intent_result.intent.display_name, session_id, response)


# Displays the response found in the intent result as is, with no options
def __display_default_response(user: User, intent_result, session_id):
    response = default_if_blank(intent_result.fulfillment_text, DEFAULT_ERROR_MESSAGE)

    return send_message(user, intent_result.intent.display_name, session_id, response)


# Displays the response found in the intent result formatted with the user's name, with main menu suggestions
def __display_main_greeting(user: User, intent_result, session_id):
    response = intent_result.fulfillment_text.format(default_if_blank(user.name, 'Customer'))

    return send_message_with_options(user, intent_result.intent.display_name, session_id, response,
                                     *MAIN_SUGGESTIONS, row_width=1)


# Displays response with menu items offered as a bulleted list
def __show_menu_response(user: User, intent_result, session_id):
    response = "Glad you asked! Here's what we offer:\n"
    for x in range(1, len(list(MENU_CODES_TO_OPTIONS.values())) + 1):
        response += "{}: {}\n".format(x, list(MENU_CODES_TO_OPTIONS.values())[x - 1])
    response += "\nWhat would you like?\n"

    return send_message(user, intent_result.intent.display_name, session_id, response)


# Displays response in intent result with a list of menu items as Telegram buttons
def __show_menu_options(user: User, intent_result, session_id):
    response = intent_result.fulfillment_text
    if is_not_blank(response):
        return send_message_with_options(user, intent_result.intent.display_name, session_id, response,
                                         *list(MENU_CODES_TO_OPTIONS.values()))
    else:
        return send_message(user, intent_result.intent.display_name, session_id, DEFAULT_ERROR_MESSAGE)


# Calls Order API to fetch user's current orders and formats them in the response
# If no orders are found, an appropriate message is shown accordingly
def __show_orders(user: User, intent_result, session_id):
    orders = order_api.list_orders(user)

    if len(orders) > 0:
        response = "Here are your current orders:\n"
        for x in range(1, len(orders) + 1):
            response += "{}. {}\n<Placed @ {}>\n\n"\
                .format(x, orders[x - 1]['order_description'], orders[x - 1]['timestamp'])
        response += "\nHow else can I help you?"

        return send_message_with_options(user, intent_result.intent.display_name, session_id, response,
                                         *MAIN_SUGGESTIONS, row_width=1)
    else:
        response = "You have no orders yet. Let me know if you wanna order something!"
        return send_message(user, intent_result.intent.display_name, session_id, response)


# Updates the session cache with the items captured in the response from user, includes "I'm done" option
def __update_order(user: User, intent_result, session_id):
    order_items = get_items_from_response(intent_result)

    if len(order_items) > 0:
        response = intent_result.fulfillment_text
        add_to_order(user, session_id, order_items)
        return send_message_with_options(user, intent_result.intent.display_name, session_id, response, "I'm done!")
    else:
        response = "Sorry, I wasn't able to detect your order. Could you repeat yourself?"
        return send_message(user, intent_result.intent.display_name, session_id, response)


# Clears the menu items from the session cache for the user
def __cancel_order(user: User, intent_result, session_id):
    response = intent_result.fulfillment_text
    clear_from_order(user, session_id)
    return send_message(user, intent_result.intent.display_name, session_id, response)


# Formats the list of menu items for the user's order in session cache, with options to submit or cancel the order
# Triggers an event call to Dialogflow to reset contexts to main menu if no menu items found
def __confirm_order(user: User, intent_result, session_id):
    order_items = get_current_order(user, session_id)

    if len(order_items) > 0:
        response = "Here are the items in your order:\n"
        for name, count in order_items.items():
            response += "- {}x {}\n".format(count,
                                            default_if_blank(MENU_CODES_TO_OPTIONS[name], 'N.A.'))
        response += "\nSubmit?"

        return send_message_with_options(user, intent_result.intent.display_name, session_id, response,
                                         "Yes, submit my order!", "Nah, cancel it")
    else:
        detect_intent_via_event(session_id, 'NINJA_CAFE_MAIN_EVENT')

        response = "Oops, you don't have any items in your order. Let me know how else I can help you!"

        return send_message(user, intent_result.intent.display_name, session_id, response)


# Calls Order API to create a new order with the user's given menu items in session cache
# Clears the cache after creating the order
def __submit_order(user: User, intent_result, session_id):
    order_items = get_current_order(user, session_id)

    response = intent_result.fulfillment_text

    order_api.create_order(user, order_items)
    clear_from_order(user, session_id)

    return send_message(user, intent_result.intent.display_name, session_id, response)


# Displays suggested inputs user can raise to the bot after hitting a fallback in the main menu
def __show_main_suggestions(user: User, intent_result, session_id):
    response = intent_result.fulfillment_text

    return send_message_with_options(user, intent_result.intent.display_name, session_id, response,
                                     *MAIN_SUGGESTIONS, row_width=1)


# Displays suggested inputs user can raise to the bot after hitting a fallback in the process of creating an order
def __show_ongoing_order_suggestions(user: User, intent_result, session_id):
    response = intent_result.fulfillment_text

    return send_message_with_options(user, intent_result.intent.display_name, session_id, response,
                                     *ONGOING_ORDER_SUGGESTIONS, row_width=1)


# Dictionary of intent actions mapped to a corresponding function that will be executed when the intent is matched
INTENT_HANDLERS = {
    'DISPLAY_DEFAULT_RESPONSE': __display_default_response,
    'DISPLAY_MAIN_GREETING': __display_main_greeting,
    'SHOW_MENU_RESPONSE': __show_menu_response,
    'SHOW_MENU_OPTIONS': __show_menu_options,
    'SHOW_ORDERS': __show_orders,
    'UPDATE_ORDER': __update_order,
    'CONFIRM_ORDER': __confirm_order,
    'CANCEL_ORDER': __cancel_order,
    'SUBMIT_ORDER': __submit_order,
    'SHOW_MAIN_SUGGESTIONS': __show_main_suggestions,
    'SHOW_ONGOING_ORDER_SUGGESTIONS': __show_ongoing_order_suggestions
}
