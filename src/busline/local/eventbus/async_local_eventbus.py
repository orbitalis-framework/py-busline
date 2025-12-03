import logging
import asyncio
from dataclasses import dataclass, field
from busline.event import event
from busline.event.event import Event
from busline.local.eventbus.eventbus import EventBus


@dataclass
class AsyncLocalEventBus(EventBus):
    """
    Async local eventbus

    Author: Nicola Ricciardi
    """

    _events_counter: int = field(default=0)

    @property
    def events_counter(self) -> int:
        return self._events_counter

    def reset_events_counter(self):
        self._events_counter = 0

    async def put_event(self, topic: str, event: Event):

        self._events_counter += 1

        topic_subscriptions = self._get_topic_subscriptions(topic)

        logging.debug("new event %s on topic %s, notify subscribers: %s", event, topic, topic_subscriptions)

        tasks = [subscriber.notify(topic, event) for subscriber in topic_subscriptions]

        if self.fire_and_forget:
            # schedule and return immediately
            for t in tasks:
                asyncio.create_task(t)
        else:
            # avoid creating extra tasks when we will wait anyway
            await asyncio.gather(*tasks)


