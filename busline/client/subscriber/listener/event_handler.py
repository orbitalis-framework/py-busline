from abc import ABC, abstractmethod
from busline.event.event import Event


class EventHandler(ABC):

    @abstractmethod
    async def on_event(self, topic: str, event: Event):
        """
        Callback called when new event arrives

        :param topic:
        :param event:
        :return:
        """