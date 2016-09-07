from flask import Flask
from flask import request

from .conf.settings import *
from .client import LineBotClient

CHANNEL_SIGNATURE_HEADER = "X-LINE-ChannelSignature"


line_bot = LineBotClient(CHANNEL_ID, CHANNEL_SECRET, CHANNEL_MID)
simple_callback_server = Flask("linebot")


class CallbackValidationError(Exception):
    """
    fail to validate line bot callback request
    """


@simple_callback_server.route("/linebot/callback", methods=["GET"])
def parse_event():
    signature = request.headers.get(CHANNEL_SIGNATURE_HEADER)
    json_text = request.data
    if not line_bot.validate_signature(json_text, signature):
        raise CallbackValidationError()

    return "OK"

if __name__ == "__main__":
    simple_callback_server.run("0.0.0.0", 10080)