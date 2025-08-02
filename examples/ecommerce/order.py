from dataclasses import dataclass, field
from typing import List
from datetime import datetime

from dataclasses_avroschema import AvroModel

from busline.event.message.avro_message import AvroMessageMixin


@dataclass
class Product(AvroModel):
    name: str
    price: float


@dataclass
class Order(AvroModel):
    products: List[Product]
    user: str


@dataclass
class NewOrderMessage(AvroMessageMixin):
    order: Order
    _when: datetime = field(default=None, init=False)

    def __post_init__(self):
        self._when = datetime.now()


