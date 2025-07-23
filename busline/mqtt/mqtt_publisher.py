import logging
from typing import override, Callable
from busline.client.publisher.publisher import Publisher
from busline.event.event import Event, RegistryPassthroughEvent, registry_passthrough_event_json_serializer
from dataclasses import dataclass, field

from busline.mqtt import _MqttClientWrapper


@dataclass(kw_only=True)
class MqttPublisher(Publisher, _MqttClientWrapper):
    """
    Publisher which works with MQTT

    Author: Nicola Ricciardi
    """

    serializer: Callable[[RegistryPassthroughEvent], bytes] = field(default_factory=lambda: registry_passthrough_event_json_serializer)


    @override
    async def _internal_publish(self, topic_name: str, event: Event, **kwargs):
        await self._internal_client.publish(
            topic=topic_name,
            payload=self.serializer(RegistryPassthroughEvent.from_event(event)),
            **kwargs
        )
