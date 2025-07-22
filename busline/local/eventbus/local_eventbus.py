import logging

from busline.event.event import Event
from busline.local.eventbus.async_local_eventbus import AsyncLocalEventBus
from busline.local.eventbus.eventbus import EventBus


class LocalEventBus(EventBus):
    """
    Local *singleton* event bus instance

    Author: Nicola Ricciardi
    """

    # === SINGLETON pattern ===
    _instance = None


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = AsyncLocalEventBus() # super().__new__(cls)

        return cls._instance


    async def put_event(self, topic: str, event: Event):
        logging.debug(f"New event: {topic} -> {event}")
        return self._instance.put_event(topic, event)