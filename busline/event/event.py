import json
import uuid
from typing import Any, Self
import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Event:
    """
    Event publishable in an eventbus

    Author: Nicola Ricciardi
    """

    identifier: str = field(default=str(uuid.uuid4()))
    content: Any = field(default=None)
    content_type: Optional[str] = field(default=None)
    event_type: Optional[str] = field(default=None)
    timestamp: float = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).timestamp())
    metadata: dict = field(default_factory=dict)

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        return cls(**json.loads(json_str))