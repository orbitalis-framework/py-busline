import json
from abc import ABC, abstractmethod
from typing import Dict, List

from busline.client.subscriber.event_handler.event_handler import EventHandler


class SchemafullEventHandler(EventHandler, ABC):

    @abstractmethod
    def input_schemas(self) -> List[Dict]:
        raise NotImplemented()

    def schemas_fingerprints(self) -> List[str]:
        fingerprints: List[str] = []
        for schema in self.input_schemas():
            fingerprints.append(str(hash(json.dumps(schema, sort_keys=True))))

        return fingerprints