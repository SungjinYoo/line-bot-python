import unittest

from linebot.models.event import EventParser


class TestCallbackRequestTest(unittest.TestCase):

    def test_event_parse(self):
        with open("fixtures/callback-request.json") as f:
            callback_request = f.read()
            event = EventParser.parse(callback_request)
