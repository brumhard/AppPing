import requests
import time

class Http_Ping:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def start(self):
        # verify false should not be used in prod
        # instead use path to cert file (https://2.python-requests.org/en/master/user/advanced/#ssl-cert-verification)
        session = requests.session()
        session.verify = False
        while True:
            response = session.get(self.connection_string)
            http_time = response.headers['date']
            print(http_time)
            time.sleep(1)