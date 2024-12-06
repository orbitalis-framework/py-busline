import unittest
from busline.client.eventbus_client import EventBusClient
from busline.local_client.local_eventbus_client import LocalEventBusClient
from busline.local_client.publisher.local_eventbus_publisher import LocalEventBusPublisher
from busline.event.event import Event
from busline.client.subscriber.listener.closure_event_handler import ClosureEventHandler
from busline.local_client.subscriber.local_eventbus_closure_subscriber import LocalEventBusClosureSubscriber


class TestLocalEventBusClient(unittest.IsolatedAsyncioTestCase):

    async def test_raw_client(self):
        received_event = None

        event = Event()

        def subscriber_callback(topic_name: str, e: Event):
            print(f"subscriber event received: {e}")

        def client_callback(topic_name: str, e: Event):
            nonlocal received_event

            received_event = e

        subscriber = LocalEventBusClosureSubscriber(subscriber_callback)
        publisher = LocalEventBusPublisher()

        client = EventBusClient(publisher, subscriber, ClosureEventHandler(client_callback))

        await client.subscribe("test")

        await client.publish("test", event)

        self.assertIs(event, received_event)

        await client.unsubscribe()
        received_event = None

        await client.publish("test", event)

        self.assertIs(received_event, None)


    async def test_local_client(self):
        received_event = None
        event = Event()

        def client_callback(topic_name: str, e: Event):
            nonlocal received_event

            received_event = e

        client = LocalEventBusClient(client_callback)

        await client.subscribe("test")

        await client.publish("test", event)

        self.assertIs(event, received_event)

        await client.unsubscribe()
        received_event = None

        await client.publish("test", event)

        self.assertIs(received_event, None)

if __name__ == '__main__':
    unittest.main()