import unittest
import hmac
import hashlib

from line.linebot import LineBotClient


class TestValidation(unittest.TestCase):

    CHANNEL_ID = "CID"
    CHANNEL_SECRET = "SECRET"
    CHANNEL_MID = "MID"

    def test_valid_signature(self):
        client = LineBotClient(TestValidation.CHANNEL_ID, TestValidation.CHANNEL_SECRET, TestValidation.CHANNEL_MID)

        request_body = "{}"
        signature = self._compute_signature(request_body)

        assert client.validate_signature(request_body, signature)

    def test_invalid_signature(self):
        client = LineBotClient(TestValidation.CHANNEL_ID, TestValidation.CHANNEL_SECRET, TestValidation.CHANNEL_MID)

        request_body = "{}"
        signature = self._compute_signature(request_body)

        altered_request_body = "{altered}"

        assert not client.validate_signature(altered_request_body, signature)

    def _compute_signature(self, request_body):
        mac = hmac.new(TestValidation.CHANNEL_SECRET.encode(), request_body.encode(), hashlib.sha256)
        return mac.digest()