from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from busline.exceptions import TopicNotFound
from busline.client.subscriber.subscriber import Subscriber
from busline.event.event import Event


@dataclass
class EventBus(ABC):
    """
    Abstract class used as base for new eventbus implemented in local projects.

    Author: Nicola Ricciardi
    """

    subscriptions: Dict[str, List[Subscriber]] = field(default_factory=dict)

    def __post_init__(self):

        self.reset_subscriptions()

    def reset_subscriptions(self):
        self.subscriptions = {}

    @property
    def topics(self) -> List[str]:
        return list(self.subscriptions.keys())

    def add_subscriber(self, topic: str, subscriber: Subscriber):
        """
        Add subscriber to topic

        :param topic:
        :param subscriber:
        :return:
        """

        self.subscriptions.setdefault(topic, [])
        self.subscriptions[topic].append(subscriber)

    def remove_subscriber(self, subscriber: Subscriber, topic: Optional[str] = None, raise_if_topic_missed: bool = False):
        """
        Remove subscriber from topic selected or from all if topic is None

        :param raise_if_topic_missed:
        :param subscriber:
        :param topic:
        :return:
        """

        if raise_if_topic_missed and isinstance(topic, str) and topic not in self.subscriptions.keys():
            raise TopicNotFound(f"topic '{topic}' not found")

        for name in self.subscriptions.keys():

            if topic is None or topic == name:
                self.subscriptions[name].remove(subscriber)


    def _topic_names_match(self, t1: str, t2: str):
        return t1 == t2

    @abstractmethod
    async def put_event(self, topic: str, event: Event):
        """
        Put a new event in the bus and notify subscribers of corresponding
        event's topic

        :param topic:
        :param event:
        :return:
        """

        raise NotImplemented()

