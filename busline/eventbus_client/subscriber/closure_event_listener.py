from typing import Callable
from busline.event.event import Event
from busline.eventbus_client.subscriber.event_listener import EventListener


class ClosureEventListener(EventListener):
    """
    Abstract event listener which use a pre-defined callback as `on_event`

    Author: Nicola Ricciardi
    """

    def __init__(self, on_event_callback: Callable[[str, Event], None]):
        EventListener.__init__(self)

        self.__on_event_callback = on_event_callback

    async def on_event(self, topic_name: str, event: Event, **kwargs):
        self.__on_event_callback(topic_name, event, **kwargs)
