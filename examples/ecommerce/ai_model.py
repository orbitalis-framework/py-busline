from dataclasses import dataclass, field

from busline.client.subscriber.event_handler import event_handler
from busline.event.event import Event
from busline.event.message.number_message import Int64Message
from busline.local.eventbus.local_eventbus import LocalEventBus
from busline.local.local_subscriber import LocalSubscriber


INBOUND_DATA_TOPIC = "inbound_data"


@dataclass
class AIModel:
    _subscriber: LocalSubscriber = field(default_factory=lambda: LocalSubscriber(eventbus=LocalEventBus()), init=False)

    def online_training(self, value: int):
        print(f"Online training with value: {value}")

    @event_handler
    async def new_data_event_handler(self, topic: str, event: Event[Int64Message]):
        self.online_training(event.payload.value)

    async def start(self):
        await self._subscriber.connect()

        await self._subscriber.subscribe(
            topic=INBOUND_DATA_TOPIC,
            handler=self.new_data_event_handler
        )

















