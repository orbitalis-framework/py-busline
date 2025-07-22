from __future__ import annotations

import uuid
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional, Generic, TypeVar, Dict, Self
from abc import ABC
from busline.utils.serde import SerdableMixin
from busline.event.registry import EventRegistry


_registry = EventRegistry()



M = TypeVar('M', bound='Message')

@dataclass(kw_only=True)
class RegistryBasedEvent:
    identifier: str
    publisher_identifier: str
    serialized_payload: Optional[bytes]
    payload_format_type: Optional[str]
    message_type: Optional[str]
    timestamp: datetime


    @classmethod
    def from_event(cls, event: Event[M], message_type: Optional[str] = None, *, add_to_registry: bool = True) -> Self:
        if message_type is None and event.payload is not None:

            class_type = type(event.payload)
            message_type = class_type.__name__

            if add_to_registry:
                _registry.add(message_type, class_type)

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
        payload = None
        if self.serialized_payload is not None:
            if self.message_type is None:
                raise ValueError("Message type missed")

            payload = _registry.retrieve_class(self.message_type).deserialize(self.payload_format_type, self.serialized_payload)

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


@dataclass(kw_only=True)
class Event(Generic[M]):
    """
    TODO

    Author: Nicola Ricciardi
    """

    publisher_identifier: str
    payload: Optional[M]
    identifier: str
    timestamp: datetime


