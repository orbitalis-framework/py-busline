import asyncio
import logging
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from busline.event.event import Event
from busline.eventbus.eventbus import EventBus


MAX_WORKERS = 3
MAX_QUEUE_SIZE = 0


class QueuedLocalEventBus(EventBus):
    """
    Queued local eventbus (singleton). It uses a queue to store and forward events.

    Author: Nicola Ricciardi
    """

    def __init__(self, max_queue_size=MAX_QUEUE_SIZE, n_workers=MAX_WORKERS):

        super().__init__()

        self.__queue = Queue(maxsize=max_queue_size)
        self.__n_workers = n_workers

        self.__tpool = ThreadPoolExecutor(max_workers=self.__n_workers)

        for i in range(self.__n_workers):
            self.__tpool.submit(self.__elaborate_queue)

    async def put_event(self, topic_name: str, event: Event):
        self.__queue.put((topic_name, event))

    def __elaborate_queue(self):

        while True:

            topic_name, event = self.__queue.get()

            topic_subscriptions = self.subscriptions.get(topic_name, [])

            logging.debug(
                f"new event {event} on topic {topic_name}, notify subscribers: {topic_subscriptions}")

            if len(topic_subscriptions) == 0:
                return

            for subscriber in topic_subscriptions:
                asyncio.run(subscriber.on_event(topic_name, event))
