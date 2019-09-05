import requests
import time
from datetime import datetime
#dev:
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.


class Http_Ping:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def start(self):
        session = requests.session()

        # verify false should not be used in prod
        # instead use path to cert file (https://2.python-requests.org/en/master/user/advanced/#ssl-cert-verification)
        session.verify = False
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        while True:
            begin = datetime.utcnow()
            
            response = session.get(self.connection_string)

            now = datetime.utcnow()
            # date header should not be used as is doesn't include milliseconds und GMT instead of UTC
            # send_time = datetime.strptime(response.headers['date'], '%a, %d %b %Y %X %Z')
            # send_time = send_time.astimezone(pytz.utc)
            
            time_delta = (now - begin).total_seconds()
            # print("\nbegin:{0}, end: {1}".format(begin, now))
            print("time consumed: {}\tStatus: {}".format(time_delta, response.status_code))
            time.sleep(0.5)