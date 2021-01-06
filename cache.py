import uuid

from beans.item import Item
from beans.session import Session
from beans.user import User
from main import cache
from utils import default_if_blank, is_not_blank


# Returns a session id for the current user, or generates a new one (UUID)
def get_current_session(user: User):
    # FILL IN CODE
    return


# Returns the Dictionary of items (and their counts) for the user in the current session order, or an empty Dict if none
def get_current_order(user: User, session_id):
    # FILL IN CODE
    return


# Adds a list of Item objects to the user's current order
def add_to_order(user: User, session_id, items):
    # FILL IN CODE
    return


# Clears the list of Item objects for the user's current order
def clear_from_order(user: User, session_id):
    # FILL IN CODE
    return


def __add_item_to_orders(orders, item: Item):
    # FILL IN CODE
    return


def __session_key(user: User):
    # FILL IN CODE
    return


def __current_orders_key(user: User, session_id):
    # FILL IN CODE
    return
