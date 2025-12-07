import asyncio
import logging
from abc import ABC, abstractmethod
from asyncio import Queue
from dataclasses import dataclass, field
from idlelib.window import add_windows_to_menu
from typing import Optional, override, List, Tuple, Dict, Callable, Any, AsyncGenerator, Awaitable

from busline.client.eventbus_connector import EventBusConnector
from busline.client.subscriber.event_handler import CallbackEventHandler, event_handler
from busline.client.subscriber.event_handler.event_handler import EventHandler
from busline.event.event import Event
from busline.exceptions import EventHandlerNotFound


class SubscribeMixin(ABC):
    """
    Mixin which provides base methods to subscribe and unsubscribe

    Author: Nicola Ricciardi
    """

    @abstractmethod
    async def subscribe(self, topic: str, **kwargs):
        raise NotImplemented()

    async def multi_subscribe(self, topics: List[str], /, parallelize: bool = True, **kwargs):
        logging.debug("%s: subscribe to %d topics (parallelization: %s)", self, len(topics), parallelize)

        if parallelize:
            tasks = [self.subscribe(topic, **kwargs) for topic in topics]
            await asyncio.gather(*tasks)

        else:
            for topic in topics:
                await self.subscribe(topic, **kwargs)

    @abstractmethod
    async def unsubscribe(self, topic: Optional[str] = None, **kwargs):
        raise NotImplemented()

    async def multi_unsubscribe(self, topics: List[str], /, parallelize: bool = True, **kwargs):
        logging.debug("%s: unsubscribe from %d topics (parallelization: %s)", self, len(topics), parallelize)

        if parallelize:
            tasks = [self.unsubscribe(topic, **kwargs) for topic in topics]
            await asyncio.gather(*tasks)

        else:
            for topic in topics:
                await self.unsubscribe(topic, **kwargs)


def _default_topic_matcher(t1: str, t2: str) -> bool:
    return t1 == t2


@dataclass(kw_only=True, eq=False)
class Subscriber(EventBusConnector, SubscribeMixin, ABC):
    """
    Handles different topic events using ad hoc handlers defined by user,
    else it uses fallback handler if provided (otherwise throws an exception)

    Attributes:
        default_handler: event handler used for a topic if no event handler is specified for that topic
        topic_names_matcher: function used to check match between two topic name (with wildcards); default "t1 == t2"
        handler_always_required: raise an exception if no handlers are found for a topic

    Author: Nicola Ricciardi
    """

    default_handler: Optional[EventHandler] = field(default=None)
    topic_names_matcher: Callable[[str, str], bool] = field(repr=False, default=_default_topic_matcher)
    handler_always_required: bool = field(default=False)
    _handlers: Dict[str, EventHandler] = field(default_factory=dict, init=False)
    _inbound_events_queue: Queue[Tuple[str, Event]] = field(default_factory=Queue, init=False)
    _inbound_not_handled_events_queue: Queue[Tuple[str, Event]] = field(default_factory=Queue, init=False)
    _stop_queue_processing: asyncio.Event = field(default_factory=asyncio.Event, init=False)

    @override
    async def connect(self):
        await super().connect()
        self._stop_queue_processing.clear()

    @override
    async def disconnect(self):
        await super().disconnect()
        self._stop_queue_processing.set()

    @abstractmethod
    async def _internal_subscribe(self, topic: str, handler: Optional[EventHandler] = None, **kwargs):
        """
        Actual subscribe to topic
        """

    @abstractmethod
    async def _internal_unsubscribe(self, topic: Optional[str] = None, **kwargs):
        """
        Actual unsubscribe to topic
        """

    @override
    async def subscribe(self, topic: str, handler: Optional[EventHandler | Callable[[str, Event], Awaitable]] = None, **kwargs):
        """
        Subscribe to topic using handler. If handler is an async callback, then it is wrapped using CallbackEventHandler.
        Otherwise, if it is None, then default handler will be used (if it will be set).
        """

        if handler is not None:
            if not issubclass(type(handler), EventHandler):
                handler = event_handler(handler)

        logging.info("%s: subscribe on topic %s", self, topic)
        await self._on_subscribing(topic, handler, **kwargs)
        await self._internal_subscribe(topic, handler, **kwargs)
        await self._on_subscribed(topic, handler, **kwargs)

    @override
    async def unsubscribe(self, topic: Optional[str] = None, **kwargs):
        """
        Unsubscribe to topic
        """

        logging.info("%s: unsubscribe from topic %s", self, topic)
        await self._on_unsubscribing(topic, **kwargs)
        await self._internal_unsubscribe(topic, **kwargs)
        await self._on_unsubscribed(topic, **kwargs)

    async def _on_subscribing(self, topic: str, handler: Optional[EventHandler] = None, **kwargs):
        """
        Callback called on subscribing
        """

    async def _on_subscribed(self, topic: str, handler: Optional[EventHandler] = None, **kwargs):
        """
        Callback called on subscribed
        """

        self._handlers[topic] = handler

    async def _on_unsubscribing(self, topic: Optional[str], **kwargs):
        """
        Callback called on unsubscribing
        """

    async def _on_unsubscribed(self, topic: Optional[str], **kwargs):
        """
        Callback called on unsubscribed
        """

        if topic is None:
            self._handlers = {}
        else:
            if topic in self._handlers:
                del self._handlers[topic]
            else:
                logging.warning("%s: unsubscribed from unknown topic: %s", self, topic)

    def __get_handlers_of_topic(self, topic: str) -> List[EventHandler]:

        handlers = []
        for t, h in self._handlers.items():
            if not self.topic_names_matcher(topic, t):
                continue

            if h is not None:
                handlers.append(h)
                continue

            if self.default_handler is not None:
                handlers.append(self.default_handler)
                continue

            if self.handler_always_required:
                raise EventHandlerNotFound()
            else:
                logging.warning("%s: event handler for topic '%s' not found", self, topic)

        return handlers


    async def notify(self, topic: str, event: Event, **kwargs):
        """
        Notify subscriber
        """

        handlers_of_topic: List[EventHandler] = self.__get_handlers_of_topic(topic)

        tasks = []

        try:
            self._inbound_events_queue.put_nowait((topic, event))
        except asyncio.QueueFull:
            tasks.append(
                self._inbound_events_queue.put((topic, event))
            )

        if len(handlers_of_topic) > 0:
            for handler in handlers_of_topic:
                tasks.append(
                    handler.handle(topic, event)
                )
        else:
            try:
                self._inbound_not_handled_events_queue.put_nowait((topic, event))
            except asyncio.QueueFull:
                tasks.append(
                    self._inbound_not_handled_events_queue.put((topic, event))
                )

        return asyncio.gather(*tasks)

    @property
    async def inbound_events(self) -> AsyncGenerator[tuple[str, Event], None]:
        """
        Generator which provides all inbound events
        """

        while not self._stop_queue_processing.is_set():
            topic, event = await self._inbound_events_queue.get()
            yield topic, event

    @property
    async def inbound_unhandled_events(self) -> AsyncGenerator[tuple[str, Event], None]:
        """
        Generator which provides only inbound events which are not handled
        """

        while not self._stop_queue_processing.is_set():
            topic, event = await self._inbound_not_handled_events_queue.get()
            yield topic, event


    def __str__(self) -> str:
        return f"Subscriber('{self.identifier}')"