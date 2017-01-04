#!/usr/bin/env python3
import argparse

from app import monitor_bitshares, monitor_steem, monitor_testnet

parser = argparse.ArgumentParser(
    description="Command line tool to manage the stats page"
)

parser.add_argument('network', choices=["bitshares", "steem", "test"])

args = parser.parse_args()

if args.network == "test":
    monitor_testnet.run()
elif args.network == "bitshares":
    monitor_bitshares.run()
elif args.network == "steem":
    monitor_steem.run()
