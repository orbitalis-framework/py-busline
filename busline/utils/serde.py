from abc import ABC, abstractmethod
from typing import Tuple, Self


class SerializableMixin(ABC):
    """
    Author: Nicola Ricciardi
    """


    @abstractmethod
    def serialize(self) -> Tuple[str, bytes]:
        """
        Serialize itself and return the format as string
        """

        raise NotImplemented()


class DeserializableMixin(ABC):
    """
    Author: Nicola Ricciardi
    """

    @classmethod
    @abstractmethod
    def deserialize(cls, payload_type: str, payload: bytes) -> Self:
        raise NotImplemented()


class SerdableMixin(SerializableMixin, DeserializableMixin, ABC):
    pass

