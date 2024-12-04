from datetime import timezone
import datetime


def utc_timestamp() -> float:
    dt = datetime.datetime.now(timezone.utc)

    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    return utc_timestamp


class EventMetadata:

    def __init__(self, timestamp: float = utc_timestamp(), **extra: dict):
        self.__timestamp = timestamp
        self.__extra = extra

    @property
    def timestamp(self) -> float:
        return self.__timestamp

    @property
    def extra(self) -> dict:
        return self.__extra
