import unittest
from typing import Type

from busline.event.event import Event
from busline.event.registry import EventRegistry


class Event1(Event):
    def my_value1(self) -> int:
        return self.content

class Event2(Event):
    def my_value2(self) -> int:
        return self.content

class TestEventRegistry(unittest.TestCase):

    def test(self):

        event_registry = EventRegistry()    # singleton

        event_registry.register("event1", Event1)
        event_registry.register("event2", Event2)

        event_registry = EventRegistry()  # singleton

        generic_event1 = Event(content=1, event_type="event1")
        generic_event2 = Event(content=2, event_type="event2")
        generic_unknown_event = Event(content=2, event_type="unknown")

        event1: Event1 = event_registry.convert(generic_event1)

        self.assertEqual(event1.event_type, "event1")
        self.assertEqual(event1.my_value1(), 1)

        event2_class = event_registry.retrive_class(generic_event2)

        self.assertIs(event2_class, Event2)

        event2_class: Type[Event2] = event2_class

        event2 = event2_class.from_event(generic_event2)

        self.assertEqual(event2.event_type, "event2")
        self.assertEqual(event2.my_value2(), 2)

        self.assertRaises(KeyError, lambda: event_registry.retrive_class(generic_unknown_event))