import json
from dataclasses import dataclass, field
import uuid
from typing import Any
from busline.event.event_metadata import EventMetadata


@dataclass(frozen=True)
class Event:
    """
    Event sendable in an eventbus

    Author: Nicola Ricciardi
    """

    identifier: str = field(default=str(uuid.uuid4()))
    content: Any = field(default=None)
    metadata: EventMetadata = field(default=EventMetadata())

    @staticmethod
    def from_json(json_str: str) -> 'Event':
        return Event(**json.loads(json_str))