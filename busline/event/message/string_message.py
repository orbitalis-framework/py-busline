import json
from dataclasses import dataclass
from typing import Self, Tuple, Optional

from busline.event.message.avro_message import AVRO_FORMAT_TYPE, AvroMessageMixin
from busline.event.message.json_message import JsonMessageMixin, JSON_FORMAT_TYPE
from busline.event.message.message import Message
from busline.utils.serde import SerdableMixin


STRING_FORMAT_TYPE = "utf-8"


@dataclass(frozen=True)
class StringMessage(AvroMessageMixin, JsonMessageMixin, SerdableMixin):
    """
    Wrap `str` and serialize into UTF-8

    Author: Nicola Ricciardi
    """

    value: str

    def serialize(self, *, format_type: Optional[str] = None) -> Tuple[str, bytes]:

        if format_type is None or format_type == STRING_FORMAT_TYPE:
            return STRING_FORMAT_TYPE, self.value.encode("utf-8")

        if format_type == AVRO_FORMAT_TYPE:
            return AvroMessageMixin.serialize(self)

        if format_type == JSON_FORMAT_TYPE:
            return JsonMessageMixin.serialize(self)

        raise ValueError("Not supported format type")

    @classmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        if format_type == STRING_FORMAT_TYPE:
            return cls(serialized_data.decode("utf-8"))

        if format_type == AVRO_FORMAT_TYPE:
            return AvroMessageMixin.deserialize.__func__(cls, format_type, serialized_data)

        if format_type == JSON_FORMAT_TYPE:
            return JsonMessageMixin.deserialize.__func__(cls, format_type, serialized_data)

        raise ValueError("Not supported format type")


    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls(json.loads(json_str)["value"])

    def to_json(self) -> str:
        return json.dumps({
            "value": self.value
        })