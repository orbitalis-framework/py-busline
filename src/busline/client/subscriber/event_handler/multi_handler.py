from typing import List
import asyncio
from dataclasses import dataclass
from busline.event.event import Event
from busline.client.subscriber.event_handler.event_handler import EventHandler


@dataclass
class MultiEventHandler(EventHandler):
    """
    Call a batch of pre-defined handlers.

    Another parameter can be specified. If strict order is False, async capabilities can be exploited

    Author: Nicola Ricciardi
    """

    handlers: List[EventHandler]
    strict_order: bool = False


    async def handle(self, topic: str, event: Event):
        if self.strict_order:
            for handler in self.handlers:
                await handler.handle(topic, event)
        else:
            tasks = [handler.handle(topic, event) for handler in self.handlers]

            await asyncio.gather(*tasks)
            