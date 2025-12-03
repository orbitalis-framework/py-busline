import logging
import asyncio
from typing import List, Awaitable
from dataclasses import dataclass, field
from busline.event.event import Event
from busline.local.eventbus.eventbus import EventBus


@dataclass
class AsyncLocalEventBus(EventBus):
    """
    Standard Async EventBus optimized for I/O-bound tasks.
    Uses asyncio.create_task for concurrency without blocking the loop.

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

        # O(1) Lookup from the optimized base class
        topic_subscriptions = self._get_topic_subscriptions(topic)

        if not topic_subscriptions:
            return

        logging.debug("Event on %s: %s", topic, event)

        # Create coroutines list
        # Note: We rely on the subscriber.notify() implementation to be non-blocking
        tasks: List[Awaitable] = [
            subscriber.notify(topic, event) for subscriber in topic_subscriptions
        ]

        if self.fire_and_forget:
            # Schedule execution immediately on the loop without waiting
            for t in tasks:
                asyncio.create_task(t)
        else:
            # Wait for all subscribers to finish
            await asyncio.gather(*tasks)