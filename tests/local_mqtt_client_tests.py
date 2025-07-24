import asyncio
import unittest
from typing import Optional

from busline.client.pubsub_client import PubSubClientBuilder
from busline.client.subscriber.event_handler import CallbackEventHandler
from busline.event.event import Event
from busline.event.message.number_message import Float64Message
from busline.local.eventbus.local_eventbus import LocalEventBus
from busline.local.local_publisher import LocalPublisher
from busline.local.local_subscriber import LocalSubscriber

from busline.mqtt.mqtt_publisher import MqttPublisher
from busline.mqtt.mqtt_subscriber import MqttSubscriber


class TestLocalAndMqttEventBus(unittest.IsolatedAsyncioTestCase):


    async def test_pubsub(self):
        test_topic = "test.topic"

        n_events = 0
        async def handler_callback(topic: str, event: Event):
            nonlocal n_events
            n_events += 1


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

        await client.publish(test_topic)

        await asyncio.sleep(1)

        self.assertEqual(n_events, 0)


        await client.subscribe(test_topic, handler_callback)

        await asyncio.sleep(1)

        await client.publish(test_topic)

        await asyncio.sleep(1)

        self.assertEqual(n_events, 2)

        await client.unsubscribe()

        await asyncio.sleep(1)

        await client.publish(test_topic)

        await asyncio.sleep(1)

        self.assertEqual(n_events, 2)

        await client.disconnect()

        await asyncio.sleep(1)
