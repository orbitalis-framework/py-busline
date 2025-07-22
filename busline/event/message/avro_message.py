from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Self, Tuple

from dataclasses_avroschema import AvroModel
import json

from busline.event.message.message import Message
from busline.utils.serde import SerdableMixin


AVRO_FORMAT_TYPE = "avro"


class AvroMessageMixin(Message, SerdableMixin, AvroModel, ABC):

    def serialize(self) -> Tuple[str, bytes]:
        return AVRO_FORMAT_TYPE, AvroModel.serialize(self, serialization_type=AVRO_FORMAT_TYPE)

    @classmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        if format_type != AVRO_FORMAT_TYPE:
            raise ValueError(f"{format_type} != {AVRO_FORMAT_TYPE}")

        return AvroModel.deserialize.__func__(cls, serialized_data, serialization_type=AVRO_FORMAT_TYPE)
        # __func__ instead of __call__ because `AvroModel.deserialize` is a classmethod