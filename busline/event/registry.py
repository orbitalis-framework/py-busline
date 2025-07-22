from typing import Dict, Type

from busline.utils.singleton import Singleton

from busline.event.message import Message


class EventRegistry(metaclass=Singleton):
    """
    Registry to manage different message types

    Author: Nicola Ricciardi
    """

    __associations: Dict[str, Type[Message]] = {}

    @property
    def associations(self) -> Dict[str, Type[Message]]:
        return self.__associations

    def remove(self, message_type: str):
        """
        Remove a message type association
        """

        self.__associations.pop(message_type)

    def add(self, message_type: str, message_class: Type[Message]):
        """
        Add a new association between an event message and message class
        """

        self.__associations[message_type] = message_class

    def retrieve_class(self, message_type: str) -> Type[Message]:
        """
        Retrieve message class

        KeyError is raised if no association is found
        """

        return self.__associations[message_type]



def add_to_registry(cls: Type[Message]):

    message_type: str = cls.__name__

    # add event message in registry
    reg = EventRegistry()
    reg.add(message_type, cls)

    return cls



