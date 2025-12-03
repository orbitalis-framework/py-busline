from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass, field
import uuid

def _generate_identifier():
    return str(uuid.uuid4())


@dataclass(kw_only=True)
class EventBusConnector(ABC):
    """
    Abstract class which provides methods to interact with eventbus

    Author: Nicola Ricciardi
    """

    identifier: str = field(default_factory=_generate_identifier)


    @abstractmethod
    async def connect(self):
        """
        Connect to eventbus

        :return:
        """

    @abstractmethod
    async def disconnect(self):
        """
        Disconnect to eventbus

        :return:
        """

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)