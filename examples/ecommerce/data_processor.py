import asyncio
from dataclasses import dataclass, field

from busline.client.subscriber.event_handler import event_handler
from busline.event.event import Event
from busline.local.eventbus.local_eventbus import LocalEventBus
from busline.local.local_publisher import LocalPublisher
from busline.mqtt.mqtt_subscriber import MqttSubscriber
from examples.ecommerce import NEW_ORDER_TOPIC
from examples.ecommerce.ai_model import INBOUND_DATA_TOPIC
from examples.ecommerce.order import Product, NewOrderMessage, Order


@dataclass
class DataProcessor:
    _subscriber: MqttSubscriber = field(default_factory=lambda: MqttSubscriber(hostname="127.0.0.1"), init=False)
    _publisher: LocalPublisher = field(default_factory=lambda: LocalPublisher(eventbus=LocalEventBus()), init=False)

    @event_handler
    async def new_order_event_handler(self, topic: str, event: Event[NewOrderMessage]):
        await self._publisher.publish(
                topic=INBOUND_DATA_TOPIC,
                message=len(event.payload.order.products)
            )

    async def start(self):
        await asyncio.gather(
            self._subscriber.connect(),
            self._publisher.connect()
        )

        await self._subscriber.subscribe(
            topic=NEW_ORDER_TOPIC,
            handler=self.new_order_event_handler
        )

        print("DataProcessor subscribed")







