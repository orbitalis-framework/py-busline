from abc import abstractmethod
from collections.abc import Buffer
from typing import Self, Tuple
from dataclasses import dataclass, asdict
from busline.event.event import EventPayload
import pickle
import json

from busline.utils.serde import SerdableMixin

JSON_FORMAT_TYPE = "json"


@dataclass(frozen=True)
class JsonEventPayload(EventPayload, SerdableMixin):

    @classmethod
    @abstractmethod
    def from_json(cls, json_str: str) -> Self:
        raise NotImplemented()

    def serialize(self) -> Tuple[str, bytes]:
        return JSON_FORMAT_TYPE, pickle.dumps(json.dumps(asdict(self)))

    @classmethod
    def deserialize(cls, format_type: str, serialized_payload: bytes) -> Self:
        if format_type != JSON_FORMAT_TYPE:
            raise ValueError("Unsupported format type")

        return cls.from_json(pickle.loads(serialized_payload))
