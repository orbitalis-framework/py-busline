import logging
import asyncio
from dataclasses import dataclass
from busline.event.event import Event
from busline.local.eventbus.eventbus import EventBus


@dataclass
class AsyncLocalEventBus(EventBus):
    """
    Async local eventbus

    Author: Nicola Ricciardi
    """

    async def put_event(self, topic: str, event: Event):

        topic_subscriptions = self._get_topic_subscriptions(topic)

        logging.debug(f"new event {event} on topic {topic}, notify subscribers: {topic_subscriptions}")

        tasks = [subscriber.on_event(topic, event) for subscriber in topic_subscriptions]

        await asyncio.gather(*tasks)

            
