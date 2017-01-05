#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(
    description="Command line tool to manage the stats page"
)

parser.add_argument('network', choices=["bitshares", "steem", "test"])

args = parser.parse_args()

if args.network == "test":
    from app import monitor_testnet
    monitor_testnet.run()
elif args.network == "bitshares":
    from app import monitor_bitshares
    monitor_bitshares.run()
elif args.network == "steem":
    from app import monitor_steem
    monitor_steem.run()
