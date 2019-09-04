import requests

# verify false should not be used in prod
# instead use path to cert file (https://2.python-requests.org/en/master/user/advanced/#ssl-cert-verification)
x = requests.get("https://www.google.com/", verify = False)
send_time = x.headers['date']
print(send_time)