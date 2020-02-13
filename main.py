import sys, os
from miner import Miner
from multiprocessing import Process
from utils import config


def main():
    for i in range(config.num_miners):
        p = Process(target=Miner, args=[i, i+5001])
        p.start()


if __name__ == "__main__":
    main()