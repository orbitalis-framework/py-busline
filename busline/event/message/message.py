from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Self, Tuple

from dataclasses_avroschema import AvroModel
import json

from busline.utils.serde import SerdableMixin



class Message(SerdableMixin, ABC):
    """
    Event message for an event, it must be serializable and deserializable

    Author: Nicola Ricciardi
    """


