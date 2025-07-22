from dataclasses import dataclass
from typing import Self, Tuple
from busline.event.message.message import Message
from busline.utils.serde import SerdableMixin


STRING_FORMAT_TYPE = "string"


@dataclass(frozen=True)
class RawStringMessage(Message, SerdableMixin):

    value: str

    def serialize(self) -> Tuple[str, bytes]:
        return STRING_FORMAT_TYPE, self.value.encode("utf-8")

    @classmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        if format_type != STRING_FORMAT_TYPE:
            raise ValueError(f"{format_type} != {STRING_FORMAT_TYPE}")

        return cls(serialized_data.decode("utf-8"))
