import asyncio
import json
import logging
from dataclasses import dataclass, field
from typing import Optional, override, Callable, List, Awaitable, Set

from busline.client.subscriber.subscriber import Subscriber
from busline.client.subscriber.event_handler.event_handler import EventHandler
from busline.event.event import RegistryPassthroughEvent, Event, registry_passthrough_event_json_deserializer
from busline.mqtt import _MqttClientWrapper





@dataclass(kw_only=True)
class MqttSubscriber(Subscriber, _MqttClientWrapper):
    """
    Subscriber topic-based which works with MQTT

    Author: Nicola Ricciardi
    """


    deserializer: Callable[[bytes], RegistryPassthroughEvent] = field(default_factory=lambda: registry_passthrough_event_json_deserializer)
    _handle_messages_task: asyncio.Task = field(default=None, init=False)

    __subscribed_topics: Set[str] = field(default_factory=set, init=False)

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
            logging.error("%s: messages handler error: %s", self, repr(e))


    @override
    async def _internal_subscribe(self, topic: str, handler: Optional[EventHandler | Callable[[str, Event], Awaitable]] = None, **kwargs):
        await self._internal_client.subscribe(topic)
        self.__subscribed_topics.add(topic)


    @override
    async def _internal_unsubscribe(self, topic: Optional[str] = None, **kwargs):

        if topic is not None:
            await self._internal_client.unsubscribe(topic)
            self.__subscribed_topics.remove(topic)
        else:
            tasks = [
                    self._internal_client.unsubscribe(t)
                    for t in self.__subscribed_topics
                ]

            self.__subscribed_topics.clear()

            await asyncio.gather(*tasks)
