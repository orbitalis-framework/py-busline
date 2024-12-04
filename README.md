# Busline for Python

Agnostic eventbus for Python.

Official eventbus library for [Orbitalis](https://github.com/orbicore/orbitalis)

## Local EventBus

### Using Publisher/Subscriber

```python
from busline.eventbus.async_local_eventbus import AsyncLocalEventBus
from busline.eventbus_client.publisher.local_eventbus_publisher import LocalEventBusPublisher
from busline.event.event import Event
from busline.eventbus_client.subscriber.local_eventbus_closure_subscriber import LocalEventBusClosureSubscriber

local_eventbus_instance = AsyncLocalEventBus()  # singleton


def callback(topic_name: str, event: Event):
    print(event)


subscriber = LocalEventBusClosureSubscriber(local_eventbus_instance, callback)
publisher = LocalEventBusPublisher(local_eventbus_instance)

await subscriber.subscribe("test-topic")

await publisher.publish("test-topic", Event())  # publish empty event
```

### Using EventBusClient

```python
from busline.event.event import Event
from busline.eventbus_client.local_eventbus_client import LocalEventBusClient


def callback(topic_name: str, event: Event):
    print(event)


client = LocalEventBusClient(callback)

await client.subscribe("test")

await client.publish("test", Event())
```


## Create Agnostic EventBus

Implement business logic of your `Publisher` and `Subscriber` and... done. Nothing more.

```python
from busline.event.event import Event
from busline.eventbus_client.publisher.publisher import Publisher


class YourEventBusPublisher(Publisher):

    async def _internal_publish(self, topic_name: str, event: Event, **kwargs):
        pass  # send events to your eventbus (maybe in cloud?)
```

```python
from busline.eventbus_client.subscriber.subscriber import Subscriber
from busline.event.event import Event


class YourEventBusSubscriber(Subscriber):

    async def on_event(self, topic_name: str, event: Event, **kwargs):
        pass  # receive your events
```

You could create a client to allow components to use it instead of become a publisher or subscriber.

```python
from busline.eventbus_client.eventbus_client import EventBusClient
from busline.event.event import Event


def client_callback(topic_name: str, e: Event):
    print(e)


subscriber = YourEventBusSubscriber(...)
publisher = YourEventBusPublisher(...)

client = EventBusClient(publisher, subscriber, ClosureEventListener(client_callback))
```





