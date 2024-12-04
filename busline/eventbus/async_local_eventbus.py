import logging
import asyncio

from busline.event.event import Event
from busline.eventbus.eventbus import EventBus


class AsyncLocalEventBus(EventBus):
    """
    Async local eventbus (singleton)

    Author: Nicola Ricciardi
    """

    async def put_event(self, topic_name: str, event: Event):

        topic_subscriptions = self.subscriptions.get(topic_name, [])

        logging.debug(f"new event {event} on topic {topic_name}, notify subscribers: {topic_subscriptions}")

        if len(topic_subscriptions) == 0:
            return

        tasks = []

        for subscriber in topic_subscriptions:
            task = asyncio.create_task(subscriber.on_event(topic_name, event))
            tasks.append(task)

        await asyncio.gather(*tasks)

            
