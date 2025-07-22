from abc import ABC, abstractmethod
from typing import Tuple, Self


class SerializableMixin(ABC):
    """
    Author: Nicola Ricciardi
    """


    @abstractmethod
    def serialize(self) -> Tuple[str, bytes]:
        """
        Serialize itself and return (format type, serialized data).
        For example, ("json", "{...}").
        """

        raise NotImplemented()


class DeserializableMixin(ABC):
    """
    Author: Nicola Ricciardi
    """

    @classmethod
    @abstractmethod
    def deserialize(cls, format_type: str, serialized_data: bytes) -> Self:
        raise NotImplemented()


class SerdableMixin(SerializableMixin, DeserializableMixin, ABC):
    pass

