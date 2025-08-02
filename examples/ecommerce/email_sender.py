import asyncio
from dataclasses import dataclass, field

from busline.client.subscriber.event_handler import event_handler
from busline.event.event import Event
from busline.mqtt.mqtt_subscriber import MqttSubscriber
from examples.ecommerce import NEW_ORDER_TOPIC
from examples.ecommerce.order import Product, NewOrderMessage, Order


@dataclass
class ConfirmationEmailSender:
    _subscriber: MqttSubscriber = field(default_factory=lambda: MqttSubscriber(hostname="127.0.0.1"), init=False)

    async def send_email(self, user: str):
        print(f"Sending email to {user}...")
        await asyncio.sleep(1)
        print(f"Email sent")

    @event_handler
    async def new_order_event_handler(self, topic: str, event: Event[NewOrderMessage]):
        await self.send_email(event.payload.order.user)

    async def start(self):
        await self._subscriber.connect()

        await self._subscriber.subscribe(
            topic=NEW_ORDER_TOPIC,
            handler=self.new_order_event_handler
        )

        print("ConfirmationEmailSender subscribed")







