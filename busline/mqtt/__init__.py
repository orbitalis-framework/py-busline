import logging
from abc import ABC
from dataclasses import dataclass, field
from typing import override, Any, Dict
from aiomqtt import Client

from busline.client.eventbus_connector import EventBusConnector


@dataclass(kw_only=True)
class _MqttClientWrapper(EventBusConnector, ABC):

    hostname: str
    port: int = field(default=1883)
    other_client_parameters: Dict = field(default_factory=dict)
    _internal_client: Client = field(default=None, init=False)
    __context: Any = field(init=False)


    def __post_init__(self):
        self._internal_client = Client(
            hostname=self.hostname,
            port=self.port,
            identifier=self.identifier,
            **self.other_client_parameters
        )

    @override
    async def connect(self):
        logging.info(f"{self}: connecting...")

        if self._internal_client is None:
            raise ValueError("Internal client is not set")

        # open context, equivalent to "async with"
        self.__context = self._internal_client.__aenter__()
        await self.__context

    @override
    async def disconnect(self):
        logging.info(f"{self}: disconnecting...")

        # close context
        await self._internal_client.__aexit__(None, None, None)
        self.__context = None


