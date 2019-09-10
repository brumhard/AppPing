from azure.eventhub.aio import EventHubClient
from azure.eventhub import EventData
import logging
import json
import asyncio


class EventHub_Connector():
    def __init__(self, connection_string):
        self._client = EventHubClient.from_connection_string(connection_string)

    def __enter__(self):
        self._producer = self._client.create_producer(partition_id="0")

    def __exit__(self, type, value, traceback):
        self._producer.close()

    async def process(self, message):
        try:
            print(f"Sending Message: {message}")
            await self._producer.send(EventData(message))
        except:
            raise


class Async_EventHub_Connector():
    def __init__(self, connection_string):
        self._client = EventHubClient.from_connection_string(connection_string)
        self._close = False

    def __enter__(self):
        self._event_loop = asyncio.get_event_loop()
        self._producer = self._client.create_producer(partition_id="0")

    async def aexit(self):
        await self._producer.close()

    def __exit__(self, type, value, traceback):
        self._close = True
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.aexit())
        loop.close()

    async def _messaging_loop(self, queue):
        # write messages to event hub
        while True and not self._close:
            if not queue.empty():
                message = queue.get()
                logging.info(f"queue size: {queue.qsize()}")
                logging.info(f"Sending Message: {message}")
                await self._producer.send(EventData(json.dumps(message)))

    def process_messages(self, queue):
        # self._event_loop.create_task(self._messaging_loop(queue))
        self._event_loop.run_until_complete(self._messaging_loop(queue))
