import requests
import time
from datetime import datetime
import threading
import json
# dev:
from urllib3.exceptions import InsecureRequestWarning


class Http_Ping:
    def __init__(self, connection_string, output_queue):
        self.connection_string = connection_string

        self._output_queue = output_queue

    def __enter__(self):
        self._session = requests.session()

    def __exit__(self, type, value, traceback):
        self._session.close()

    def _send_request(self):
        begin = datetime.utcnow()
        response = self._session.get(self.connection_string)
        now = datetime.utcnow()

        time_delta = (now - begin).total_seconds()

        info_obj = {"TimeStamp": begin.isoformat(), "TimeTaken": time_delta,
                    "Status": response.status_code, "Target": self.connection_string}
        #info_json = json.dumps(info_obj)

        self._output_queue.put(info_obj)
        # print(info_json)

    def _start(self):
        while True:
            self._send_request()
            time.sleep(0.5)

    def start_in_thread(self):
        client_thread = threading.Thread(target=self._start)
        client_thread.daemon = True
        client_thread.start()
