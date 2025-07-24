from abc import ABC, abstractmethod
from busline.event.event import Event


class EventHandler(ABC):
    """

    Author: Nicola Ricciardi
    """

    @abstractmethod
    async def handle(self, topic: str, event: Event):
        """
        Manage an event of a topic
        """