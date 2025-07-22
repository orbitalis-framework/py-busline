import logging
from typing import override, Callable
from aiomqtt import Client
from busline.client.publisher.publisher import Publisher
from busline.event.event import Event, RegistryBasedEvent
from dataclasses import dataclass, field, asdict
import json

from busline.mqtt import _MqttClientWrapper


def json_serializer(event: RegistryBasedEvent) -> bytes:
    return json.dumps(event.to_dict(), default=str).encode("utf-8")


@dataclass(kw_only=True)
class MqttPublisher(Publisher, _MqttClientWrapper):
    """
    Publisher which works with MQTT

    Author: Nicola Ricciardi
    """

    serializer: Callable[[RegistryBasedEvent], bytes] = field(default_factory=lambda: json_serializer)


    @override
    async def _internal_publish(self, topic_name: str, event: Event, **kwargs):
        await self._internal_client.publish(
            topic=topic_name,
            payload=self.serializer(RegistryBasedEvent.from_event(event)),
            **kwargs
        )
