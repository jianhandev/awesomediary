from requests import request
import constants
from beans.user import User
from utils import default_if_blank


# Calls an API to list orders for a user given his Telegram user id
def list_orders(user: User):
    # !!! Commented out first since API is not done, also returns dummy data
    # return json.loads(__send_request('GET', get_orders_url(user), ()).text)
    return [
        {
            "order_description": "2x Rye Sourdough Bread, 1x Teriyaki Chicken Burger, 5x, Minute Steak Frites",
            "timestamp": "29th December 2020, 12 PM"
        },
        {
            "order_description": "2x Spaghetti Aglio Olio, 1x Almond Crunch Cookie",
            "timestamp": "29th December 2020, 5 PM"
        }
    ]


# Calls an API to create a new order (with one or many menu items) for a user given his Telegram user id
def create_order(user: User, order_items):
    # !!! Commented out first since API is not done
    # return __send_request('POST', get_orders_url(user), order_items)
    return {}


def get_orders_url(user: User):
    return "https://api.com/sg/ninjacafe/%s/orders".format(default_if_blank(user.id, ''))


def __send_request(method, url, body):
    headers = {
        "Connection": "keep-alive",
        "Authorization": "Bearer " + constants.INTERNAL_ACCESS_TOKEN
    }

    response = request(method, headers=headers, url=url, data=body)
    return response
