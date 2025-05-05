from abc import ABC, abstractmethod
from uuid import uuid4
from typing import Optional
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class EventBusConnector(ABC):
    """
    Abstract class which provides methods to interact with eventbus

    Author: Nicola Ricciardi
    """

    identifier: str = field(default=str(uuid4()))


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