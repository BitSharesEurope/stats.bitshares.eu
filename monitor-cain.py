from grapheneapi import GrapheneClient, GrapheneWebsocketProtocol
from graphenebase import Memo, PrivateKey, PublicKey
from flask_socketio import SocketIO
import redis
import json
from collections import deque
import re

windowLength = 1200
numtxs = deque([0] * windowLength, windowLength)
namespace = "/status"


class Config(GrapheneWebsocketProtocol):
    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.socketio = SocketIO(message_queue='redis://')
        self.chain_properties = client.ws.get_global_properties()
        self.lastblock = 0

    def onPropertiesChange(self, data):
        self.chain_properties = data

    def onBlock(self, notice):
        if notice["head_block_number"] <= self.lastblock:
            return
        self.lastblock = notice["head_block_number"]

        print("new block %d" % notice["head_block_number"])
        witness = client.ws.get_account(notice["current_witness"])
        account = client.ws.get_account(witness["witness_account"])
        block = client.ws.get_block(notice["head_block_number"])

        notice["num_transactions"] = len(block["transactions"])
        numtxs.appendleft(len(block["transactions"]))

        blockInterval = self.chain_properties["parameters"]["block_interval"]
        tps = {}
        for span in [15, 30, 60, 5 * 60, 60 * 60]:
            numBlocks = int(span / blockInterval)
            tps["span-%d" % span] = "%.3f" % (
                sum([numtxs[a] for a in range(0, numBlocks)]) /
                float(span) /
                blockInterval
            )
        notice["tps"] = tps

        self.socketio.emit('block',
                           notice,
                           namespace=namespace,
                           room=room,
                           broadcast=True)
        self.socketio.emit('witness',
                           {"witness": witness, "account": account},
                           namespace=namespace,
                           room=room,
                           broadcast=True)


config = Config
m = re.search('monitor-(.*).py', __file__)
room = m.group(1)

print("Serving room: " + room)

if room == "gph":
    config.witness_url = "ws://localhost:8090/"
elif room == "bts":
    config.witness_url = "wss://bitshares.openledger.info/ws"
elif room == "test":
    config.witness_url = "ws://testnet.bitshares.eu:11011/"

client = GrapheneClient(config)
client.run()
