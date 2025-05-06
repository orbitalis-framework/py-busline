import unittest

from busline.client.subscriber.event_handler.closure_event_handler import ClosureEventHandler
from busline.local.eventbus.async_local_eventbus import AsyncLocalEventBus
from busline.local.eventbus.local_eventbus import LocalEventBus
from busline.local.local_pubsub_client import LocalPubSubClient
from busline.local.publisher.local_publisher import LocalEventBusPublisher
from busline.event.event import Event
from busline.local.subscriber.local_subscriber import LocalEventBusMultiHandlersSubscriber


class TestAsyncLocalEventBus(unittest.IsolatedAsyncioTestCase):

    async def test_async_eventbus(self):

        local_eventbus_instance1 = LocalEventBus()       # singleton
        local_eventbus_instance2 = LocalEventBus()       # singleton

        self.assertIs(local_eventbus_instance1, local_eventbus_instance2)        # check singleton

        event = Event()
        received_event = None

        def callback(t: str, e: Event):
            nonlocal received_event

            received_event = e

        subscriber = LocalEventBusMultiHandlersSubscriber(
            eventbus=local_eventbus_instance1,
            fallback_event_handler=ClosureEventHandler(callback)
        )
        publisher = LocalEventBusPublisher(eventbus=local_eventbus_instance2)

        await subscriber.connect()
        await publisher.connect()

        await subscriber.subscribe("test")

        await publisher.publish("test", event)

        self.assertIs(event, received_event)

        await subscriber.unsubscribe()
        received_event = None

        await publisher.publish("test", event)

        self.assertIs(received_event, None)


    async def test_local_client(self):
        received_event = None
        event = Event()

        def client_callback(topic_name: str, e: Event):
            nonlocal received_event

            received_event = e

        client = LocalPubSubClient.from_callback(client_callback)

        await client.connect()

        await client.subscribe("test")

        await client.publish("test", event)

        self.assertIs(event, received_event)

        await client.unsubscribe()
        received_event = None

        await client.publish("test", event)

        self.assertIs(received_event, None)

    async def test_mhs(self):

        received_event = 0

        def callback(t: str, e: Event):
            nonlocal received_event

            received_event += 1

        subscriber = LocalEventBusMultiHandlersSubscriber(
            fallback_event_handler=ClosureEventHandler(callback),
            eventbus=LocalEventBus()
        )

        await subscriber.connect()

        await subscriber.subscribe("t1")
        await subscriber.subscribe("t2", handler=ClosureEventHandler(callback))

        await subscriber.notify("t1", Event())

        self.assertEqual(received_event, 1)

        await subscriber.notify("t2", Event())

        self.assertEqual(received_event, 2)

        await subscriber.unsubscribe()

        await subscriber.notify("t1", Event())
        await subscriber.notify("t2", Event())

        self.assertEqual(received_event, 2)

if __name__ == '__main__':
    unittest.main()