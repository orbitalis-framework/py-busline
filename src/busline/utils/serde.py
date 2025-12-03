from abc import ABC, abstractmethod
from typing import Tuple, Self, Optional


class SerializableMixin(ABC):
    """
    Author: Nicola Ricciardi
    """


    @abstractmethod
    def serialize(self, *, format_type: Optional[str] = None) -> Tuple[str, bytes]:
        """
        Serialize itself and return (format type, serialized data).
        For example, ("json", "{...}").

        Explicitly provide format_type to choose it, otherwise default is used
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

