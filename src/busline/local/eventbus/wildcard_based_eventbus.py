from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from busline.exceptions import TopicNotFound
from busline.client.subscriber.subscriber import Subscriber
from busline.event.event import Event
from busline.local.eventbus.eventbus import EventBus


@dataclass
class WildCardBasedEventBus(EventBus, ABC):
    """
    Abstract class used as base for new eventbus implemented in local projects.

    Author: Nicola Ricciardi
    """

    subscriptions: Dict[str, Set[Subscriber]] = field(default_factory=lambda: defaultdict(set), init=False)
    fire_and_forget: bool = field(default=True)

    @property
    def topics(self) -> List[str]:
        return list(self.subscriptions.keys())

    def reset_subscriptions(self):
        self.subscriptions = defaultdict(set)

    def add_subscriber(self, topic: str, subscriber: Subscriber):
        """
        Add subscriber to topic

        :param topic:
        :param subscriber:
        :return:
        """

        self.subscriptions[topic].add(subscriber)

    def remove_subscriber(self, subscriber: Subscriber, topic: Optional[str] = None, raise_if_topic_missed: bool = False):
        """
        Remove subscriber from topic selected or from all if topic is None

        :param raise_if_topic_missed:
        :param subscriber:
        :param topic:
        :return:
        """

        if raise_if_topic_missed and topic is not None and topic not in self.subscriptions.keys():
            raise TopicNotFound(f"topic '{topic}' not found")

        for name in self.subscriptions.keys():

            if topic is None or self._topic_names_match(topic, name):
                if subscriber in self.subscriptions[name]:
                    self.subscriptions[name].remove(subscriber)


    def _topic_names_match(self, t1: str, t2: str):
        return t1 == t2

    def _get_topic_subscriptions(self, topic: str) -> Set[Subscriber]:

        topic_subscriptions: Set[Subscriber] = set()
        for t, subs in self.subscriptions.items():
            if self._topic_names_match(t, topic):
                topic_subscriptions = topic_subscriptions.union(subs)

        return topic_subscriptions

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

