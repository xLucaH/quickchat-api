from typing import Dict, List, Union

from .event_types import EventType


class EventHandler:

    def __init__(self):

        self.events: Dict[EventType, List] = {}

    def register_event(self, event: Union[EventType, List[EventType]], function: Union[callable, List[callable]]):
        event_types = []

        if isinstance(event, list):
            event_types.extend(event)
        else:
            event_types.append(event)

        if callable(function):
            for e in event_types:
                self._register_event(e, function)
            return

        if isinstance(function, list):
            for fn in function:
                self._register_event(event, fn)

    def _register_event(self, event: EventType, function: callable):
        handlers = self.events.get(event, None)

        if handlers is None:
            self.events[event] = [function, ]
        else:
            self.events[event].append(function)

    async def dispatch(self, event: EventType, data):
        handlers: List[callable] = self.events.get(event, None)

        if handlers is None:
            raise ValueError(f'Unknown event of type "{event}"')

        for func in handlers:
            await func(data)
