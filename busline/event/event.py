import json
import uuid
from typing import Any
from busline.event.event_metadata import EventMetadata


class Event:
    """
    Base component of eventbus

    Author: Nicola Ricciardi
    """

    def __init__(self, content: Any = None, content_type: str = "raw", metadata: EventMetadata = EventMetadata()):

        self._identifier = str(uuid.uuid4())
        self._content = content
        self._metadata = metadata
        self._content_type = content_type


    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def content(self) -> Any:
        return self._content

    @property
    def content_type(self) -> str:
        return self._content_type

    @property
    def metadata(self) -> EventMetadata:
        return self._metadata

    def to_json(self) -> str:
        return json.dumps({
            "identifier": self.identifier,
            "content": self.content,
            "content_type": self.content_type,
            "metadata": self.metadata
        })

    @staticmethod
    def from_json(json_str: str):
        return Event(**json.loads(json_str))