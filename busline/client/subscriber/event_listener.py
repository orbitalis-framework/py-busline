from abc import ABC, abstractmethod
from busline.event.event import Event


class EventListener(ABC):

    @abstractmethod
    async def on_event(self, topic_name: str, event: Event, **kwargs):
        """
        Callback called when new event arrives

        :param topic_name:
        :param event:
        :return:
        """