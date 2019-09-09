import requests
from http_ping import Http_Ping
import json
import argparse
import queue
from messaging import EventHub_Connector

# arguments for script
parser = argparse.ArgumentParser(
    description="Start querying the defined endpoints")
parser.add_argument("-t", "--targetfile", help="The file containing the targets to be pinged",
                    default='C:\\Users\\brumhardadm\\Desktop\\tmp\\worker_targets.json'#, required=True
                    )
args = parser.parse_args()

# open external config file
with open(args.targetfile, 'r') as config_file:
    config_data = json.load(config_file)

# create queue that threads are writing to
# start threads
message_queue = queue.Queue()
for target in config_data['targets']:
    test = Http_Ping(target, message_queue)
    test.start_in_thread()

# write messages to event hub
handler = EventHub_Connector(config_data['EHConnectionString'])
while True:
    if not message_queue.empty():
        message = message_queue.get()
        with handler:
            handler.process(json.dumps(message))
        