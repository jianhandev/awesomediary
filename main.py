from flask import Flask
from flask_caching import Cache

config = {
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 60 * 20  # 20 minutes expiry for session ids
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

from controller import *

if __name__ == "__main__":
    app.run()
