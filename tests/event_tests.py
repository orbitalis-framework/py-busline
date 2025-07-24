from datetime import datetime
import json
import unittest
from typing import Self, Tuple, override
from dataclasses import dataclass, asdict

from busline.event.message.avro_message import AvroMessageMixin, AVRO_FORMAT_TYPE
from busline.event.event import Event, RegistryPassthroughEvent, registry_passthrough_event_json_serializer, registry_passthrough_event_json_deserializer
from busline.event.message.json_message import JsonMessageMixin, JSON_FORMAT_TYPE
from busline.event.message.message import Message
from busline.event.message.number_message import Int64Message, Float32Message
from busline.event.message.string_message import StringMessage
from busline.event.registry import EventRegistry, add_to_registry


@dataclass(frozen=True)
class CustomSerdableMessage1(Message):

    value: int

    def my_value1(self) -> int:
        return self.value

    def serialize(self) -> Tuple[str, bytes]:
        return "raw", self.value.to_bytes(1)

    @classmethod
    def deserialize(cls, payload_type: str, payload: bytes) -> Self:
        return cls(int.from_bytes(payload))

@dataclass(frozen=True)
@add_to_registry
class CustomSerdableMessage2(Message):

    value: int

    def my_value2(self) -> int:
        return self.value

    def serialize(self) -> Tuple[str, bytes]:
        return "raw", self.value.to_bytes(1)

    @classmethod
    def deserialize(cls, payload_type: str, payload: bytes) -> Self:
        return cls(int.from_bytes(payload))

@dataclass(frozen=True)
class MockUserCreationMessage(JsonMessageMixin):


    email: str
    password: str

    @classmethod
    @override
    def from_json(cls, json_str: str) -> Self:
        data = json.loads(json_str)

        return cls(data["email"], data["password"])

    @override
    def to_json(self) -> str:
        return json.dumps(asdict(self))


@dataclass(frozen=True)
class MockUserCreationAvroPayload(AvroMessageMixin):
    email: str
    password: str


class TestEventRegistry(unittest.TestCase):

    def test_raw_payload(self):
        message = CustomSerdableMessage1(1)

        _, serialized_payload = message.serialize()
        self.assertIs(type(serialized_payload), bytes)


    def test_json_payload(self):
        message = MockUserCreationMessage("email", "password")

        format_type, serialized_payload = message.serialize()

        self.assertIs(type(serialized_payload), bytes)
        self.assertEqual(format_type, JSON_FORMAT_TYPE)

        message_rec: MockUserCreationMessage = MockUserCreationMessage.deserialize(format_type, serialized_payload)

        self.assertEqual(message_rec.email, message.email)
        self.assertEqual(message_rec.password, message.password)

    def test_avro_payload(self):

        message = MockUserCreationAvroPayload("email", "password")

        format_type, serialized_payload = message.serialize()

        self.assertIs(type(serialized_payload), bytes)
        self.assertEqual(format_type, AVRO_FORMAT_TYPE)

        deserialized_message = MockUserCreationAvroPayload.deserialize(format_type, serialized_payload)

        self.assertEqual(message.email, deserialized_message.email)
        self.assertEqual(message.password, deserialized_message.password)

    def test_registry(self):

        event_registry = EventRegistry()    # singleton

        message_type = event_registry.add(CustomSerdableMessage1)

        self.assertEqual(len(event_registry.associations), 2)   # @add_to_registry used

        event_registry = EventRegistry()  # singleton

        message = CustomSerdableMessage1(1)

        format_type, serialized_message = message.serialize()

        class_of_message = event_registry.retrieve_class(message_type)

        message_rec = class_of_message.deserialize(format_type, serialized_message)

        self.assertEqual(message_rec, message)

    def test_registry_based_event(self):
        message = StringMessage("my message")

        event = Event(
            identifier="event-id",
            payload=message,
            publisher_identifier="pub-id",
            timestamp=datetime.now()
        )

        registry_based_event = RegistryPassthroughEvent.from_event(event)   # auto-add message in EventRegistry

        self.assertIsNotNone(registry_based_event.message_type)
        self.assertIsNotNone(registry_based_event.payload_format_type)
        self.assertIsNotNone(registry_based_event.serialized_payload)

        self.assertIn(EventRegistry.obj_to_type(message), EventRegistry().associations)     # EventRegistry is singleton

        # serialization (e.g. JSON)
        registry_based_event_ser = registry_passthrough_event_json_serializer(registry_based_event)

        # deserialization
        registry_based_event_des = registry_passthrough_event_json_deserializer(registry_based_event_ser)

        event_rec = registry_based_event_des.to_event()

        self.assertEqual(event_rec.identifier, event.identifier)
        self.assertEqual(event_rec.payload, event.payload)
        self.assertEqual(event_rec.publisher_identifier, event.publisher_identifier)
        self.assertEqual(event_rec.timestamp, event.timestamp)

    def test_serde_multi_format_type(self):
        int64_message = Int64Message(42)

        format_type, serialized_data = int64_message.serialize(format_type=AVRO_FORMAT_TYPE)

        self.assertEqual(format_type, AVRO_FORMAT_TYPE)

        self.assertEqual(Int64Message.deserialize(format_type, serialized_data), int64_message)

        format_type, serialized_data = int64_message.serialize(format_type=JSON_FORMAT_TYPE)

        self.assertEqual(format_type, JSON_FORMAT_TYPE)

        self.assertEqual(Int64Message.deserialize(format_type, serialized_data), int64_message)

        float32_message = Float32Message(3.14)

        format_type, serialized_data = float32_message.serialize(format_type=AVRO_FORMAT_TYPE)

        self.assertEqual(format_type, AVRO_FORMAT_TYPE)

        self.assertEqual(Float32Message.deserialize(format_type, serialized_data), float32_message)












