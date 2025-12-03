import asyncio
import unittest

from busline.client.subscriber.event_handler.callback_event_handler import CallbackEventHandler
from busline.event.message.string_message import StringMessage
from busline.local.eventbus.local_eventbus import LocalEventBus
from busline.local.local_publisher import LocalPublisher
from busline.event.event import Event
from busline.local.local_subscriber import LocalSubscriber


class TestLocalEventBus(unittest.IsolatedAsyncioTestCase):

    async def test_async_eventbus(self):

        local_eventbus_instance1 = LocalEventBus()       # singleton
        local_eventbus_instance2 = LocalEventBus()       # singleton

        self.assertIs(local_eventbus_instance1, local_eventbus_instance2)        # check singleton

        received_event = None

        def callback(t: str, e: Event):
            nonlocal received_event

            received_event = e

        subscriber = LocalSubscriber(
            eventbus=local_eventbus_instance1,
            default_handler=CallbackEventHandler(callback)
        )
        publisher = LocalPublisher(eventbus=local_eventbus_instance2)

        await subscriber.connect()
        await publisher.connect()

        await asyncio.sleep(0.5)

        await subscriber.subscribe("tests")

        await asyncio.sleep(0.5)

        event = await publisher.publish("tests")

        await asyncio.sleep(0.5)

        self.assertIs(event, received_event)

        await subscriber.unsubscribe()

        await asyncio.sleep(0.5)

        received_event = None

        event = await publisher.publish("tests")

        self.assertIs(received_event, None)

    async def test_incoming_events_queue(self):

        test_topic1 = "test-topic-1"
        test_topic2 = "test-topic-2"

        publisher = LocalPublisher(eventbus=LocalEventBus())
        subscriber = LocalSubscriber(eventbus=LocalEventBus())

        await asyncio.gather(
            publisher.connect(),
            subscriber.connect()
        )

        await asyncio.sleep(0.5)

        n_inbound_events = 0
        async def gather_inbound_events():
            nonlocal n_inbound_events
            nonlocal subscriber

            async for (topic, event) in subscriber.inbound_events:
                n_inbound_events += 1

        asyncio.create_task(
            gather_inbound_events(),
        )

        n_unhandled_events = 0
        async def gather_unhandled_events():
            nonlocal n_unhandled_events
            nonlocal subscriber

            async for (topic, event) in subscriber.inbound_unhandled_events:
                n_unhandled_events += 1

        asyncio.create_task(
            gather_unhandled_events()
        )

        await subscriber.subscribe(test_topic1)
        await subscriber.subscribe(test_topic2, lambda t, e: ...)

        await asyncio.sleep(1)

        await publisher.publish(test_topic1)
        await publisher.publish(test_topic2)

        await asyncio.sleep(1)

        self.assertEqual(n_inbound_events, 2)
        self.assertEqual(n_unhandled_events, 1)

    async def test_string_message_publish(self):
        received_message = None

        async def callback(t: str, e: Event):
            nonlocal received_message

            self.assertTrue(isinstance(e.payload, StringMessage))

            received_message = e.payload.value

        subscriber = LocalSubscriber(eventbus=LocalEventBus())
        publisher = LocalPublisher(eventbus=LocalEventBus())

        await subscriber.connect()
        await publisher.connect()

        await asyncio.sleep(0.5)

        await subscriber.subscribe("tests", handler=callback)

        await asyncio.sleep(0.5)

        message = "my message"

        event = await publisher.publish("tests", message)

        await asyncio.sleep(0.5)

        self.assertIs(received_message, message)


if __name__ == '__main__':
    unittest.main()