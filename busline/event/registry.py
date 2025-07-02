from dataclasses import dataclass, field
from typing import Dict, Type
from functools import wraps
from busline.event.event import Event, EventPayload
from busline.utils.singleton import Singleton


class EventRegistry(metaclass=Singleton):
    """
    Registry to manage different event types

    Author: Nicola Ricciardi
    """

    __associations: Dict[str, Type[EventPayload]] = {}

    @property
    def associations(self) -> Dict[str, Type[EventPayload]]:
        return self.__associations

    def remove(self, event_type: str):
        """
        Remove an event type association
        """

        self.__associations.pop(event_type)

    def add(self, event_type: str, event_payload_class: Type[EventPayload]):
        """
        Add a new association between an event type and an event class
        """

        self.__associations[event_type] = event_payload_class

    def retrieve_class(self, event_type: str) -> Type[EventPayload]:
        """
        Retrieve event class of event input based on saved associations and given event type

        KeyError is raised if no association is found
        """

        return self.__associations[event_type]

    def build(self, event_type: str, format_type: str, serialized_payload: bytes) -> EventPayload:
        """
        Build EventPayload from Event, raises a KeyError if there is not the association in registry
        """

        event_class: Type[EventPayload] = self.retrieve_class(event_type)

        return event_class.deserialize(format_type, serialized_payload)



def registry(cls: Type[EventPayload]):

    event_type: str = cls.__name__

    # add event payload to registry
    reg = EventRegistry()
    reg.add(event_type, cls)

    return cls





