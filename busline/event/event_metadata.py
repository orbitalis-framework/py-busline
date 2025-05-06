import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class EventMetadata:

    timestamp: float = field(default=datetime.datetime.now(datetime.timezone.utc).timestamp())
    content_type: Optional[str] = field(default=None)