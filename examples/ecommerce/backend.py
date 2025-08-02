from dataclasses import dataclass, field
from typing import List

from busline.mqtt.mqtt_publisher import MqttPublisher
from examples.ecommerce import NEW_ORDER_TOPIC
from examples.ecommerce.order import Product, NewOrderMessage, Order


@dataclass
class EcommerceFrontend:
    logged_user: str

    _publisher: MqttPublisher = field(default_factory=lambda: MqttPublisher(hostname="127.0.0.1"))
    _chart: List[Product] = field(default_factory=list)

    def add_to_chart(self, product: Product):
        self._chart.append(product)

    async def buy(self):
        order = Order(
            products=self._chart,
            user=self.logged_user
        )

        await self._publisher.publish(
            topic=NEW_ORDER_TOPIC,
            message=NewOrderMessage(order)
        )







