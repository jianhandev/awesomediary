import uuid

from beans.item import Item
from beans.session import Session
from beans.user import User
from main import cache
from utils import default_if_blank, is_not_blank
from command_handlers import asked_qns
import os
from datetime import date 


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


# Returns the Dictionary of items (and their counts) for the user in the current session order, or an empty Dict if none
def get_current_order(user: User, session_id):
    orders_key = __current_orders_key(user, session_id)
    orders = cache.get(orders_key)

    if orders is not None and len(orders) > 0:
        return orders
    else:
        cache.set(orders_key, {})
        return {}


# Adds an response to the user's current entry (response is a string)
def add_to_entry(user: User, session_id, items):
    orders_key = __current_orders_key(user, session_id)
    orders = get_current_order(user, session_id)

    for item in items:
        orders = __add_item_to_orders(orders, item)

    cache.set(orders_key, orders)

    return orders

# gets the message journal entry from the chat
def get_message():
    # To Do
    return ''


# Convert the message journal entry into a Markdown file by user and session_id
def add_to_journal(user: User, session: Session, user_input):
#msg: get_message(user, session_id)

    try:
        os.makedirs(user)
    except:
        os.chdir(user)
            
    # latest_qn = ""
    # try:
    #     latest_qn = asked_qns[-1]
    # except:
    #     latest_qn = "Unknown question"
    
    try:
        f = open(str(user.name) + str(date.today()) + ".md", "x")
        f.write(user_input)
    except:
        f = open(str(user.name) + str(date.today()) + ".md", "a")
        f.write("\n" + user_input)
    f.close()


# Clears the list of Item objects for the user's current order
def clear_from_order(user: User, session_id):
    orders_key = __current_orders_key(user, session_id)
    cache.delete(orders_key)


def __add_item_to_orders(orders, item: Item):

    if item.name in orders:
        orders[item.name] = orders[item.name] + item.count
    else:
        orders[item.name] = item.count

    return orders


def __session_key(user: User):
    return "session_{}".format(default_if_blank(user.id, ''))


def __current_orders_key(user: User, session_id):
    return "orders_{}_{}".format(default_if_blank(user.id, ''), session_id)
