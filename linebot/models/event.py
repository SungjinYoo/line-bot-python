import json
from abc import ABCMeta, abstractmethod

from linebot.models.content import ContentMapper
from linebot.models.operation import OperationMapper


class NoEventMappingException(Exception):
    """
    no handler to handle event with event type
    """


class EventType:
    RECEIVING_MESSAGE = "138311609000106303"
    RECEIVING_OPERATION = "138311609100106403"
    SENDING_MESSAGE = "138311608800106203"
    SENDING_MULTIPLE_MESSAGES = "140177271400161403"


class Event(metaclass=ABCMeta):
    def __init__(self, event, content):
        self.from_channel = event['fromChannel']
        self.to = event['to']
        self.eventType = event['eventType']
        self.id_ = event['id']
        self.content = content


class MessageEvent(Event):
    def __init__(self, event):
        super().__init__(event, ContentMapper.map(event['content']))


class OperationEvent(Event):
    def __init__(self, event):
        super().__init__(event, OperationMapper.map(event['content']))


class EventParser:
    @classmethod
    def parse(cls, event_json):
        event = json.loads(event_json)
        event_type = event['eventType']
        if event_type == EventType.RECEIVING_MESSAGE:
            return MessageEvent(event)
        elif event_type == EventType.RECEIVING_OPERATION:
            return OperationEvent(event)
        else:
            raise NoEventMappingException()
