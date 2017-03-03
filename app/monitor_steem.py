from datetime import datetime
from steem import Steem
from steem.blockchain import Blockchain
from flask_socketio import SocketIO
from .database import SteemBlock
import redis
namespace = "/status"
room = "steem"


def run():
    socketio = SocketIO(message_queue='redis://')
    steem = Steem("wss://steemd.steemit.com")
    chain = Blockchain(mode="head", steem_instance=steem)
    print(chain.steem.rpc.url, flush=True)
    for block in chain.blocks():
        timestamp = int(datetime.strptime(block["timestamp"], '%Y-%m-%dT%H:%M:%S').timestamp())
        num_ops = sum([len(tx["operations"]) for tx in block["transactions"]])
        num_txs = len(block["transactions"])
        SteemBlock(timestamp, block.get("block_num", None), num_txs, num_ops)
        notice = {
            "block": block.get("block_num", 0),
            "timestamp": timestamp,
            "num_transactions": num_txs,
            "num_operations": num_ops,
        }
        print(notice, flush=True)
        socketio.emit(
            'notice',
            notice,
            namespace=namespace,
            room=room,
            broadcast=True)


if __name__ == "__main__":
    run()
