from abc import ABC
from typing import Dict, List, Callable

from busline.client.subscriber.listener.closure_event_handler import ClosureEventHandler
from busline.client.subscriber.listener.event_handler import EventHandler
from busline.client.subscriber.subscriber import Subscriber
from busline.event.event import Event


class MultiHandlersSubscriber(Subscriber, ABC):

    def __init__(self, subscriber_id: str | None = None, default_event_handler: EventHandler | Callable[[str, Event], None] | None = None):
        Subscriber.__init__(self, subscriber_id)

        if default_event_handler is not None and not isinstance(default_event_handler, EventHandler):
            default_event_handler = ClosureEventHandler(on_event_callback=default_event_handler)

        self._default_event_handler = default_event_handler

        self.__handlers: Dict[str, List[EventHandler]] = {}

    @property
    def default_event_handler(self) -> EventHandler | None:
        return self._default_event_handler

    @default_event_handler.setter
    def default_event_handler(self, handler: EventHandler | Callable[[str, Event], None] | None):
        self._default_event_handler = handler

    async def subscribe(self, topic: str, handlers: EventHandler | Callable[[str, Event], None] | List[EventHandler] | None = None, **kwargs):
        await super().subscribe(topic, handlers=handlers, **kwargs)

    async def _on_subscribed(self, topic: str, handlers: EventHandler | Callable[[str, Event], None] | List[EventHandler] | None = None, **kwargs):
        await super()._on_subscribed(topic, **kwargs)

        self.__set_handlers(topic, handlers)

    def __set_handlers(self, topic: str, event_handlers: EventHandler | Callable[[str, Event], None] | List[EventHandler] | None = None):
        handlers: List[EventHandler] = []

        if event_handlers is not None:
            try:
                for handler in event_handlers:
                    if isinstance(handler, EventHandler):
                        handlers.append(handler)
                    else:
                        handlers.append(ClosureEventHandler(on_event_callback=handler))

            except TypeError:

                handler = event_handlers

                if isinstance(handler, EventHandler):
                    handlers.append(handler)
                else:
                    handlers.append(ClosureEventHandler(on_event_callback=handler))

        self.__handlers[topic] = handlers       # TODO: wildcard support

    async def _on_unsubscribing(self, topic: str | None, **kwargs):
        await super()._on_unsubscribing(topic, **kwargs)

        if topic is None:
            self.__handlers = {}
        else:
            del self.__handlers[topic]

    async def on_event(self, topic: str, event: Event):

        if self._default_event_handler is not None:
            await self._default_event_handler.on_event(topic, event)

        for handler in self.__handlers.get(topic, []):
            await handler.on_event(topic, event)