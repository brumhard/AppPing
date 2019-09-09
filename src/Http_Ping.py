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
        self._session = requests.session()
        self._output_queue = output_queue

        # verify false should not be used in prod
        # instead use path to cert file (https://2.python-requests.org/en/master/user/advanced/#ssl-cert-verification)
        self._session.verify = False
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)

    def _send_request(self):
        begin = datetime.utcnow()
        response = self._session.get(self.connection_string)
        now = datetime.utcnow()

        time_delta = (now - begin).total_seconds()

        info_obj = {"TimeStamp": begin.isoformat(), "TimeTaken": time_delta,
                    "Status": response.status_code, "Target": self.connection_string}
        #info_json = json.dumps(info_obj)

        self._output_queue.put(info_obj)
        #print(info_json)

    def _start(self):
        while True:
            self._send_request()
            time.sleep(0.5)

    def start_in_thread(self):
        client_thread = threading.Thread(target=self._start)
        client_thread.daemon = True
        client_thread.start()
