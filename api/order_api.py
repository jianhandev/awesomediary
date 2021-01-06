import json

from requests import request

from beans.user import User
from constants import MENU_CODES_TO_OPTIONS
from utils import default_if_blank


# Calls an API to list orders for a user given his Telegram user id
def list_orders(user: User):
    # FILL IN CODE
    return


# Calls an API to create a new order (with one or many menu items) for a user given his Telegram user id
def create_order(user: User, order_items):
    # FILL IN CODE
    # Request format
    #     {
    #         "items": [
    #             {
    #                 "code": "MENU_ITEM_COOKIE",
    #                 "count": 2
    #             },
    #             ...
    #         ]
    #     }
    return


# Parses the response from list orders endpoint into a list of order descriptions and timestamps
def __parse_order(order):
    # FILL IN CODE
    # Expected response format:
    # [
    #     {
    #         "items": [
    #             {
    #                 "code": "MENU_ITEM_COOKIE",
    #                 "count": 2
    #             },
    #             ...
    #         ],
    #         "timestamp": "29th December 2020, 12 PM"
    #     },
    #     ...
    # ]
    return


def get_orders_url(user: User):
    return "https://api-qa.ninjavan.co/global/ninjacafe/orders/{}".format(default_if_blank(user.id, ''))


def __send_request(method, url, body):
    # FILL IN CODE
    return
