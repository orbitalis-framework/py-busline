import unittest
from busline.event.event import Event
from busline.local_client.subscriber.local_mhs import LocalMultiHandlersSubscriber


class TestMHS(unittest.IsolatedAsyncioTestCase):

    async def test_mhs(self):

        received_event = 0

        def callback(t: str, e: Event):
            nonlocal received_event

            received_event += 1

        subscriber = LocalMultiHandlersSubscriber(default_event_handler=callback)

        await subscriber.subscribe("t1")
        await subscriber.subscribe("t2", handlers=callback)

        await subscriber.on_event("t1", Event())

        self.assertEqual(received_event, 1)

        await subscriber.on_event("t2", Event())

        self.assertEqual(received_event, 3)

        await subscriber.unsubscribe()

        await subscriber.on_event("t1", Event())
        await subscriber.on_event("t2", Event())

        self.assertEqual(received_event, 5)

        subscriber.default_event_handler = None

        await subscriber.on_event("t1", Event())
        await subscriber.on_event("t2", Event())

        self.assertEqual(received_event, 5)




if __name__ == '__main__':
    unittest.main()