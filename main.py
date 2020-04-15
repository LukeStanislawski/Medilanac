import sys, os
from miner.miner import Miner
from multiprocessing import Process
from utils.config import Config
import urllib3


def reset_exchange():
	http = urllib3.PoolManager()
	r = http.request('GET', Config.reset_exchange_addr)
	print("Exchange response to reset request: {}".format(r.data))


def main():
    Config.validate()
    reset_exchange()

    for i in range(Config.num_miners):
        p = Process(target=Miner, args=[i, i+5000])
        p.start()


if __name__ == "__main__":
    main()