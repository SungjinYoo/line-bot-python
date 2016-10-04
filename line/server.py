# -*- coding: utf-8 -*-

from flask import Flask
from flask import request

from line.message import create_text
from line.settings import *
from line.linebot import AbstractLineBot

LINE_SIGNATURE_HEADER = "X_LINE_SIGNATURE"


class MyLineBot(AbstractLineBot):
    def __init__(self, channel_id, channel_secret, channel_access_token):
        super().__init__(channel_id, channel_secret, channel_access_token)

    def _handle_postback(self, event):
        pass

    def _handle_message(self, event):
        message = event["message"]
        if not message["type"] == "text":
            return

        reply_token = event["replyToken"]
        input_text = message["text"]

        self._send_reply(reply_token, create_text(input_text))

    def _handle_leave(self, event):
        pass

    def _handle_unfollow(self, event):
        pass

    def _handle_join(self, event):
        pass

    def _handle_follow(self, event):
        pass

    def _handle_beacon(self, event):
        pass


line_bot = MyLineBot(CHANNEL_ID, CHANNEL_SECRET, CHANNEL_ACCESS_TOKEN)
simple_callback_server = Flask("line")


@simple_callback_server.route("/line/callback", methods=["POST"])
def parse_event():
    signature = request.headers.get(LINE_SIGNATURE_HEADER)
    json_text = request.data.decode()

    line_bot.handle_callback(json_text, signature)

    return "OK"

if __name__ == "__main__":
    simple_callback_server.run("0.0.0.0", 10080)
