import datetime
import unittest

from busline.client.subscriber.event_handler import event_handler, CallbackEventHandler
from busline.client.subscriber.event_handler.multi_handler import MultiEventHandler
from busline.event.event import Event


class TestEventRegistry(unittest.IsolatedAsyncioTestCase):

    async def test_event_handler_decorator(self):

        test = False

        @event_handler
        async def func_event_handler(topic: str, event: Event):
            nonlocal test
            test = True


        await func_event_handler.handle("tests", Event(
            identifier="id",
            publisher_identifier="pub-id",
            timestamp=datetime.datetime.now(),
            payload=None
        ))

        self.assertTrue(test)

    async def test_multi_handler(self):

        n_events = 0

        def sync_handler_callback(topic: str, event: Event):
            nonlocal n_events
            n_events += 1

        async def async_handler_callback(topic: str, event: Event):
            nonlocal n_events
            n_events += 1

        handler = MultiEventHandler([
            CallbackEventHandler(sync_handler_callback),
            CallbackEventHandler(async_handler_callback),
        ], strict_order=False)


        await handler.handle("tests", Event(
            identifier="id",
            publisher_identifier="pub-id",
            timestamp=datetime.datetime.now(),
            payload=None
        ))

        self.assertEqual(n_events, 2)


    async def test_method_event_handler_decorator(self):

        class Dummy:

            def __init__(self):
                self.test = False

            @event_handler
            async def operation1(self, topic: str, event: Event):
                self.test = True

        dummy = Dummy()

        handler = dummy.operation1
        await handler.handle("tests", Event(
            identifier="id",
            publisher_identifier="pub-id",
            timestamp=datetime.datetime.now(),
            payload=None
        ))

        self.assertTrue(dummy.test)

        dummy.test = False

        await dummy.operation1.handle("tests", Event(
            identifier="id",
            publisher_identifier="pub-id",
            timestamp=datetime.datetime.now(),
            payload=None
        ))

        self.assertTrue(dummy.test)
