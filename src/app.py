import requests
from http_ping import Http_Ping
import json
import argparse
import queue
import logging
from messaging import Async_EventHub_Connector

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

handler = Async_EventHub_Connector(config_data['EHConnectionString'])
with handler:
    handler.process_messages(message_queue)



        