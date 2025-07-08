from abc import ABC, abstractmethod
from typing import Dict, List

from busline.client.subscriber.topic_subscriber.event_handler.event_handler import EventHandler


class SchemafullEventHandler(EventHandler, ABC):

    @abstractmethod
    def input_schemas(self) -> List[Dict]:
        raise NotImplemented()
