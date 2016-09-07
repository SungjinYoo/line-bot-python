import hashlib
import hmac

import requests

from .models import message
from .models.event import EventType


class MessagePostError(Exception):
    """
    fail to post the message to line bot server
    """


class RecipientType:
    USER = 1


class LineBotClient:
    DEFAULT_SENDING_MESSAGE_CHANNEL_ID = "1383378250"
    DEFAULT_SENDING_MESSAGE_EVENT_ID = "138311608800106203"
    DEFAULT_SENDING_MULTIPLE_MESSAGES_EVENT_ID = "140177271400161403"
    DEFAULT_USER_AGENT = "line-botsdk-python/" + '0.0.1' # TODO: version?
    DEFAULT_EVENT_API_END_POINT = "https://trialbot-api.line.me/v1/events"
    DEFAULT_BOT_API_END_POINT = "https://trialbot-api.line.me/v1"
    HASH_ALGORITHM = hashlib.sha256

    def __init__(self, channel_id, channel_secret, channel_mid, **kwargs):
        self.channel_id = channel_id
        self.channel_secret = channel_secret
        self.channel_mid = channel_mid
        self.event_api_end_point = kwargs.get('eventAPIEndpoint', LineBotClient.DEFAULT_EVENT_API_END_POINT)

    def validate_signature(self, json_text, signature):
        if not signature or not json_text:
            return False

        mac = hmac.new(self.channel_secret.encode(), json_text.encode(), hashlib.sha256)
        return mac.digest() == signature

    def send_text(self, mid, text):
        self._send_message(mid, message.create_text(text))

    def _send_message(self, mid, data, to_type=RecipientType.USER, event_type=EventType.SENDING_MESSAGE):
        mid = mid if isinstance(mid, list) else [mid]
        payload = {**data, **{'toType': to_type}}
        self._post_message(mid, payload, event_type)

    def _post_message(self, mid, payload, event_type):
        payload['toChannel'] = LineBotClient.DEFAULT_SENDING_MESSAGE_CHANNEL_ID
        payload['eventType'] = event_type
        response = requests.post(self.event_api_endpoint, json=payload)
        if response.status_code != 200:
            raise MessagePostError()
