import asyncio
import logging
from abc import ABC
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass, field
from busline.client.subscriber.event_handler.event_handler import EventHandler
from busline.client.subscriber.subscriber import Subscriber
from busline.event.event import Event
from busline.exceptions import EventHandlerNotFound


@dataclass(kw_only=True)
class MultiHandlersSubscriber(Subscriber, ABC):
    """
    Handles different topic events using ad hoc handlers defined by user,
    else it uses fallback handler if provided (otherwise throws an exception)

    Attributes:
        fallback_event_handler: event handler used for a topic if no event handler is specified for that topic
        handlers: event handler for each topic (i.e. key); notice that key can also be a string with wildcards
        topic_names_matcher: function used to check match between two topic name (with wildcards); default "t1 == t2"
        event_handler_always_required: raise an exception if no handlers are found for a topic

    Author: Nicola Ricciardi
    """

    fallback_event_handler: Optional[EventHandler] = field(default=None)
    handlers: Dict[str, EventHandler] = field(default_factory=dict)
    topic_names_matcher: Callable[[str, str], bool] = field(repr=False, default=lambda t1, t2: t1 == t2)
    event_handler_always_required: bool = field(default=False)

    async def subscribe(self, topic: str, handler: Optional[EventHandler] = None, **kwargs):
        await super().subscribe(topic, handler=handler, **kwargs)

    async def _on_subscribing(self, topic: str, handler: Optional[EventHandler] = None, **kwargs):
        await super()._on_subscribing(topic, **kwargs)

        if self.fallback_event_handler is None:
            if self.event_handler_always_required:
                raise EventHandlerNotFound()
            else:
                logging.warning(f"event handler for topic '{topic}' not found in subscriber {self.identifier}")

    async def _on_subscribed(self, topic: str, handler: Optional[EventHandler] = None, **kwargs):
        await super()._on_subscribed(topic, **kwargs)
        self.handlers[topic] = handler

    async def _on_unsubscribed(self, topic: str | None, **kwargs):
        await super()._on_subscribed(topic, **kwargs)

        if topic is None:
            self.handlers = {}
        else:
            del self.handlers[topic]

    def _get_handlers_of_topic(self, topic: str) -> List[EventHandler]:

        handlers = []
        for t, h in self.handlers.items():
            if self.topic_names_matcher(topic, t):
                if h is not None:
                    handlers.append(h)
                else:
                    if self.fallback_event_handler is not None:
                        handlers.append(self.fallback_event_handler)
                    else:
                        if self.event_handler_always_required:
                            raise EventHandlerNotFound()
                        else:
                            logging.warning(f"event handler for topic '{topic}' not found in subscriber {self.identifier}")

        return handlers

    async def on_event(self, topic: str, event: Event):

        handlers_of_topic: List[EventHandler] = self._get_handlers_of_topic(topic)

        if len(handlers_of_topic) > 0:
            tasks = [handler.handle(topic, event) for handler in handlers_of_topic]
            await asyncio.gather(*tasks)
