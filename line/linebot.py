# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
from abc import ABCMeta, abstractmethod

import requests


class UnexpectedEventTypeException(Exception):
    """
    unexpected event type
    """


class MessagePostError(Exception):
    """
    fail to post the message to line bot server
    """


class SignatureValidationError(Exception):
    """
    fail to validate line bot callback request signature
    """


class AbstractLineBot(metaclass=ABCMeta):
    MESSAGING_API_ENDPOINT = "https://api.line.me"
    REPLAY_MESSAGE_API_URL = MESSAGING_API_ENDPOINT + "/v2/bot/message/reply"
    PUSH_MESSAGE_API_URL = MESSAGING_API_ENDPOINT + "/v2/bot/message/push"

    def __init__(self, channel_id, channel_secret, channel_access_token, **kwargs):
        self.channel_id = channel_id
        self.channel_secret = channel_secret
        self.request_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(channel_access_token),
        }

    def handle_callback(self, json_text, signature):
        self._validate_signature(json_text, signature)

        data = json.loads(json_text)
        for event in data.get("events", []):
            self._handle_event(event)

    def _send_reply(self, reply_token, message):
        payload = {
            "replyToken": reply_token,
            "messages": [message]
        }

        response = requests.post(AbstractLineBot.REPLAY_MESSAGE_API_URL, json=payload, headers=self.request_headers)
        if not response.status_code == 200:
            raise Exception(response.status_code)  # TODO: fix this exception to match status code

    def _validate_signature(self, json_text, signature):
        if not signature or not json_text:
            raise SignatureValidationError()

        mac = hmac.new(self.channel_secret.encode(), json_text.encode(), hashlib.sha256)
        expected_signature = base64.b64encode(mac.digest()).decode()
        if not expected_signature == signature:
            raise SignatureValidationError()

    def _handle_event(self, event):
        """
        event format
        {
            "replyToken": "hahahaha",
            "type": "{event type}",
            "timestamp": 123123,
            "source": ...
        }
        """
        event_type = event["type"]
        if event_type == "message":
            self._handle_message(event)
        elif event_type == "follow":
            self._handle_follow(event)
        elif event_type == "unfollow":
            self._handle_unfollow(event)
        elif event_type == "join":
            self._handle_join(event)
        elif event_type == "leave":
            self._handle_leave(event)
        elif event_type == "postback":
            self._handle_postback(event)
        elif event_type == "beacon":
            self._handle_beacon(event)
        else:
            raise UnexpectedEventTypeException()

    @abstractmethod
    def _handle_message(self, event):
        """
        text message format
        {
            "id": "325708",
            "type": "text",
            "text": "Hello, world"
        }

        image, audio, video message format
        {
            "id": "325708",
            "type": "{format}"
        }

        location message format
        {
            "id": "325708",
            "type": "location",
            "title": "my location",
            "address": "〒150-0002 東京都渋谷区渋谷２丁目２１−１",
            "latitude": 35.65910807942215,
            "longitude": 139.70372892916203
        }

        sticker message format
        {
            "id": "325708",
            "type": "sticker",
            "packageId": "1",
            "stickerId": "1"
        }
        """
        pass

    @abstractmethod
    def _handle_follow(self, event):
        pass

    @abstractmethod
    def _handle_unfollow(self, event):
        pass

    @abstractmethod
    def _handle_join(self, event):
        pass

    @abstractmethod
    def _handle_leave(self, event):
        pass

    @abstractmethod
    def _handle_postback(self, event):
        pass

    @abstractmethod
    def _handle_beacon(self, event):
        pass


