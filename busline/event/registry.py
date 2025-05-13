from dataclasses import dataclass, field
from typing import Dict, Type

from busline.event.event import Event

class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class EventRegistry(metaclass=_Singleton):
    """
    Registry to manage different event types

    Author: Nicola Ricciardi
    """

    associations: Dict[str, Type[Event]] = field(default_factory=dict)

    def unregister(self, event_type: str):
        """
        Remove an event type association
        """

        self.associations.pop(event_type)

    def register(self, event_type: str, event_class: Type[Event]):
        """
        Add a new association between an event type and an event class
        """

        self.associations[event_type] = event_class

    def retrive_class(self, event) -> Type[Event]:
        """
        Retrive event class of event input based on saved associations and given event type

        KeyError is raised if no association is found
        """

        return self.associations[event.event_type]

    def convert(self, event: Event, raise_on_miss: bool = True) -> Event:
        """
        Convert a generic event, auto-building the right event class based on event type.

        If raise_on_miss=True, a KeyError exception is raised. Otherwise, input is returned in output.
        """

        if event.event_type not in self.associations and not raise_on_miss:
            return event

        event_class: Type[Event] = self.retrive_class(event)

        return event_class.from_event(event)







