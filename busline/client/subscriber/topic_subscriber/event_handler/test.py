import unittest

from busline.client.subscriber.topic_subscriber.event_handler import event_handler, schemafull_event_handler
from busline.event.event import Event


class TestEventRegistry(unittest.IsolatedAsyncioTestCase):

    async def test_event_handler_decorator(self):

        test = False

        @event_handler
        async def func_event_handler(topic: str, event: Event):
            nonlocal test
            test = True

        @schemafull_event_handler({ "test": "test" })
        async def schema_func_event_handler(topic: str, event: Event):
            nonlocal test
            test = True


        await func_event_handler.handle("test", Event())

        self.assertTrue(test)

        test = False

        await schema_func_event_handler.handle("test", Event())

        self.assertTrue(test)

        self.assertEqual(schema_func_event_handler.input_schema()["test"], "test")


    async def test_method_event_handler_decorator(self):

        class Dummy:

            def __init__(self):
                self.test = False

            @event_handler
            async def operation1(self, topic: str, event: Event):
                self.test = True

            @schemafull_event_handler({ "test": "test" })
            async def operation2(self, topic: str, event: Event):
                self.test = True

        dummy = Dummy()

        handler = dummy.operation1
        await handler.handle("test", Event())
        self.assertTrue(dummy.test)

        dummy.test = False

        await dummy.operation1.handle("test", Event())
        self.assertTrue(dummy.test)

        dummy.test = False

        await dummy.operation2.handle("test", Event())
        self.assertTrue(dummy.test)

        self.assertEqual(dummy.operation2.input_schema()["test"], "test")
