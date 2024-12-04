import unittest
from busline.eventbus.async_local_eventbus import AsyncLocalEventBus
from busline.eventbus_client.publisher.local_eventbus_publisher import LocalEventBusPublisher
from busline.event.event import Event
from busline.eventbus_client.subscriber.local_eventbus_closure_subscriber import LocalEventBusClosureSubscriber


class TestAsyncLocalEventBus(unittest.IsolatedAsyncioTestCase):

    async def test_async_eventbus(self):

        local_eventbus_instance = AsyncLocalEventBus()       # singleton
        local_eventbus_instance2 = AsyncLocalEventBus()       # singleton

        self.assertIs(local_eventbus_instance, local_eventbus_instance2)        # check singleton

        event = Event()
        received_event = None

        def callback(t: str, e: Event):
            nonlocal received_event

            received_event = e

        subscriber = LocalEventBusClosureSubscriber(local_eventbus_instance, callback)
        publisher = LocalEventBusPublisher(local_eventbus_instance2)

        await subscriber.subscribe("test")

        await publisher.publish("test", event)

        self.assertIs(event, received_event)

        await subscriber.unsubscribe()
        received_event = None

        await publisher.publish("test", event)

        self.assertIs(received_event, None)


if __name__ == '__main__':
    unittest.main()