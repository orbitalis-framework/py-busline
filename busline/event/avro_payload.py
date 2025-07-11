from abc import abstractmethod
from collections.abc import Buffer
from typing import Self, Tuple
from dataclasses import dataclass, asdict

from dataclasses_avroschema import AvroModel

from busline.event.event import EventPayload
from busline.utils.serde import SerdableMixin

AVRO_CONTENT_TYPE = "avro"


@dataclass(frozen=True)
class AvroEventPayload(EventPayload, SerdableMixin, AvroModel):


    def serialize(self) -> Tuple[str, bytes]:
        return AVRO_CONTENT_TYPE, AvroModel.serialize(self, serialization_type=AVRO_CONTENT_TYPE)

    @classmethod
    def deserialize(cls, format_type: str, serialized_payload: bytes) -> Self:
        if format_type != AVRO_CONTENT_TYPE:
            raise ValueError("Unsupported format type")

        return AvroModel.deserialize.__func__(cls, serialized_payload, serialization_type=AVRO_CONTENT_TYPE)
        # __func__ instead of __call__ because `AvroModel.deserialize` is a classmethod
