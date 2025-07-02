from __future__ import annotations

import uuid
import datetime
from dataclasses import dataclass, field
from typing import Optional, Generic, TypeVar
from abc import ABC
from collections.abc import Buffer
from busline.utils.serde import SerdableMixin


@dataclass(frozen=True)
class EventPayload(SerdableMixin, ABC):
    """
    Event payload for an event, it must be serializable and deserializable

    Author: Nicola Ricciardi
    """

    def into_event(self, /, **kwargs) -> Event:
        return Event(
            payload=self,
            **kwargs
        )


P = TypeVar('P', bound='EventPayload')

@dataclass(frozen=True, kw_only=True)
class Event(Generic[P]):
    """
    Event publishable in an eventbus

    Author: Nicola Ricciardi
    """

    identifier: str = field(default_factory=lambda: str(uuid.uuid4()))
    payload: Optional[P] = field(default=None)
    event_type: Optional[str] = field(default=None)
    timestamp: float = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).timestamp())
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.event_type is None and self.payload is not None:
            object.__setattr__(self, 'event_type', self.payload.__class__.__name__)
