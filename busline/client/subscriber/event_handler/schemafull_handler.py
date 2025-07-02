from abc import ABC, abstractmethod
from typing import Dict

from busline.client.subscriber.event_handler.event_handler import EventHandler
from busline.event.event import Event


class SchemafullEventHandler(EventHandler, ABC):

    @abstractmethod
    def input_schema(self) -> Dict:
        raise NotImplemented()

    @abstractmethod
    def output_schema(self) -> Dict:
        raise NotImplemented()