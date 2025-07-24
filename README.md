from busline.client.subscriber.event_handler import CallbackEventHandler

# Busline for Python

Agnostic asynchronous pub/sub library for Python and official library for [Orbitalis](https://github.com/orbitalis-framework/py-orbitalis).

This library is fully based on `asyncio` and provided out-of-the-box a local and MQTT implementation.

In addiction, you can choose between a pair pub/sub or a client, i.e. a set of publishers and subscribers. 
Client allows you to use a _heterogeneous combination_ of pubs/subs (e.g., local + MQTT). 

Busline allows you to choose your favourite programming pattern between _callback_ and _iterator_.

## Quick start

```python
publisher = ...     # choose a publisher
subscriber = ...    # choose a subscriber

await asyncio.gather(
    publisher.connect(),
    subscriber.connect()
)

await subscriber.subscribe("your_topic", lambda t, e: print(f"New event: {t} -> {e}"))

await publisher.publish("your_topic", "hello")

# ...or

async for (topic, event) in subscriber.inbound_events:
    print(f"New event: {topic} -> {event}")
    break

# finally...
await asyncio.gather(
    publisher.disconnect(),
    subscriber.disconnect()
)
```

### Client

```python
client = (PubSubClientBuilder()
            .with_publisher(publisher)
            .with_subscriber(subscriber)
            .build())

await client.connect()

await client.publish("your-topic", "hello")
# and/or
await client.subscribe("your-topic", lambda t, e: print(f"{t} -> {e}"))

await client.disconnect()
```

### Local EventBus

```python
publisher = LocalPublisher(eventbus=LocalEventBus())
subscriber = LocalSubscriber(eventbus=LocalEventBus())
```

> [!NOTE]
> `LocalEventBus()` is a singleton and the default implementation of a local eventbus, but you can provide yours.


### MQTT

```python
publisher = MqttPublisher(hostname="127.0.0.1")
subscriber = MqttSubscriber(hostname="127.0.0.1")
```

> [!NOTE]
> Default port: `1883`
> 
> Default event serializer/deserializer: JSON


## Documentation

### Events

We have 2+1 different concepts related to events in Busline:

- `Message`: actual information that you publish
- `Event`: inbound envelope of messages, providing useful information
- `RegistryPassthroughEvent`, low-level class to manage events communication (care about it only if you want to create your custom implementation of pubs/subs)

#### Message

`Message` is the class which contains data which can be published using publishers.

We must provide `serialize` and `deserialize` methods, in order to be able to publish them.

Fortunately, Busline provides out-of-the-box a set of mixins to avoid custom implementations:

- `AvroMessageMixin` based on Avro, it uses `dataclasses_avroschema` library to work with dataclasses
- `JsonMessageMixin` based on JSON, given that `json` library is not able to serialize some types of data (e.g., `set`), you will implement `to_json/from_json` methods
- `StringMessage`, `Int64Message`, `Int32Message`, `Float32Message`, `Float64Message` to wrap primitive data

> [!NOTE]
> If you use `AvroMessageMixin` you should not use dataclass default values which are time-variant (e.g. `datetime.now()`),
> because schemas will be different.


```python
@dataclass
class MockUserCreationMessage(AvroMessageMixin):
    email: str
    password: str
```

```python
@dataclass
class MockUserCreationMessage(JsonMessageMixin):
    email: str
    password: str

    @classmethod
    @override
    def from_json(cls, json_str: str) -> Self:
        data = json.loads(json_str)

        return cls(data["email"], data["password"])

    @override
    def to_json(self) -> str:
        return json.dumps(asdict(self))
```

```python
StringMessage("hello")

Int64Message(42)

Int32Message(42)

Float32Message(3.14)

Float64Message(3.14)
```

#### Event

`Event` is the envelope for messages. It is what you will receive from subscribers.

Events can be sent also without a payload, for example if you want to notify only.

Generally, you must not care about its creation, because it is performed in subscribers logic.

- `identifier`: unique identifier of event
- `publisher_identifier`: identifier of publisher
- `payload`: message data
- `timestamp`: event generation datetime


#### Registry & RegistryPassthroughEvent

Given serialized data, we know neither serialization format nor message type.

In Busline there are **two serializations**: messages serialization and events serialization.

`EventRegistry` is a _singleton_ which helps system to retrieve right class type to instance message objects.
In particular, it stores associations `message_type => Type[Message]`.

`RegistryPassthroughEvent` represents the utility model which should be serialized by publishers based on related eventbus and
deserialized by subscribers. In addiction, it works together with `EventRegistry` to restore message class based on bytes.

Following class fields:

- `identifier: str`
- `publisher_identifier: str`
- `serialized_payload: Optional[bytes]` contains bytes produced by message (`payload` of `Event`) serialization.
- `payload_format_type: Optional[str]` states serialization format (e.g., JSON, Avro, ...)
- `message_type: Optional[str]` states "what" message is stored in bytes
- `timestamp: datetime`

`RegistryPassthroughEvent` is equipped with `from_event`/`to_event` methods 
and with `from_dict`/`to_dict` to provide its serializable data in a fancy way (they exploit `serialize`/`deserialize` methods of message payload).

`from_event` adds event message to registry automatically, in order to make it available in a second time.

`to_event` retrieves from registry right message class, then construct the event.

> [!NOTE]
> Without this process we are not able to provide you an instance of message class.

Therefore, the common steps to send an event into an eventbus and reconstruct it is:

1. Create a `Message`
2. Wrap the `Message` in an `Event`
3. Generate `RegistryPassthroughEvent` from `Event` (this adds `Message` to registry) using `from_event`
4. Serialize `RegistryPassthroughEvent`, for example using already implemented `registry_passthrough_event_json_serializer` function
5. Send serialized `RegistryPassthroughEvent` into eventbus
6. Deserialize bytes of `RegistryPassthroughEvent` (e.g., you could use `registry_passthrough_event_json_deserializer` function)
7. Reconstruct `Event` using `to_event` of `RegistryPassthroughEvent`
8. Retrieve the message thanks to `event.payload`

```python
message = MyMessage()

event = Event(message, ...)

rp_event = RegistryPassthroughEvent.from_event(event)   # new association in the registry is created

serialized_rp_event = registry_passthrough_event_json_serializer(rp_event)

# send serialized_event

rp_event = registry_passthrough_event_json_deserializer(serialized_rp_event)

event = rp_event.to_event()

message = event.payload
```

##### Add to registry manually

If you want to add an association into registry manually you can:

- Decorate a class using `@add_to_registry`
- Use `add` method of registry

```python
@dataclass
@add_to_registry
class MyMessage(AvroMessageMixin):
    pass
```

```python
event_registry = EventRegistry()    # singleton

message_type = event_registry.add(MyMessage)

# or if you want to explicit define the message type:
message_type = event_registry.add(MyMessage, message_type="my_message")
assert message_type == "my_message"
```


### Publisher

`Publisher` is the abstract class which can be implemented to create publishers.

The main method is `publish`, used to publish a message in only one topic. 
If you want to publish a message in more topics at the same time: `multi_publish`.

`publish` method takes two parameters: `topic` and `message`. 
`topic` is a string and represent the topic in which message must be published.
`message` can be `None` if you want to send a payload-empty event, otherwise you can provide:

- Implementation of `Message`
- `str` which is wrapped into `StringMessage`
- `int` which is wrapped into `Int64Message`
- `float` which is wrapped into `Float64Message`

```python
await publisher.connect()

await publisher.publish("topic", "hello")
await publisher.publish("topic", 42)
await publisher.publish("topic", 3.14)
await publisher.publish("topic", YourCustomMessage(...))

await publisher.disconnect()
```

In addiction to `topic` and `message`, `publish` can be fed using more parameters, but they depend on actual publisher implementation.

If you want to implement your publishers you must implement only `_internal_publish`, 
in which you must insert logic to send messages.

There are two additional hooks: `_on_publishing` and `_on_published`, called before and after `_internal_publish` when `publish` method is called.


Busline provides two implementations:

- `LocalPublisher`
- `MqttPublisher`

#### LocalPublisher

```python
publisher = LocalPublisher(eventbus=...)
```

You must only provide an eventbus implementation which works locally.
Busline provides `AsyncLocalEventBus`, which is wrapped in a singleton called `LocalEventBus`.

You can implement your eventbus thanks to `EventBus` abstract class.
By default, no wildcards are supported, but you can override `_topic_names_match` to change the logic.


#### MqttPublisher

```python
MqttPublisher(hostname="127.0.0.1")
```

`MqttPublisher` uses `aiomqtt` MQTT client to publish messages. The mandatory parameter is `hostname`, but you can provide also:

- `port`: (int) default `1883`
- `other_client_parameters`: key-value dictionary which is provided during `aiomqtt` MQTT client creation
- `serializer`: function to serialize events, by default JSON is used (see `RegistryPassthroughEvent` explanation)

> [!WARNING]
> You _must_ instantiate it into an `async` context (e.g., async function), otherwise an error will be raised.


### Subscriber

`Subscriber` is the abstract class which provides the base implementation for a subscriber. It has some similarities with `Publisher`.

You can subscribe to a topic using `subscribe` method and unsubscribe thanks to `unsubscribe`. 
If no topic is specified during unsubscription, subscriber unsubscribes itself from **all** topics.

`multi_subscribe` and `multi_unsubscribe` are provided.

```python
await subscriber.subscribe("topic")
# see below how to consume messages
```

If you want to manually notify a subscriber: `notify` method.

```python
subscriber.notify(
    "topic",
    Event(...)
)
```

There are two main ways to consume messages:

- **Handler**
- **Iterator**

You can also use both!

#### Handler-style

`EventHandler` represents an object which is able to handle a new event.
Busline provides two handler implementations:

- `CallbackEventHandler` to wrap a _synchronous_ or an _asynchronous_ function
- `MultiEventHandler` to wrap more than one handler (order of execution is strict if `strict_order=True`, otherwise they are executed in parallel)

```python
def sync_handler_callback(topic: str, event: Event):
    print(f"{topic} -> {event}")
    
async def async_handler_callback(topic: str, event: Event):
    print(f"{topic} -> {event}")
    
handler1 = CallbackEventHandler(sync_handler_callback)
# or
handler2 = CallbackEventHandler(async_handler_callback)

await handler1.handle(
    "topic",
    Event(...)
)

handler = MultiEventHandler([handler1, handler2])

await handler.handle(
    "topic",
    Event(...)
)
```

If you don't want to wrap every time your functions or _if you have a method_ instead, you can use our decorator: `@event_handler`.

```python
@event_handler
async def my_function(topic: str, event: Event):
    print(f"{topic} -> {event}")
```

> [!WARNING]
> You must import event_handler decorator explicitly: 
> 
> `from busline.client.subscriber.event_handler import event_handler`
> 
> This will not work:
> 
> `import busline.client.subscriber.event_handler`


`Subscriber` has `default_handler` attribute, which represents the default handler which will be used if there is not a handler related to a topic.

In addiction, when you subscribe to a topic, you can (or not) specify a handler. In case, that handler will be used to handle new events.
You can specify a `EventHandler` or a function/method (which will be wrapped into a `CallbackHandler`):

```python
subscriber = MockSubscriber(default_handler=...)

await subscriber.subscribe(test_topic2, CallbackEventHandler(lambda t, e: ...))
# or
await subscriber.subscribe(test_topic2, lambda t, e: ...)
# or
await subscriber.subscribe(test_topic2)     # will use default handler if set
```

Every new inbound event is handled using the related pre-defined handler or default (_if it was defined_).

If you want to ensure to use a handler for every topic, you must set `handler_always_required=True` attribute in subscriber.

> [!NOTE]
> If you use wildcard, you must specify a `topic_names_matcher` function in order to provide wildcards logic.
> 
> By default, a handler handles an event if its related topic and the inbound topic are _perfectly_ equal.

#### Iterator-style

If you don't like callbacks, you can use asynchronous iterators (i.e., `async for`).

Every subscriber provides you two properties:

- `inbound_events`: generator which provides you all inbound events
- `inbound_unhandled_events`: generator which provides you all inbound events which are _not handled_ by a handler

Obviously, some events can arrive both to `inbound_events` and `inbound_unhandled_events`.

```python
async for (topic, event) in subscriber.inbound_events:
    print(f"{topic} -> {event}")

async for (topic, event) in subscriber.inbound_unhandled_events:
    print(f"{topic} -> {event}")
```


#### Custom subscriber implementation

The main methods which you should implement if you want to create your subscriber are `_internal_subscribe` and `_internal_unsubscribe`,
in which must be inserted logic of subscription and unsubscription.

Remember `notify` method, this already processes every needed operations in a subscriber, therefore you should only collect remote message (from eventbus)
and call it.

#### LocalSubscriber

```python
LocalSubscriber(eventbus=LocalEventBus())
```

`LocalSubscriber` is the implementation to use a local eventbus, which must be fed during definition.

Similarly for `Publisher`, Busline already provides `AsyncLocalEventBus`, which is wrapped in a singleton called `LocalEventBus`.

#### MqttSubscriber

```python
MqttSubscriber(hostname="127.0.0.1")
```

`MqttSubscriber` is a MQTT subscriber implementation provided by Busline, based on `aiomqtt` library.

You must provide `hostname` of your MQTT broker and may provide `port` and `other_client_parameters`.

`MqttSubscriber` uses a `deserializer`, i.e. function to deserialize events, by default JSON is used (see `RegistryPassthroughEvent` explanation).

> [!WARNING]
> You _must_ instantiate it into an `async` context (e.g., async function), otherwise an error will be raised.


### PubSubClient

`PubSubClient` is a class which wraps a list of publishers and subscribers in order to provide both methods in an all-in-one object.

`PubSubClient` allows you to use _different kinds of publishers and subscribers_! 
Therefore, you can publish a message in more eventbus at the same time.

To simplify its creation, `PubSubClientBuilder` is provided.

```python
client = (PubSubClientBuilder()
            .with_publishers([
                MqttPublisher(hostname="127.0.0.1"),
                LocalPublisher(eventbus=LocalEventBus())
            ])
            .with_subscribers([
                MqttSubscriber(hostname="127.0.0.1"),
                LocalSubscriber(eventbus=LocalEventBus())
            ])
            .build())

await client.connect()

# ...

await client.disconnect()
```


