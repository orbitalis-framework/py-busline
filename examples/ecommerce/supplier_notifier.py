from dataclasses import dataclass, field

from busline.client.subscriber.event_handler import event_handler
from busline.event.event import Event
from busline.mqtt.mqtt_subscriber import MqttSubscriber
from examples.ecommerce import NEW_ORDER_TOPIC
from examples.ecommerce.order import Product, NewOrderMessage, Order


@dataclass
class SupplierNotifier:
    _subscriber: MqttSubscriber = field(default_factory=lambda: MqttSubscriber(hostname="127.0.0.1"), init=False)

    @event_handler
    async def new_order_event_handler(self, topic: str, event: Event[NewOrderMessage]):
        print(f"Supplier was notified. New order: {event.payload.order}")

    async def start(self):
        await self._subscriber.connect()

        await self._subscriber.subscribe(
            topic=NEW_ORDER_TOPIC,
            handler=self.new_order_event_handler
        )

        print("SupplierNotifier subscribed")





