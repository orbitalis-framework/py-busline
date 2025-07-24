from dataclasses import dataclass, field
from typing import Self, Tuple, Literal, Optional
import struct

from busline.event.message.message import Message, BYTES_FORMAT_TYPE
from busline.utils.serde import SerdableMixin




@dataclass(frozen=True)
class Int64Message(Message, SerdableMixin):
    """
    Wrap `int` and serialize into 8 bytes integer number

    Author: Nicola Ricciardi
    """

    value: int

    def serialize(self, *, format_type: Optional[str] = None) -> Tuple[str, bytes]:
        return BYTES_FORMAT_TYPE, self.value.to_bytes(length=8, signed=True, byteorder="big")

    @classmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        if format_type != BYTES_FORMAT_TYPE:
            raise ValueError(f"{format_type} != {BYTES_FORMAT_TYPE}")

        return cls(int.from_bytes(serialized_data, signed=True, byteorder="big"))


@dataclass(frozen=True)
class Int32Message(Message, SerdableMixin):
    """
    Wrap `int` and serialize into 4 bytes integer number

    Author: Nicola Ricciardi
    """

    value: int

    def serialize(self, *, format_type: Optional[str] = None) -> Tuple[str, bytes]:
        return BYTES_FORMAT_TYPE, self.value.to_bytes(length=4, byteorder="big")

    @classmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        if format_type != BYTES_FORMAT_TYPE:
            raise ValueError(f"{format_type} != {BYTES_FORMAT_TYPE}")

        return cls(int.from_bytes(serialized_data, byteorder="big"))


@dataclass(frozen=True)
class Float32Message(Message, SerdableMixin):
    """
    Wrap `float` and serialize into 4 bytes floating point

    Author: Nicola Ricciardi
    """

    value: float

    def serialize(self, *, format_type: Optional[str] = None) -> Tuple[str, bytes]:
        return BYTES_FORMAT_TYPE, struct.pack(">f", self.value)

    @classmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        if format_type != BYTES_FORMAT_TYPE:
            raise ValueError(f"{format_type} != {BYTES_FORMAT_TYPE}")

        return cls(struct.unpack(">f", serialized_data)[0])


@dataclass(frozen=True)
class Float64Message(Message, SerdableMixin):
    """
    Wrap `float` and serialize into 8 bytes floating point

    Author: Nicola Ricciardi
    """

    value: float

    def serialize(self, *, format_type: Optional[str] = None) -> Tuple[str, bytes]:
        return BYTES_FORMAT_TYPE, struct.pack(">d", self.value)

    @classmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        if format_type != BYTES_FORMAT_TYPE:
            raise ValueError(f"{format_type} != {BYTES_FORMAT_TYPE}")

        return cls(struct.unpack(">d", serialized_data)[0])
