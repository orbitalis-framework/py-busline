from dataclasses import dataclass, field
from typing import List, Optional

from busline.mqtt.mqtt_publisher import MqttPublisher
from examples.ecommerce import NEW_ORDER_TOPIC
from examples.ecommerce.order import Product, NewOrderMessage, Order


@dataclass
class EcommerceBackend:
    _logged_user: Optional[str] = field(default=None, init=False)

    _publisher: MqttPublisher = field(default_factory=lambda: MqttPublisher(hostname="127.0.0.1"), init=False)
    _cart: List[Product] = field(default_factory=list, init=False)

    async def start(self):
        await self._publisher.connect()

    def login(self, user: str):
        self._logged_user = user
        self._cart = []

    def add_to_cart(self, product: Product):
        if self._logged_user is None:
            raise RuntimeError("You are not logged in")

        self._cart.append(product)
        print(f"{product} was added to cart!")

    async def buy(self):
        if self._logged_user is None:
            raise RuntimeError("You are not logged in")

        order = Order(
            products=self._cart,
            user=self._logged_user
        )

        await self._publisher.publish(
            topic=NEW_ORDER_TOPIC,
            message=NewOrderMessage(order)
        )

        print("Order published")







