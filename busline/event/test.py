import json
import unittest
from typing import Type, Self, Tuple, override
from dataclasses import dataclass

from busline.event.avro_payload import AvroEventPayload
from busline.event.event import Event, EventPayload
from busline.event.json_payload import JsonEventPayload
from busline.event.registry import EventRegistry, registry


@dataclass(frozen=True)
class EventPayload1(EventPayload):

    value: int

    def my_value1(self) -> int:
        return self.value

    def serialize(self) -> Tuple[str, bytes]:
        return "raw", self.value.to_bytes(1)

    @classmethod
    def deserialize(cls, payload_type: str, payload: bytes) -> Self:
        return EventPayload1(int.from_bytes(payload))

@dataclass(frozen=True)
@registry
class EventPayload2(EventPayload):

    value: int

    def my_value2(self) -> int:
        return self.value

    def serialize(self) -> Tuple[str, bytes]:
        return "raw", self.value.to_bytes(1)

    @classmethod
    def deserialize(cls, payload_type: str, payload: bytes) -> Self:
        return EventPayload2(int.from_bytes(payload))

@dataclass(frozen=True)
class MockUserCreationJsonPayload(JsonEventPayload):

    email: str
    password: str

    @classmethod
    @override
    def from_json(cls, json_str: str) -> Self:
        data = json.loads(json_str)

        return MockUserCreationJsonPayload(data["email"], data["password"])


@dataclass(frozen=True)
class MockUserCreationAvroPayload(AvroEventPayload):
    email: str
    password: str


class TestEventRegistry(unittest.TestCase):

    def test_raw_payload(self):
        event = Event(payload=EventPayload1(1))

        _, serialized_payload = event.payload.serialize()
        self.assertIs(type(serialized_payload), bytes)


    def test_json_payload(self):
        event = Event(payload=MockUserCreationJsonPayload("email", "password"))

        format_type, serialized_payload = event.payload.serialize()

        self.assertIs(type(serialized_payload), bytes)
        self.assertEqual(format_type, "application/json")

        payload: MockUserCreationJsonPayload = MockUserCreationJsonPayload.deserialize(format_type, serialized_payload)

        self.assertEqual(payload.email, event.payload.email)
        self.assertEqual(payload.password, event.payload.password)

    def test_registry(self):

        event_registry = EventRegistry()    # singleton

        event_registry.add("event_payload1", EventPayload1)

        self.assertEqual(len(event_registry.associations), 2)

        event_registry = EventRegistry()  # singleton

        generic_event1 = Event(payload=EventPayload1(1), event_type="event_payload1")
        generic_unknown_event = Event(payload=None, event_type="unknown")

        self.assertNotEqual(generic_event1.identifier, generic_unknown_event.identifier)

        format_type, serialized_payload = generic_event1.payload.serialize()
        event_payload1: EventPayload1 = event_registry.build(generic_event1.event_type, format_type, serialized_payload)

        self.assertEqual(event_payload1.value, 1)
        self.assertEqual(event_payload1.my_value1(), 1)

        self.assertRaises(KeyError, lambda: event_registry.retrieve_class(generic_unknown_event.event_type))

    def test_avro_payload(self):

        payload = MockUserCreationAvroPayload("email", "password")

        format_type, serialized_payload = payload.serialize()

        deserialized_payload = MockUserCreationAvroPayload.deserialize(format_type, serialized_payload)

        self.assertEqual(payload.email, deserialized_payload.email)
        self.assertEqual(payload.password, deserialized_payload.password)