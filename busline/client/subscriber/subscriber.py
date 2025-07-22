import asyncio
import logging
from abc import ABC, abstractmethod
from asyncio import Queue
from dataclasses import dataclass, field
from idlelib.window import add_windows_to_menu
from typing import Optional, override, List, Tuple, Dict, Callable, Any, AsyncGenerator, Awaitable

from busline.client.eventbus_connector import EventBusConnector
from busline.client.subscriber.event_handler import CallbackEventHandler
from busline.client.subscriber.event_handler.event_handler import EventHandler
from busline.event.event import Event
from busline.exceptions import EventHandlerNotFound


class SubscribeMixin(ABC):
    @abstractmethod
    async def subscribe(self, topic: str, **kwargs):
        raise NotImplemented()

    async def multi_subscribe(self, topics: List[str], /, parallelize: bool = True, **kwargs):
        logging.debug(f"{self}: subscribe to {len(topics)} topics (parallelization: {parallelize})")

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
        logging.debug(f"{self}: unsubscribe from {len(topics)} topics (parallelization: {parallelize})")

        if parallelize:
            tasks = [self.unsubscribe(topic, **kwargs) for topic in topics]
            await asyncio.gather(*tasks)

        else:
            for topic in topics:
                await self.unsubscribe(topic, **kwargs)



@dataclass(eq=False)
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
    topic_names_matcher: Callable[[str, str], bool] = field(repr=False, default=lambda t1, t2: t1 == t2)
    handler_always_required: bool = field(default=False)
    _handlers: Dict[str, EventHandler] = field(default_factory=dict, init=False)
    _inbound_events_queue: Queue[Tuple[str, Event]] = field(default_factory=lambda: Queue(maxsize=0), init=False)
    _inbound_not_handled_events_queue: Queue[Tuple[str, Event]] = field(default_factory=lambda: Queue(maxsize=0), init=False)
    _stop_queue_processing: asyncio.Event = field(default_factory=lambda: asyncio.Event(), init=False)

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
                handler = CallbackEventHandler(handler)

        logging.info(f"{self}: subscribe on topic {topic}")
        await self._on_subscribing(topic, handler, **kwargs)
        await self._internal_subscribe(topic, handler, **kwargs)
        await self._on_subscribed(topic, handler, **kwargs)

    @override
    async def unsubscribe(self, topic: Optional[str] = None, **kwargs):
        """
        Unsubscribe to topic
        """

        logging.info(f"{self}: unsubscribe from topic {topic}")
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
                logging.warning(f"{self}: unsubscribed from unknown topic: {topic}")

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
                logging.warning(f"{self}: event handler for topic '{topic}' not found")

        return handlers


    async def notify(self, topic: str, event: Event, **kwargs):
        """
        Notify subscriber
        """

        handlers_of_topic: List[EventHandler] = self.__get_handlers_of_topic(topic)

        tasks = [
            self._inbound_events_queue.put((topic, event))
        ]

        if len(handlers_of_topic) > 0:
            tasks.extend([handler.handle(topic, event) for handler in handlers_of_topic])
        else:
            tasks.append(self._inbound_not_handled_events_queue.put((topic, event)))

        await asyncio.gather(
            *tasks
        )


    @property
    async def inbound_events(self) -> AsyncGenerator[tuple[str, Event], None]:
        while not self._stop_queue_processing.is_set():
            topic, event = await self._inbound_events_queue.get()
            yield topic, event

    @property
    async def inbound_unhandled_events(self) -> AsyncGenerator[tuple[str, Event], None]:
        while not self._stop_queue_processing.is_set():
            topic, event = await self._inbound_not_handled_events_queue.get()
            yield topic, event


    def __str__(self) -> str:
        return f"Subscriber('{self.identifier}')"