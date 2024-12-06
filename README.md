# Busline for Python

Agnostic eventbus for Python.

Official eventbus library for [Orbitalis](https://github.com/orbitalis-framework/py-orbitalis)

## Get Start

### Local EventBus

#### Using Publisher/Subscriber

```python
from busline.local_client.publisher.local_eventbus_publisher import LocalEventBusPublisher
from busline.event.event import Event
from busline.local_client.subscriber.local_eventbus_closure_subscriber import LocalEventBusClosureSubscriber

def callback(topic_name: str, event: Event):
    print(event)


subscriber = LocalEventBusClosureSubscriber(callback)
publisher = LocalEventBusPublisher()

await subscriber.subscribe("test-topic")

await publisher.publish("test-topic", Event())  # publish empty event
```

#### Using EventBusClient

```python
from busline.event.event import Event
from busline.local_client.local_eventbus_client import LocalEventBusClient


def callback(topic_name: str, event: Event):
    print(event)


client = LocalEventBusClient(callback)

await client.subscribe("test")

await client.publish("test", Event())
```

#### Specifying EventBus

Local eventbuses use an internal implemented `EventBus`, this sort of architecture is not required in other scenarios such
as MQTT, because the "eventbus" is the broken.

Anyway, you may want to specify what `EventBus` instance your pub/sub components should use:

```python
local_eventbus_instance = AsyncLocalEventBus()

subscriber = LocalEventBusClosureSubscriber(callback, eventbus_instance=local_eventbus_instance)
publisher = LocalEventBusPublisher(eventbus_instance=local_eventbus_instance2)
```


### Create Agnostic EventBus

Implement business logic of your `Publisher` and `Subscriber` and... done. Nothing more.

```python
from busline.event.event import Event
from busline.client.publisher.publisher import Publisher


class YourEventBusPublisher(Publisher):

    async def _internal_publish(self, topic_name: str, event: Event, **kwargs):
        pass  # send events to your eventbus (maybe in cloud?)
```

```python
from busline.client.subscriber.subscriber import Subscriber
from busline.event.event import Event


class YourEventBusSubscriber(Subscriber):

    async def on_event(self, topic_name: str, event: Event, **kwargs):
        pass  # receive your events
```

You could create a client to allow components to use it instead of become a publisher or subscriber.

```python
from busline.client.eventbus_client import EventBusClient
from busline.event.event import Event


def client_callback(topic_name: str, e: Event):
    print(e)


subscriber = YourEventBusSubscriber(...)
publisher = YourEventBusPublisher(...)

client = EventBusClient(publisher, subscriber, ClosureEventListener(client_callback))
```


## Subscriber

`Subscriber` is the component which receives events. It is a `EventHandler`, therefore it has `on_event` method in which 
every event (and related topic) is passed.

### MultiHandlerSubscriber

`MultiHandlerSubscriber` is an enhanced subscriber which manages multi-handlers for each topic. We can specify a _default handler_,
which is run every time a new event comes. In addiction, we can (but it is not needed) specify additional handlers for each topic.

A local implementation is already provided:

```python
from busline.local_client.subscriber.local_mhs import LocalMultiHandlersSubscriber

subscriber = LocalMultiHandlersSubscriber(default_event_handler=callback)

await subscriber.subscribe("t1")
await subscriber.subscribe("t2", handlers=callback)
await subscriber.subscribe("t3", handlers=[callback1, event_handler1, event_handler2, callback2])
```

Raw functions are automatically wrapped into a `ClosureEventHandler`












