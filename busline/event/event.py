from __future__ import annotations

import base64
import json
import uuid
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, Generic, TypeVar, Dict, Self
from abc import ABC

from dataclasses_avroschema import AvroModel

from busline.utils.serde import SerdableMixin
from busline.event.registry import EventRegistry


_registry = EventRegistry()



M = TypeVar('M', bound='Message')



@dataclass(kw_only=True)
class Event(Generic[M]):
    """
    Python-level inbound event

    Author: Nicola Ricciardi
    """

    publisher_identifier: str
    payload: Optional[M]
    identifier: str
    timestamp: datetime


@dataclass(kw_only=True)
class RegistryPassthroughEvent(AvroModel):
    """
    Utility class to manage event serialization. It works with EventRegistry to manage deserialization.

    Author: Nicola Ricciardi
    """

    identifier: str
    publisher_identifier: str
    serialized_payload: Optional[bytes]
    payload_format_type: Optional[str]
    message_type: Optional[str]
    timestamp: datetime


    @classmethod
    def from_event(cls, event: Event[M], *, message_type: Optional[str] = None) -> Self:
        """
        Automatically add event message to registry
        """

        if message_type is None and event.payload is not None:
            message_type = _registry.add(type(event.payload), message_type=message_type)

        payload_format_type, serialized_payload = event.payload.serialize() if event.payload is not None else (None, None)

        return cls(
            publisher_identifier=event.publisher_identifier,
            timestamp=event.timestamp,
            identifier=event.identifier,
            message_type=message_type,
            serialized_payload=serialized_payload,
            payload_format_type=payload_format_type
        )

    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        return cls(
            identifier=data["identifier"],
            publisher_identifier=data["publisher_identifier"],
            serialized_payload=data["serialized_payload"],
            message_type=data["message_type"],
            timestamp=data["timestamp"],
            payload_format_type=data["payload_format_type"]
        )

    def to_event(self) -> Event:
        """
        Retrieve from registry right message class, then construct the event
        """

        payload = None
        if self.serialized_payload is not None:
            if self.message_type is None:
                raise ValueError("Message type missed")

            class_of_message = _registry.retrieve_class(self.message_type)
            payload = class_of_message.deserialize(self.payload_format_type, self.serialized_payload)

        return Event(
            identifier=self.identifier,
            publisher_identifier=self.publisher_identifier,
            timestamp=self.timestamp,
            payload=payload
        )

    def to_dict(self) -> Dict:
        return {
            "identifier": self.identifier,
            "publisher_identifier": self.publisher_identifier,
            "serialized_payload": self.serialized_payload,
            "payload_format_type": self.payload_format_type,
            "message_type": self.message_type,
            "timestamp": self.timestamp
        }


def _custom_encoder(obj):
    if isinstance(obj, datetime):
        return {"__type__": "datetime", "value": obj.isoformat()}
    if isinstance(obj, bytes):
        return {"__type__": "bytes", "value": base64.b64encode(obj).decode("utf-8")}

    return str(obj)


def registry_passthrough_event_json_serializer(event: RegistryPassthroughEvent) -> bytes:
    return json.dumps(event.to_dict(), default=_custom_encoder).encode("utf-8")


def _custom_decoder(obj):
    if "__type__" in obj:
        if obj["__type__"] == "datetime":
            return datetime.fromisoformat(obj["value"])
        if obj["__type__"] == "bytes":
            return base64.b64decode(obj["value"])
    return obj

def registry_passthrough_event_json_deserializer(serialized_event: bytes) -> RegistryPassthroughEvent:
    return RegistryPassthroughEvent.from_dict(json.loads(serialized_event.decode("utf-8"), object_hook=_custom_decoder))



