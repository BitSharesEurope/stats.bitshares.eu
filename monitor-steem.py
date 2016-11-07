from steemapi.steemnoderpc import SteemNodeRPC
from flask_socketio import SocketIO
import redis
import json
from collections import deque
import re
import time
from pprint import pprint

windowLength = 1200
numtxs = deque([0] * windowLength, windowLength)
namespace = "/status"
room = "steem"
print("Serving room: " + room, flush=True)

client = SteemNodeRPC("wss://this.piston.rocks")
socketio = SocketIO(message_queue='redis://')
blockInterval = 3

for block in client.block_stream(mode="head"):
    notice = client.get_dynamic_global_properties()

    witness = client.get_witness_by_account(block["witness"])
    account = client.get_account(witness["owner"])
    notice["num_transactions"] = len(block["transactions"])
    notice["next_maintenance_time"] = "n/a"
    numtxs.appendleft(len(block["transactions"]))

    tps = {}
    for span in [15, 30, 60, 5 * 60, 60 * 60]:
        numBlocks = int(span / blockInterval)
        tps["span-%d" % span] = "%.3f" % (
            sum([numtxs[a] for a in range(0, numBlocks)]) / float(span)
        )
    notice["tps"] = tps

    socketio.emit('block',
                  notice,
                  namespace=namespace,
                  room=room,
                  broadcast=True)
    socketio.emit('witness',
                  {"witness": witness, "account": account},
                  namespace=namespace,
                  room=room,
                  broadcast=True)
