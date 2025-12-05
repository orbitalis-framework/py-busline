from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from busline.exceptions import TopicNotFound
from busline.client.subscriber.subscriber import Subscriber
from busline.event.event import Event


@dataclass
class EventBus(ABC):
    """
    Abstract class used as base for new eventbus implemented in local projects.
    Optimized for O(1) direct topic lookup.

    Author: Nicola Ricciardi
    """

    subscriptions: Dict[str, Set[Subscriber]] = field(default_factory=lambda: defaultdict(set), init=False)

    @property
    def topics(self) -> List[str]:
        return list(self.subscriptions.keys())

    def reset_subscriptions(self):
        self.subscriptions = defaultdict(set)

    def add_subscriber(self, topic: str, subscriber: Subscriber):
        self.subscriptions[topic].add(subscriber)

    def remove_subscriber(self, subscriber: Subscriber, topic: Optional[str] = None, raise_if_topic_missed: bool = False):
        """
        Remove subscriber from a specific topic (O(1)) or from all topics if topic is None.
        """
        
        # Check if topic exists if strict checking is requested
        if raise_if_topic_missed and topic is not None and topic not in self.subscriptions:
            raise TopicNotFound(f"topic '{topic}' not found")

        if topic is not None:
            # Direct access O(1), no wildcard matching
            if topic in self.subscriptions:
                self.subscriptions[topic].discard(subscriber)
                
                # Optional: Cleanup empty topics to keep `topics` property clean
                if not self.subscriptions[topic]:
                    del self.subscriptions[topic]
        else:
            # Fallback: Iterate all topics only when unsubscribing from EVERYTHING
            # We use list(keys) to allow modification during iteration if needed
            for topic_name in list(self.subscriptions.keys()):
                self.subscriptions[topic_name].discard(subscriber)
                
                if not self.subscriptions[topic_name]:
                    del self.subscriptions[topic_name]

    def _get_topic_subscriptions(self, topic: str) -> Set[Subscriber]:
        """
        Retrieve subscribers for a topic using direct hash lookup O(1).
        """
        # OPTIMIZED: No iteration. Returns the set directly.
        # Uses .get() to return an empty set if topic has no subscribers.
        return self.subscriptions.get(topic, set())

    @abstractmethod
    async def put_event(self, topic: str, event: Event):
        raise NotImplemented()