import asyncio
import json
import logging
from dataclasses import dataclass, field
from typing import Optional, override, Callable, List, Awaitable

from busline.client.subscriber.subscriber import Subscriber
from busline.client.subscriber.event_handler.event_handler import EventHandler
from busline.event.event import RegistryBasedEvent, Event
from busline.mqtt import _MqttClientWrapper


def json_deserializer(serialized_event: bytes) -> RegistryBasedEvent:
    return RegistryBasedEvent.from_dict(json.loads(serialized_event.decode("utf-8")))


@dataclass(kw_only=True)
class MqttSubscriber(Subscriber, _MqttClientWrapper):
    """
    Subscriber topic-based which works with MQTT

    Author: Nicola Ricciardi
    """


    deserializer: Callable[[bytes], RegistryBasedEvent] = field(default_factory=lambda: json_deserializer)
    _handle_messages_task: asyncio.Task = field(default=None, init=False)

    @override
    async def connect(self):
        await super().connect()
        self._handle_messages_task = asyncio.create_task(
            self._messages_handler()
        )

    async def _messages_handler(self):
        try:
            async for message in self._internal_client.messages:
                await self.notify(
                    str(message.topic),
                    self.deserializer(message.payload).to_event()
                )
        except Exception as e:
            logging.error(f"{self}: messages handler error: {repr(e)}")


    @override
    async def _internal_subscribe(self, topic: str, handler: Optional[EventHandler | Callable[[str, Event], Awaitable]] = None, **kwargs):
        await self._internal_client.subscribe(topic)


    @override
    async def _internal_unsubscribe(self, topic: Optional[str] = None, **kwargs):
        await self._internal_client.unsubscribe(topic)