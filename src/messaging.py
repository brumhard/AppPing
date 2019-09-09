from azure.eventhub import EventHubClient
from azure.eventhub import EventData
import logging

class EventHub_Connector():
    def __init__(self, connection_string):
        self._client = EventHubClient.from_connection_string(connection_string)

    def __enter__(self):
        self._producer = self._client.create_producer(partition_id="0")
    
    def __exit__(self, type, value, traceback):
        self._producer.close()

    def process(self, message):
        try:
            self._producer.send(EventData(message))
        except:
            raise