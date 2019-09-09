import requests
from Http_Ping import Http_Ping
import json
import argparse
import queue

parser = argparse.ArgumentParser(
    description="Start querying the defined endpoints")
parser.add_argument("-t", "--targetfile", help="The file containing the targets to be pinged",
                    default='C:\\Users\\brumhard\\Desktop\\tmp\\worker_targets.json'#, required=True
                    )
args = parser.parse_args()

with open(args.targetfile, 'r') as config_file:
    config_data = json.load(config_file)

message_queue = queue.Queue()

for target in config_data['targets']:
    test = Http_Ping(target, message_queue)
    test.start_in_thread()

while True:
    if not message_queue.empty():
        message = message_queue.get()
        print(json.dumps(message))