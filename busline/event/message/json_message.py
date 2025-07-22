from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Self, Tuple
import json
from busline.event.message.message import Message
from busline.utils.serde import SerdableMixin


JSON_FORMAT_TYPE = "json"


@dataclass(frozen=True)
class JsonMessageMixin(Message, SerdableMixin, ABC):

    @classmethod
    @abstractmethod
    def from_json(cls, json_str: str) -> Self:
        raise NotImplemented()

    @abstractmethod
    def to_json(self) -> str:
        raise NotImplemented()

    def serialize(self) -> Tuple[str, bytes]:
        return JSON_FORMAT_TYPE, json.dumps(self.to_json()).encode("utf-8")

    @classmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        if format_type != JSON_FORMAT_TYPE:
            raise ValueError(f"{format_type} != {JSON_FORMAT_TYPE}")

        return cls.from_json(serialized_data.decode("utf-8"))
