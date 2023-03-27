from typing import Dict, List, Union

from .event_types import EventType


class EventHandler:

    def __init__(self):

        self.events: Dict[EventType, List] = {}

    def register_event(self, event: Union[EventType, List[EventType]], function: callable):

        if isinstance(event, EventType):
            self._register_event(event, function)
            return

        if isinstance(event, list):
            for e in event:
                self._register_event(e, function)

    def _register_event(self, event: EventType, function: callable):
        handlers = self.events.get(event, None)

        if handlers is None:
            self.events[event] = [function, ]
        else:
            self.events[event].append(function)

    def dispatch(self, event: EventType, data):
        handlers = self.events.get(event, None)

        if handlers is None:
            raise ValueError(f'Unknown event of type "{event}"')

        for func in handlers:
            func(data)
