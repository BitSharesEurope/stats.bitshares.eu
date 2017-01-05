from datetime import datetime
from bitshares.bitshares import BitShares
from bitshares.blockchain import Blockchain
from flask_socketio import SocketIO
from . database import BTSBlock
import redis
namespace = "/status"
room = "bts"


def run():
    socketio = SocketIO(message_queue='redis://')
    bitshares = BitShares(node="wss://this.uptick.rocks/")
    chain = Blockchain(mode="head", bitshares_instance=bitshares)
    print(chain.bitshares.rpc.url)
    for block in chain.blocks():
        timestamp = int(datetime.strptime(block["timestamp"], '%Y-%m-%dT%H:%M:%S').timestamp())
        num_ops = sum([len(tx["operations"]) for tx in block["transactions"]])
        num_txs = len(block["transactions"])
        BTSBlock(timestamp, block.get("block_num", None), num_txs, num_ops)
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
