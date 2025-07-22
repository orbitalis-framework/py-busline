import asyncio
import unittest

from busline.client.pubsub_client import PubSubClient, PubSubClientBuilder
from busline.client.subscriber.event_handler import CallbackEventHandler
from busline.event.event import Event

from busline.mqtt.mqtt_publisher import MqttPublisher
from busline.mqtt.mqtt_subscriber import MqttSubscriber


class TestLocalEventBus(unittest.IsolatedAsyncioTestCase):


    async def test_pubsub(self):
        test_topic = "test-topic"

        n_events = 0
        async def handler_callback(topic: str, event: Event):
            nonlocal n_events
            n_events += 1


        client = (PubSubClientBuilder()
                    .with_publisher(MqttPublisher(hostname="127.0.0.1"))
                    .with_subscriber(MqttSubscriber(hostname="127.0.0.1"))
                    .build())

        await client.connect()

        await client.publish(test_topic)

        await asyncio.sleep(1)

        self.assertEqual(n_events, 0)


        await client.subscribe(test_topic, handler_callback)

        await asyncio.sleep(1)

        await client.publish(test_topic)

        await asyncio.sleep(1)

        self.assertEqual(n_events, 1)

        await client.subscribe(test_topic)

        await asyncio.sleep(1)

        client.subscribers[0].default_handler = CallbackEventHandler(handler_callback)

        await client.publish(test_topic)

        await asyncio.sleep(1)

        self.assertEqual(n_events, 2)

    async def test_incoming_events_queue(self):

        test_topic1 = "test-topic-1"
        test_topic2 = "test-topic-2"

        publisher = MqttPublisher(hostname="127.0.0.1")
        subscriber = MqttSubscriber(hostname="127.0.0.1")

        await asyncio.gather(
            publisher.connect(),
            subscriber.connect()
        )

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

        await asyncio.sleep(2)

        self.assertEqual(n_inbound_events, 2)
        self.assertEqual(n_unhandled_events, 1)




if __name__ == '__main__':
    unittest.main()