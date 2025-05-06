# Busline for Python

Agnostic eventbus for Python.

Official eventbus library for [Orbitalis](https://github.com/orbitalis-framework/py-orbitalis)

## Get Start

### Local EventBus

#### Using Publisher/Subscriber

```python
local_eventbus_instance1 = LocalEventBus()       # singleton
local_eventbus_instance2 = LocalEventBus()       # singleton

subscriber = LocalEventBusMultiHandlersSubscriber(
    eventbus=local_eventbus_instance1,
    fallback_event_handler=ClosureEventHandler(lambda t, e: print(t, e))
)
publisher = LocalEventBusPublisher(eventbus=local_eventbus_instance2)

await subscriber.connect()
await publisher.connect()

await subscriber.subscribe("topic-name")

await publisher.publish("topic-name", Event())  # publish empty event

# ...subscriber receives Event()

await subscriber.disconnect()
await publisher.disconnect()
```

#### Using EventBusClient

```python
client = LocalPubSubClient.from_callback(lambda t, e: print(t, e))
# NOTE: both publisher and subscriber will use singleton local eventbus

await client.connect()

await client.subscribe("topic-name")

await client.publish("topic-name", Event())  # publish empty event

# ...client receives Event()

await client.disconnect()
```

#### MultiClient

```python
local_eventbus_instance1 = AsyncLocalEventBus()  # not singleton
local_eventbus_instance2 = AsyncLocalEventBus()  # not singleton

client1 = LocalPubSubClient.from_callback(
    lambda t, e: ...,
    eventbus=local_eventbus_instance1
)

client2 = LocalPubSubClient.from_callback(
    lambda t, e: ...,
    eventbus=local_eventbus_instance2
)

multi_client = EventBusMultiClient([
    client1,
    client2
])

await multi_client.connect()

await multi_client.subscribe("topic-name", handler=ClosureEventHandler(on_event_callback))

await multi_client.publish("topic-name", Event())

# ...both clients receive Event() and handle it using `on_event_callback`

await multi_client.disconnect()
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
class YourEventBusPublisher(Publisher):

    async def _internal_publish(self, topic_name: str, event: Event, **kwargs):
        pass  # send events to your eventbus (maybe in cloud?)
```

```python
class YourEventBusSubscriber(Subscriber):

    async def on_event(self, topic_name: str, event: Event, **kwargs):
        pass  # receive your events
```

You could create a client to allow components to use it instead of become a publisher or subscriber.

```python
subscriber = YourEventBusSubscriber(...)
publisher = YourEventBusPublisher(...)

client = PubSubClient(publisher, subscriber)
```


## Subscriber

`Subscriber` is the component which receives events. It is a `EventHandler`, therefore it has `on_event` method in which 
every event (and related topic) is passed.

### MultiHandlerSubscriber

`MultiHandlerSubscriber` is an enhanced subscriber which manages an handler for each topic. We can specify a _fallback handler_,
which is run if no handler is spefied for a subscribed topic.

If the subscriber is not subscribed to a topic, fallback handler is not called.

A local implementation is already provided:

```python
subscriber = LocalMultiHandlersSubscriber(fallback_event_handler=...)

await subscriber.subscribe("t1")
await subscriber.subscribe("t2", handler=...)
```












