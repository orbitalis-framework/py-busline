import unittest

from busline.client.subscriber.topic_subscriber.event_handler.callback_event_handler import CallbackEventHandler
from busline.local.eventbus.async_local_eventbus import AsyncLocalEventBus
from busline.local.eventbus.local_eventbus import LocalEventBus
from busline.local.local_pubsub_client import LocalPubTopicSubClientBuilder
from busline.local.publisher.local_publisher import LocalEventBusPublisher
from busline.event.event import Event
from busline.local.subscriber.local_subscriber import LocalEventBusSubscriber


class TestLocalEventBus(unittest.IsolatedAsyncioTestCase):

    async def test_async_eventbus(self):

        local_eventbus_instance1 = LocalEventBus()       # singleton
        local_eventbus_instance2 = LocalEventBus()       # singleton

        self.assertIs(local_eventbus_instance1, local_eventbus_instance2)        # check singleton

        event = Event()
        received_event = None

        def callback(t: str, e: Event):
            nonlocal received_event

            received_event = e

        subscriber = LocalEventBusSubscriber(
            eventbus=local_eventbus_instance1,
            fallback_event_handler=CallbackEventHandler(callback)
        )
        publisher = LocalEventBusPublisher(eventbus=local_eventbus_instance2)

        await subscriber.connect()
        await publisher.connect()

        await subscriber.subscribe("tests")

        await publisher.publish("tests", event)

        self.assertIs(event, received_event)

        await subscriber.unsubscribe()
        received_event = None

        await publisher.publish("tests", event)

        self.assertIs(received_event, None)

    async def test_local_client(self):
        received_event = None
        event = Event()

        def fallback_client_callback(topic_name: str, e: Event):
            nonlocal received_event

            received_event = e


        client = LocalPubTopicSubClientBuilder().with_subscriber(
            LocalEventBusSubscriber(
                eventbus=LocalEventBus(),
                fallback_event_handler=CallbackEventHandler(fallback_client_callback)
            )
        ).with_publisher(
            LocalEventBusPublisher(eventbus=LocalEventBus())
        ).build()

        await client.connect()

        await client.subscribe("tests")

        await client.publish("tests", event)

        self.assertIs(event, received_event)

        await client.unsubscribe()
        received_event = None

        await client.publish("tests", event)

        self.assertIs(received_event, None)

        test = False

        def client_callback(topic_name: str, e: Event):
            nonlocal test

            test = True

        await client.subscribe("tests", handler=CallbackEventHandler(client_callback))

        await client.publish("tests", event)

        self.assertTrue(test)


    async def test_default_builder(self):
        client = LocalPubTopicSubClientBuilder.default()

        await client.connect()

        test = False

        def client_callback(topic_name: str, e: Event):
            nonlocal test

            test = True

        await client.subscribe("tests", handler=CallbackEventHandler(client_callback))

        await client.publish("tests", Event())

        self.assertTrue(test)


    async def test_mhs(self):

        received_event = 0

        def callback(t: str, e: Event):
            nonlocal received_event

            received_event += 1

        subscriber = LocalEventBusSubscriber(
            fallback_event_handler=CallbackEventHandler(callback),
            eventbus=LocalEventBus()
        )

        await subscriber.connect()

        await subscriber.subscribe("t1")
        await subscriber.subscribe("t1")
        await subscriber.subscribe("t2", handler=CallbackEventHandler(callback))
        await subscriber.subscribe("t2", handler=CallbackEventHandler(callback))

        await subscriber.notify("t1", Event())

        self.assertEqual(received_event, 1)

        await subscriber.notify("t2", Event())

        self.assertEqual(received_event, 2)

        await subscriber.unsubscribe()
        await subscriber.unsubscribe()

        await subscriber.notify("t1", Event())
        await subscriber.notify("t2", Event())

        self.assertEqual(received_event, 2)




if __name__ == '__main__':
    unittest.main()