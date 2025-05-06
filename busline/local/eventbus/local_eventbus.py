from busline.event.event import Event
from busline.local import DEFAULT_EVENT_BUS_INSTANCE
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
            cls._instance = DEFAULT_EVENT_BUS_INSTANCE # super().__new__(cls)

        return cls._instance

    async def put_event(self, topic: str, event: Event):
        return self._instance.put_event(topic, event)