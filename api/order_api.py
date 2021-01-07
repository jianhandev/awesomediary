import json

from requests import request

from beans.user import User
from constants import MENU_CODES_TO_OPTIONS
from utils import default_if_blank


# Calls an API to list orders for a user given his Telegram user id
def list_orders(user: User):
    return list(map(__parse_order, json.loads(__send_request('GET', get_orders_url(user), ()).text)))


# Calls an API to create a new order (with one or many menu items) for a user given his Telegram user id
def create_order(user: User, order_items):
    return __send_request('POST', get_orders_url(user),
                          json.dumps({
                              "items": [
                                  {'code': name, 'count': count} for name, count in order_items.items()
                              ]
                          }))


# Parses the response from list orders endpoint into a list of order descriptions and timestamps
def __parse_order(order):
    return {
        "order_description": ", ".join(
            map(lambda item: "{}x {}".format(item['count'], MENU_CODES_TO_OPTIONS[item['code']]),
                filter(lambda item: item['code'] in MENU_CODES_TO_OPTIONS, order['items']))),
        "timestamp": order['timestamp']
    }


def get_orders_url(user: User):
    return "https://api-dev.ninjavan.co/global/ninjacafe/orders/{}".format(default_if_blank(user.id, ''))


def __send_request(method, url, body):
    headers = {
        "Connection": "keep-alive",
        "Content-Type": "application/json"
    }

    response = request(method, headers=headers, url=url, data=body)
    return response
