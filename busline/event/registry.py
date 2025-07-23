from typing import Dict, Type, Optional

from busline.event.message.message import Message
from busline.utils.singleton import Singleton


class EventRegistry(metaclass=Singleton):
    """
    Registry to manage different message types

    Author: Nicola Ricciardi
    """

    __associations: Dict[str, Type[Message]] = {}

    @property
    def associations(self) -> Dict[str, Type[Message]]:
        return self.__associations

    @classmethod
    def class_to_type(cls, message_class: Type[Message]) -> str:
        return message_class.__name__

    @classmethod
    def obj_to_type(cls, message: Message) -> str:
        return type(message).__name__

    def remove(self, *, message_type: Optional[str] = None, message_class: Optional[Type[Message]] = None):
        """
        Remove a message type association

        ValueError is raised if neither message_type nor message_class is provided
        """

        if message_class is None and message_type is None:
            raise ValueError("Neither message_type nor message_class is provided")

        if message_type is None:
            message_type = EventRegistry.class_to_type(message_class)

        self.__associations.pop(message_type)

    def add(self, message_class: Type[Message], *, message_type: Optional[str] = None) -> str:
        """
        Add a new association between an event message and message class.

        Return message type
        """

        if message_type is None:
            message_type = EventRegistry.class_to_type(message_class)

        self.__associations[message_type] = message_class

        return message_type

    def retrieve_class(self, message_type: str) -> Type[Message]:
        """
        Retrieve message class

        KeyError is raised if no association is found.
        """

        return self.__associations[message_type]



def add_to_registry(cls: Type[Message]):

    # add event message in registry
    reg = EventRegistry()
    reg.add(cls)

    return cls



