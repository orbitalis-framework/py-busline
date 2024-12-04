from abc import ABC, abstractmethod
from typing import Dict, List
from busline.eventbus.exceptions import TopicNotFound
from busline.eventbus_client.subscriber.subscriber import Subscriber
from busline.eventbus.topic import Topic
from busline.event.event import Event



class EventBus(ABC):
    """
    Abstract class used as base for new eventbus implemented in local projects.

    Eventbus are *singleton*

    Author: Nicola Ricciardi
    """

    # === SINGLETON pattern ===
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        self.__subscriptions = None
        self.__topics = None

        self.reset_topics()

    def reset_topics(self):
        self.__topics: Dict[str, Topic] = {}
        self.__subscriptions: Dict[str, List[Subscriber]] = {}

    def add_topic(self, topic: Topic):
        self.__topics[topic.name] = topic
        self.__subscriptions[topic.name] = []

    def remove_topic(self, topic_name: str):
        """
        Remove topic by name

        :param topic_name:
        :return:
        """

        del self.__topics[topic_name]
        del self.__subscriptions[topic_name]

    @property
    def topics(self) -> Dict[str, Topic]:
        return self.__topics

    @property
    def subscriptions(self) -> Dict[str, List[Subscriber]]:
        return self.__subscriptions

    def add_subscriber(self, topic_name: str, subscriber: Subscriber, raise_if_topic_missed: bool = False):
        """
        Add subscriber to topic

        :param raise_if_topic_missed:
        :param topic_name:
        :param subscriber:
        :return:
        """

        if topic_name not in self.__topics:
            if raise_if_topic_missed:
                raise TopicNotFound(f"topic '{topic_name}' not found")

            else:
                self.add_topic(Topic(topic_name))

        self.__subscriptions[topic_name].append(subscriber)

    def remove_subscriber(self, subscriber: Subscriber, topic_name: str = None, raise_if_topic_missed: bool = False):
        """
        Remove subscriber from topic selected or from all if topic is None

        :param raise_if_topic_missed:
        :param subscriber:
        :param topic_name:
        :return:
        """

        if raise_if_topic_missed and isinstance(topic_name, str) and topic_name not in self.__topics.keys():
            raise TopicNotFound(f"topic '{topic_name}' not found")

        for name in self.__topics.keys():

            if topic_name is None or topic_name == name:
                self.__subscriptions[name].remove(subscriber)


    @abstractmethod
    async def put_event(self, topic_name: str, event: Event):
        """
        Put a new event in the bus and notify subscribers of corresponding
        event's topic

        :param topic_name:
        :param event:
        :return:
        """

        raise NotImplemented()

