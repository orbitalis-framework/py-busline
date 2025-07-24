import json
from dataclasses import dataclass, field
from typing import Self, Tuple, Literal, Optional
import struct

from busline.event.message.avro_message import AVRO_FORMAT_TYPE, AvroMessageMixin
from busline.event.message.json_message import JSON_FORMAT_TYPE, JsonMessageMixin
from busline.event.message.message import Message, BYTES_FORMAT_TYPE
from busline.utils.serde import SerdableMixin




@dataclass(frozen=True)
class Int64Message(AvroMessageMixin, JsonMessageMixin, SerdableMixin):
    """
    Wrap `int` and serialize into 8 bytes integer number

    Author: Nicola Ricciardi
    """

    value: int

    def serialize(self, *, format_type: Optional[str] = None) -> Tuple[str, bytes]:
        if format_type == BYTES_FORMAT_TYPE:
            return BYTES_FORMAT_TYPE, self.value.to_bytes(length=8, signed=True, byteorder="big")

        if format_type == AVRO_FORMAT_TYPE:
            return AvroMessageMixin.serialize(self)

        if format_type == JSON_FORMAT_TYPE:
            return JsonMessageMixin.serialize(self)

        raise ValueError("Not supported format type")

    @classmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        if format_type == BYTES_FORMAT_TYPE:
            return cls(int.from_bytes(serialized_data, signed=True, byteorder="big"))

        if format_type == AVRO_FORMAT_TYPE:
            return AvroMessageMixin.deserialize.__func__(cls, format_type, serialized_data)

        if format_type == JSON_FORMAT_TYPE:
            return JsonMessageMixin.deserialize.__func__(cls, format_type, serialized_data)

        raise ValueError("Not supported format type")

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        cls(json.loads(json_str)["value"])

    def to_json(self) -> str:
        return json.dumps({
            "value": self.value
        })



@dataclass(frozen=True)
class Int32Message(AvroMessageMixin, JsonMessageMixin, SerdableMixin):
    """
    Wrap `int` and serialize into 4 bytes integer number

    Author: Nicola Ricciardi
    """

    value: int

    def serialize(self, *, format_type: Optional[str] = None) -> Tuple[str, bytes]:
        if format_type == BYTES_FORMAT_TYPE:
            return BYTES_FORMAT_TYPE, self.value.to_bytes(length=4, byteorder="big")

        if format_type == AVRO_FORMAT_TYPE:
            return AvroMessageMixin.serialize(self)

        if format_type == JSON_FORMAT_TYPE:
            return JsonMessageMixin.serialize(self)

        raise ValueError("Not supported format type")

    @classmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        if format_type == BYTES_FORMAT_TYPE:
            return cls(int.from_bytes(serialized_data, byteorder="big"))

        if format_type == AVRO_FORMAT_TYPE:
            return AvroMessageMixin.deserialize.__func__(cls, format_type, serialized_data)

        if format_type == JSON_FORMAT_TYPE:
            return JsonMessageMixin.deserialize.__func__(cls, format_type, serialized_data)

        raise ValueError("Not supported format type")

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        cls(json.loads(json_str)["value"])

    def to_json(self) -> str:
        return json.dumps({
            "value": self.value
        })


@dataclass(frozen=True)
class Float32Message(AvroMessageMixin, JsonMessageMixin, SerdableMixin):
    """
    Wrap `float` and serialize into 4 bytes floating point

    Author: Nicola Ricciardi
    """

    value: float

    def serialize(self, *, format_type: Optional[str] = None) -> Tuple[str, bytes]:
        if format_type == BYTES_FORMAT_TYPE:
            return BYTES_FORMAT_TYPE, struct.pack(">f", self.value)

        if format_type == AVRO_FORMAT_TYPE:
            return AvroMessageMixin.serialize(self)

        if format_type == JSON_FORMAT_TYPE:
            return JsonMessageMixin.serialize(self)

        raise ValueError("Not supported format type")

    @classmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        if format_type == BYTES_FORMAT_TYPE:
            return cls(struct.unpack(">f", serialized_data)[0])

        if format_type == AVRO_FORMAT_TYPE:
            return AvroMessageMixin.deserialize.__func__(cls, format_type, serialized_data)

        if format_type == JSON_FORMAT_TYPE:
            return JsonMessageMixin.deserialize.__func__(cls, format_type, serialized_data)

        raise ValueError("Not supported format type")

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        cls(json.loads(json_str)["value"])

    def to_json(self) -> str:
        return json.dumps({
            "value": self.value
        })


@dataclass(frozen=True)
class Float64Message(AvroMessageMixin, JsonMessageMixin, SerdableMixin):
    """
    Wrap `float` and serialize into 8 bytes floating point

    Author: Nicola Ricciardi
    """

    value: float

    def serialize(self, *, format_type: Optional[str] = None) -> Tuple[str, bytes]:
        if format_type == BYTES_FORMAT_TYPE:
            return BYTES_FORMAT_TYPE, struct.pack(">d", self.value)

        if format_type == AVRO_FORMAT_TYPE:
            return AvroMessageMixin.serialize(self)

        if format_type == JSON_FORMAT_TYPE:
            return JsonMessageMixin.serialize(self)

        raise ValueError("Not supported format type")

    @classmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        if format_type == BYTES_FORMAT_TYPE:
            return cls(struct.unpack(">d", serialized_data)[0])

        if format_type == AVRO_FORMAT_TYPE:
            return AvroMessageMixin.deserialize.__func__(cls, format_type, serialized_data)

        if format_type == JSON_FORMAT_TYPE:
            return JsonMessageMixin.deserialize.__func__(cls, format_type, serialized_data)

        raise ValueError("Not supported format type")

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        cls(json.loads(json_str)["value"])

    def to_json(self) -> str:
        return json.dumps({
            "value": self.value
        })
