from datetime import datetime
from bitshares.bitshares import BitShares
from bitshares.blockchain import Blockchain
from flask_socketio import SocketIO
from .database import TestBlock
import redis
namespace = "/status"
room = "test"
socketio = SocketIO(message_queue='redis://')
testnet = BitShares(node="wss://testnet.bitshares.eu/ws")


def run():
    chain = Blockchain(mode="head", bitshares_instance=testnet)
    print(chain.bitshares.rpc.url)
    for block in chain.blocks():
        timestamp = int(datetime.strptime(block["timestamp"], '%Y-%m-%dT%H:%M:%S').timestamp())
        num_ops = sum([len(tx["operations"]) for tx in block["transactions"]])
        num_txs = len(block["transactions"])
        TestBlock(timestamp, num_txs, num_ops)
        notice = {
            "timestamp": timestamp,
            "num_transactions": num_txs,
            "num_operations": num_ops,
        }
        print(notice)
        socketio.emit(
            'notice',
            notice,
            namespace=namespace,
            room=room,
            broadcast=True)


if __name__ == "__main__":
    run()
